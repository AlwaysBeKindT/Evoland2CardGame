from enum import Enum

import pygame

import constants
from card_location import Hand, Back, Front
from card_sprites import get_cards, CardSprite

def gen_player_hand_cards(is_player_one):
  player_hand_cards = get_cards()
  card_sprites = []
  for i in range(3):
    card_sprites.append(CardSprite(player_hand_cards[i], i, is_player_one))
  return card_sprites

class Direction(Enum):
  # 将方法与枚举成员绑定
  LEFT = ("can_move_left", "move_left")
  RIGHT = ("can_move_right", "move_right")
  UP = ("can_move_up", "move_up")
  DOWN = ("can_move_down", "move_down")

  def __init__(self, check_method, move_method):
    self.check_method = check_method  # 存储方法名称
    self.move_method = move_method

  def can_move(self, location, group, cards):
    # 通过反射调用对应方法
    return getattr(location, self.check_method)(group, cards)

  def move(self, location, group, cards):
    getattr(location, self.move_method)(group, cards)

card_locations = [[Hand(0), Back(0), Front(0)], [Hand(1), Back(1), Front(1)], [Hand(2), Back(2), Front(2)]]

def print_game_state(cards):
  for row in cards:
    print("|".join(f"{card.card.cn[:3]}({card.health:2})" if card else "       " for card in row))

can_move_up = pygame.image.load("./images/can_move.png")
can_move_up = pygame.transform.scale(can_move_up,
  (constants.handle_wight(can_move_up.get_width()), constants.handle_height(can_move_up.get_height())))
can_move_up_rect = can_move_up.get_rect()
can_move_left = pygame.transform.rotate(can_move_up, 90)
can_move_left_rect = can_move_left.get_rect()
can_move_down = pygame.transform.rotate(can_move_up, 180)
can_move_down_rect = can_move_down.get_rect()
can_move_right = pygame.transform.rotate(can_move_up, 270)
can_move_right_rect = can_move_right.get_rect()

class CardsGroup(pygame.sprite.Group):
  select = None
  focus = None

  def __init__(self, is_player_one):
    super().__init__()
    game_cards_one = [None, None, None]
    game_cards_two = [None, None, None]
    game_cards_three = [None, None, None]
    self.game_cards = [game_cards_one, game_cards_two, game_cards_three]
    self.is_player_one = is_player_one
    self.hand_column = 0 if is_player_one else 2
    self.front_column = 2 if is_player_one else 0

  def gen_cards(self):
    cards = gen_player_hand_cards(self.is_player_one)
    self.add(cards)
    idx = 0 if self.is_player_one else 2
    if len(cards) != 3:
      raise ValueError("Cards len must be 3")
    for i in range(3):
      self.game_cards[i][idx] = cards[i]
    self.focus = cards[0]
    self.focus.handle_focus()

  def choose(self, owner_player):
    hand_column = self.hand_column
    if self.select is not None:
      if self.select.column == hand_column:
        self.select.handle_unchoose()
      if self.select.column != hand_column and self.select.card.cost > owner_player.mana:
        return
      if self.select.column != hand_column:
        self.select.handle_unfocus()
        self.select_new_focus()
        owner_player.mana -= self.select.card.cost
      self.select = None
    else:
      self.select = self.focus
      # 处理选择事件
      if self.select.column == hand_column:
        self.select.handle_choose(owner_player.mana >= self.select.card.cost)

  def select_new_focus(self):
    hand_column = self.hand_column
    for idx in range(3):
      if self.game_cards[idx][hand_column] is not None:
        self.focus = self.game_cards[idx][hand_column]
        break

  def handle_can_move_icron(self):
    if self.select is None or self.select.column == self.hand_column:
      return
    rect = self.select.rect
    # 使用卡片中心点坐标作为基准
    card_center_x = rect.centerx
    card_center_y = rect.centery
    # 向上箭头：卡片中心正上方
    can_move_up_rect.center = (card_center_x, card_center_y - rect.height // 2 - can_move_up.get_height() // 2)
    # 向下箭头：卡片中心正下方
    can_move_down_rect.center = (card_center_x, card_center_y + rect.height // 2 + can_move_down.get_height() // 2)
    # 向左箭头：卡片中心正左方
    can_move_left_rect.center = (card_center_x - rect.width // 2 - can_move_left.get_width() // 2, card_center_y)
    # 向右箭头：卡片中心正右方
    can_move_right_rect.center = (card_center_x + rect.width // 2 + can_move_right.get_width() // 2, card_center_y)
    dirty_rects = []
    card_location = card_locations[self.select.row][self.select.column]
    if card_location.can_move_up(self, self.game_cards):
      constants.screen.blit(can_move_up, can_move_up_rect)
      dirty_rects.append(can_move_up_rect)
    if card_location.can_move_left(self, self.game_cards):
      constants.screen.blit(can_move_left, can_move_left_rect)
      dirty_rects.append(can_move_left_rect)
    if card_location.can_move_down(self, self.game_cards):
      constants.screen.blit(can_move_down, can_move_down_rect)
      dirty_rects.append(can_move_down_rect)
    if card_location.can_move_right(self, self.game_cards):
      constants.screen.blit(can_move_right, can_move_right_rect)
      dirty_rects.append(can_move_right_rect)
    # 仅更新相关区域
    pygame.display.update(dirty_rects)

  def move_choose(self, owner_player, direction):
    self_select = self.select
    if self_select is None:
      self.hand_move_focus(direction)
      return
    column = self_select.column
    if self.is_card_in_hand(self_select) and owner_player.mana < self_select.card.cost and self.play_card(direction):
      return
    if self.is_card_in_hand(self_select) and self.play_card(direction):
      self_select.handle_unchoose()
    card_location = card_locations[self_select.row][column if self.is_player_one else 2 - column]
    if direction.can_move(card_location, self, self.game_cards):
      direction.move(card_location, self, self.game_cards)
      if column == self.hand_column and direction == (Direction.LEFT if self.is_player_one else Direction.RIGHT):
        owner_player.mana += self_select.card.profit
        self.select_new_focus()
        self.remove(self_select)
      if self.select is not None and self.is_card_return(column, self.select):
        self.select = None
        self_select.handle_unchoose()
      self.update_all_card_row_column()
    print_game_state(self.game_cards)

  def update_all_card_row_column(self):
    for row in range(3):
      for column in range(3):
        card = self.game_cards[row][column]
        if card is not None:
          card.update_row_column(row, column)

  def is_card_in_hand(self, card):
    return card.column == 0 if self.is_player_one else card.column == 2

  def is_card_return(self, column, card):
    return card.column == 0 and column > 0 if self.is_player_one else card.column == 2 and column < 2

  def play_card(self, direction):
    return direction == Direction.RIGHT if self.is_player_one else direction == Direction.LEFT

  def hand_move_focus(self, direction):
    focus = self.focus
    hand_column = self.hand_column
    if direction == Direction.UP:
      for row in range(focus.row - 1, -1, -1):
        if self.game_cards[row][hand_column] is not None:
          focus = self.game_cards[row][hand_column]
          focus.handle_focus()
          break
    elif direction == Direction.DOWN:
      for row in range(focus.row + 1, 3):
        if self.game_cards[row][hand_column] is not None:
          focus = self.game_cards[row][hand_column]
          focus.handle_focus()
          break
    if self.focus != focus:
      self.focus.handle_unfocus()
      focus.handle_focus()
    self.focus = focus
