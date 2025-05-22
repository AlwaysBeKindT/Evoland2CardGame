import pygame

import constants
from card_group import CardsGroup, Direction


def draw_num(screen, font, num, x, y):
  text = font.render(str(num), True, (255, 255, 255))
  text_rect = text.get_rect()
  text_rect.center = (x * constants.wight_scale, y * constants.height_scale)
  screen.blit(text, text_rect)

class Player(pygame.sprite.Sprite):
  def __init__(self, health, is_player_one):
    super().__init__()
    self.health = health
    self.is_player_one = is_player_one
    self.card_group = None
    self.mana = 0
    self.card_group = CardsGroup(is_player_one)

  def draw(self, screen):
    player_health_x = constants.player_one_health_x if self.is_player_one else constants.player_two_health_x
    draw_num(screen, constants.health_font, self.health, player_health_x, constants.player_health_y)
    player_mana_x = constants.player_one_mana_x if self.is_player_one else constants.player_two_mana_x
    draw_num(screen, constants.mana_font, self.mana, player_mana_x, constants.player_mana_y)

  def active(self, screen, other_player, draw_bg, clock):
    self.mana += 1
    self.card_group.gen_cards()
    self.update_screen(draw_bg, other_player, screen)
    # 控制是否需要重绘
    redraw_needed = True
    while True:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and (self.is_player_one and event.key == pygame.K_SPACE or (
          not self.is_player_one) and event.key == pygame.K_RETURN):
          print("enter")
          self.card_group.choose(self)
          redraw_needed = True
        if event.type == pygame.KEYDOWN and (
          self.is_player_one and event.key == pygame.K_a or (not self.is_player_one) and event.key == pygame.K_LEFT):
          print("left")
          self.card_group.move_choose(self, Direction.LEFT)
          redraw_needed = True
        if event.type == pygame.KEYDOWN and (
          self.is_player_one and event.key == pygame.K_d or (not self.is_player_one) and event.key == pygame.K_RIGHT):
          print("right")
          self.card_group.move_choose(self, Direction.RIGHT)
          redraw_needed = True
        if event.type == pygame.KEYDOWN and (
          self.is_player_one and event.key == pygame.K_w or (not self.is_player_one) and event.key == pygame.K_UP):
          print("up")
          self.card_group.move_choose(self, Direction.UP)
          redraw_needed = True
        if event.type == pygame.KEYDOWN and (
          self.is_player_one and event.key == pygame.K_s or (not self.is_player_one) and event.key == pygame.K_DOWN):
          print("down")
          self.card_group.move_choose(self, Direction.DOWN)
          redraw_needed = True
        if event.type == pygame.QUIT:
          print("退出游戏...")
          pygame.quit()
          exit()
      cards = self.card_group.game_cards
      hand_card_column = 0 if self.is_player_one else 2
      if all(row[hand_card_column] is None for row in cards) and self.card_group.select is None:
        print("all hand card used, active game.")
        break
      if self.health <= 0 or other_player.health <= 0:
        print("game over")
        return
      # 优化后的渲染流程
      if redraw_needed:
          self.update_screen(draw_bg, other_player, screen)
          redraw_needed = False
      # 设置屏幕刷新帧率
      clock.tick(60)

    cards = self.card_group.game_cards
    for row in range(3):
      row_cards = cards[row]
      if row_cards[1] is not None:
        row_cards[1].attack(row_cards, self, [other_player.card_group.game_cards[row], other_player])
      if row_cards[self.card_group.front_column] is not None:
        row_cards[self.card_group.front_column].attack(row_cards, self, [other_player.card_group.game_cards[row], other_player])

    for row in range(3):
      row_cards = cards[row]
      other_row_cards = other_player.card_group.game_cards[row]
      if row_cards[1] is not None and row_cards[1].health <= 0:
        row_cards[1] = None
      if other_row_cards[1] is not None and other_row_cards[1].health <= 0:
        other_row_cards[1] = None
      if row_cards[self.card_group.front_column] is not None and row_cards[self.card_group.front_column].health <= 0:
        row_cards[self.card_group.front_column] = None
      other_front_column = other_player.card_group.front_column
      if other_row_cards[other_front_column] is not None and other_row_cards[other_front_column].health <= 0:
        other_row_cards[other_front_column] = None

    if self.health > 0 and other_player.health > 0:
      other_player.active(screen, self, draw_bg, clock)

  def update_screen(self, draw_bg, other_player, screen):
    draw_bg()  # 先绘制背景
    self.card_group.update_all_card_row_column()
    self.card_group.update()  # 更新精灵状态
    self.card_group.draw(screen)  # 绘制精灵
    self.card_group.handle_can_move_icron()
    self.draw(screen)  # 绘制玩家状态
    other_player.card_group.update_all_card_row_column()
    other_player.card_group.update()  # 更新精灵状态
    other_player.card_group.draw(screen)  # 绘制精灵
    other_player.draw(screen)
    pygame.display.flip()  # 统一更新显示

  # 受伤
  def heart(self, damage):
    self.health -= damage

  def after_heart(self):
    if self.health <= 0:
      print("player dead")
