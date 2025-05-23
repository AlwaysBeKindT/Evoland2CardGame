import pygame

import card_group
import constants
from card_group import CardsGroup, Direction

def draw_num(screen, font, num, x, y):
  text = font.render(str(num), True, (255, 255, 255))
  text_rect = text.get_rect()
  text_rect.center = (x * constants.wight_scale, y * constants.height_scale)
  screen.blit(text, text_rect)

def update_screen(player_one, other_player, draw_bg, screen):
  draw_bg()  # 先绘制背景
  player_one.card_group.update()  # 更新精灵状态
  player_one.card_group.draw(screen)  # 绘制精灵
  card_group.handle_can_move_icron(player_one.card_group)
  player_one.draw(screen)  # 绘制玩家状态
  other_player.card_group.update()  # 更新精灵状态
  other_player.card_group.draw(screen)  # 绘制精灵
  other_player.draw(screen)
  pygame.display.flip()  # 统一更新显示

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

  def is_press_key(self, key, key1, key2, direction):
    if self.is_player_one and key == key1 or (not self.is_player_one) and key == key2:
      self.card_group.move_choose(self, direction)
      return True
    return False

  def active(self, screen, other_player, draw_bg, clock):
    self.mana += 1
    self.card_group.gen_cards()
    self.card_group.update_all_card_row_column()
    other_player.card_group.update_all_card_row_column()
    update_screen(self, other_player, draw_bg, screen)
    # 控制是否需要重绘
    redraw_needed = True
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          print("退出游戏...")
          pygame.quit()
          exit()
        if event.type != pygame.KEYDOWN:
          continue
        key = event.key
        if self.is_player_one and key == pygame.K_SPACE or (not self.is_player_one) and key == pygame.K_RETURN:
          self.card_group.choose(self)
          redraw_needed = True
        redraw_needed = redraw_needed or self.is_press_key(key, pygame.K_a, pygame.K_LEFT, Direction.LEFT)
        redraw_needed = redraw_needed or self.is_press_key(key, pygame.K_d, pygame.K_RIGHT, Direction.RIGHT)
        redraw_needed = redraw_needed or self.is_press_key(key, pygame.K_w, pygame.K_UP, Direction.UP)
        redraw_needed = redraw_needed or self.is_press_key(key, pygame.K_s, pygame.K_DOWN, Direction.DOWN)
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
        update_screen(self, other_player, draw_bg, screen)
        redraw_needed = False
      # 设置屏幕刷新帧率
      clock.tick(60)

    cards = self.card_group.game_cards
    for row in range(3):
      row_cards = cards[row]
      if row_cards[1] is not None:
        row_cards[1].attack(row_cards, self, [other_player.card_group.game_cards[row], other_player])
      if row_cards[self.card_group.front_column] is not None:
        row_cards[self.card_group.front_column].attack(row_cards, self,
          [other_player.card_group.game_cards[row], other_player])

  # 受伤
  def heart(self, damage):
    self.health -= damage

  def after_heart(self):
    if self.health <= 0:
      print("player dead")
