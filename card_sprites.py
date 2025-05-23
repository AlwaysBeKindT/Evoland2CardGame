import random
from enum import Enum

import pygame

import card_operator
import constants

sale_image = pygame.image.load("images/sale.png")
cant_play_image = pygame.image.load("images/cant_play.png")
play_image = pygame.image.load("images/play.png")
final_sale = pygame.transform.scale(sale_image,
  (constants.handle_wight(sale_image.get_width()), constants.handle_height(sale_image.get_height())))
final_cant_play = pygame.transform.scale(cant_play_image,
  (constants.handle_wight(cant_play_image.get_width()), constants.handle_height(cant_play_image.get_height())))
final_play = pygame.transform.scale(play_image,
  (constants.handle_wight(play_image.get_width()), constants.handle_height(play_image.get_height())))

def get_card_by_code_number(random_id):
  # 遍历所有Card枚举成员
  idx = 1
  for member in Card:
    if idx == random_id:
      return member
    idx += 1
  return None  # 如果没有找到匹配的成员

# 定义一个函数，用于获取三张牌
def get_cards():
  # 生成一个随机数，范围是1到Card.__members__的长度
  one = random.randint(1, len(Card.__members__))
  # 生成一个随机数，范围是1到Card.__members__的长度
  two = random.randint(1, len(Card.__members__))
  # 生成一个随机数，范围是1到Card.__members__的长度
  three = random.randint(1, len(Card.__members__))
  # 返回三张牌
  return [get_card_by_code_number(one), get_card_by_code_number(two), get_card_by_code_number(three)]

def add_soft_shadow(image, shadow_color=(139, 0, 0), shadow_size=20, alpha=80):
  """
  为图像添加带偏移的柔和阴影
  参数：
  - shadow_color: 阴影颜色 (默认淡红色)
  - shadow_size: 阴影大小/偏移量 (像素)
  - alpha: 阴影透明度 (0-255)
  """
  # 获取原图尺寸
  img_w, img_h = image.get_size()

  # 创建带透明通道的新画布（向右下方扩展阴影区域）
  shadow_surface = pygame.Surface((img_w + shadow_size, img_h + shadow_size), pygame.SRCALPHA)

  # 绘制阴影层（由深到浅的渐变效果）
  for i in range(shadow_size, 0, -1):
    # 动态计算透明度
    current_alpha = int(alpha * (i / shadow_size))
    # 绘制右侧阴影
    pygame.draw.rect(shadow_surface, (*shadow_color, current_alpha), (img_w - i, i, shadow_size, img_h - i * 2))
    # 绘制底部阴影
    pygame.draw.rect(shadow_surface, (*shadow_color, current_alpha), (i, img_h - i, img_w - i * 2, shadow_size))

  # 将原图绘制到阴影层左上方
  shadow_surface.blit(image, (0, 0))

  return shadow_surface

def handle_card_info(card, image, self_health):
  width = image.get_width()
  height = image.get_height()
  if card.skill is not None:
    skill = pygame.image.load("images/" + str.lower(card.skill.name) + ".png")
    skill = pygame.transform.scale(skill,
      (constants.handle_wight(skill.get_width()), constants.handle_height(skill.get_height())))
    skill_rect = skill.get_rect()
    skill_rect.center = (width * 0.86, height * 0.1)
    image.blit(skill, skill_rect)
  cost = constants.card_font.render(str(card.cost), True, (255, 255, 255))
  cost_rect = cost.get_rect()
  cost_rect.center = (width * 0.128, height * 0.1)
  image.blit(cost, cost_rect)
  name = constants.card_font.render(card.cn, True, (135, 206, 235))
  name_rect = name.get_rect()
  name_rect.center = (width * 0.5, height * 0.5)
  image.blit(name, name_rect)
  attack = constants.card_font.render(str(card.damage), True, (255, 255, 255))
  attack_rect = attack.get_rect()
  attack_rect.center = (width * 0.128, height * 0.88)
  image.blit(attack, attack_rect)
  health = constants.card_font.render(str(self_health), True, (255, 255, 255))
  health_rect = health.get_rect()
  health_rect.center = (width * 0.86, height * 0.88)
  image.blit(health, health_rect)

class Skill(Enum):
  RANGED_ATTACKS = ("远程攻击:即使在后排也能攻击",)
  PREEMPTIVE_STRIKE = ("先发制人:首先造成伤害",)
  SWIFT_TRAMPLING = ("迅猛践踏:继续对下个目标造成伤害",)
  MAGIC_STRIKES = ("魔法出击:每回合能返还一个马纳",)
  HEALING_ENERGY = ("治疗能量:稀有,可以治疗前方的卡牌",)

class Card(Enum):
  KU_LUO = ("库洛", "C01", 7, 3, Skill.RANGED_ATTACKS, 5, 10)
  FEI_NA = ("菲娜", "C02", 5, 2, Skill.HEALING_ENERGY, 2, 8)
  TIAN_E_RONG = ("天鹅绒", "C03", 4, 2, None, 3, 8)
  MENG_NUO_SI = ("蒙诺斯", "C04", 8, 3, Skill.SWIFT_TRAMPLING, 5, 9)
  HUNTER = ("猎人", "C20", 0, 1, Skill.MAGIC_STRIKES, 1, 1)
  SLAM = ("史莱姆", "C45", 1, 1, None, 1, 1)
  MOUSE = ("老鼠", "C46", 2, 1, None, 2, 1)
  BAT = ("蝙蝠", "C51", 1, 1, None, 1, 2)
  MUSHROOM_PEOPLE = ("狂人", "C52", 3, 2, Skill.SWIFT_TRAMPLING, 2, 2)
  SQUIRREL = ("松鼠", "C53", 2, 1, Skill.RANGED_ATTACKS, 1, 2)

  def __init__(self, cn, code, cost, profit, skill, damage, health):
    super().__init__()
    self.cn = cn
    self.code = code
    self.cost = cost
    self.profit = profit
    self.skill = skill
    self.damage = damage
    self.health = health

class CardSprite(pygame.sprite.Sprite):
  def __init__(self, card, idx, is_player_one):
    super().__init__()
    self.rect = None
    self.image = None
    self.normal_image = None
    self.shadow_image = None
    self.select_image = None
    self.card = card
    self.health = card.health
    self.row = idx
    self.is_player_one = is_player_one
    self.column = 0 if is_player_one else 2
    select_height, select_width = self.gen_new_card_image()
    if not is_player_one:
      sale = pygame.transform.flip(final_sale, True, False)
      cant_play = pygame.transform.flip(final_cant_play, True, False)
      play = pygame.transform.flip(final_play, True, False)
    else:
      sale = final_sale.copy()
      cant_play = final_cant_play.copy()
      play = final_play.copy()
    rect_centers = [(sale.get_width() // 2, int(select_height * 0.5)),
      (select_width - play.get_width() // 2, int(select_height * 0.5))]
    sale_rect = sale.get_rect()
    sale_rect.center = rect_centers[0 if is_player_one else 1]
    play_rect = play.get_rect()
    play_rect.center = rect_centers[1 if is_player_one else 0]
    cant_play_rect = cant_play.get_rect()
    cant_play_rect.center = rect_centers[1 if is_player_one else 0]

    self.sale = sale
    self.sale_rect = sale_rect
    self.cant_play = cant_play
    self.cant_play_rect = cant_play_rect
    self.play = play
    self.play_rect = play_rect
    self.rect.y = constants.row_ys[idx]
    self.rect.x = constants.column_xs[idx][0 if is_player_one else 5]

  def gen_new_card_image(self):
    path = "images/card_no_skill.png"
    image = pygame.image.load(path)
    image = pygame.transform.scale(image,
      (constants.handle_wight(image.get_width()), constants.handle_height(image.get_height())))
    handle_card_info(self.card, image, self.health)
    shadow_image = add_soft_shadow(image)  # 红色5像素边框
    # 创建足够大的选择状态画布
    select_width = image.get_width() + final_sale.get_width() * 2  # 增加50%宽度
    select_height = image.get_height()
    select_image = pygame.Surface((select_width, select_height), pygame.SRCALPHA)
    # 将原卡牌图像居中
    card_rect = image.get_rect(center=(select_width // 2, select_height // 2))
    select_image.blit(shadow_image, card_rect)
    self.image = image
    self.rect = image.get_rect()
    self.normal_image = image
    self.shadow_image = shadow_image
    self.select_image = select_image
    return select_height, select_width

  # 攻击
  def attack(self, row_cards, owner_player, targets):
    if self.card.skill == Skill.MAGIC_STRIKES:
      owner_player.mana += 1
    if self.card.skill == Skill.HEALING_ENERGY and self.column == 1:
      row_cards[owner_player.card_group.front_column].health += 1
    if self.column == 1 and self.card.skill != Skill.RANGED_ATTACKS:
      return
    other_player = targets[1]
    target = targets[0][other_player.card_group.front_column]
    target = target if target is not None else other_player
    heart_objects = {self: owner_player, target: other_player}
    if self.card.skill == Skill.SWIFT_TRAMPLING:
      damage = self.card.damage
      if target.health < damage:
        damage -= target.health
        target.heart(target.health)
        if isinstance(target, CardSprite):
          if targets[0][1] is not None:
            other_card = targets[0][1]
            heart_objects[other_card] = other_player
            if other_card.health < damage:
              damage -= other_card.health
              other_card.heart(other_card.health)
            else:
              other_card.heart(damage)
          self.heart(target.card.damage)
          heart_objects[other_player] = other_player
          other_player.heart(damage)
      else:
        target.heart(damage)
    elif self.card.skill == Skill.PREEMPTIVE_STRIKE:
      target.heart(self.card.damage)
      if isinstance(target, CardSprite) and (target.card.skill == Skill.PREEMPTIVE_STRIKE or target.health > 0):
        self.heart(target.card.damage)
    else:
      if self.column != 1:
        target.heart(self.card.damage)
      if isinstance(target, CardSprite):
        self.heart(target.card.damage)
    for heart_object, player in heart_objects.items():
      if heart_object.health <= 0 and isinstance(heart_object, CardSprite):
        player_card_group = player.card_group
        cards = player_card_group.game_cards
        cards[heart_object.row][heart_object.column] = None
        card_operator.check_back_should_move_front(heart_object.row, player_card_group.front_column, cards)
      heart_object.after_heart()

  # 受伤
  def heart(self, damage):
    self.health -= damage

  def after_heart(self):
    if self.health <= 0:
      print("card dead")
      self.kill()

  def update_row_column(self, row, column):
    self.gen_new_card_image()
    self.row = row
    self.column = column
    self.rect.y = constants.row_ys[row]
    self.rect.x = constants.column_xs[row][column if self.is_player_one else 3 + column]

  # 获得焦点
  def handle_focus(self):
    self.image = self.shadow_image

  # 失去焦点
  def handle_unfocus(self):
    self.image = self.normal_image

  # 被选择后，在牌的左右展示卖出和放入棋盘的图标
  # 定义handle_choose函数，用于处理选择
  def handle_choose(self, can_sale):
    profit = constants.card_font.render(str(self.card.profit), True, (255, 255, 255))
    profit_rect = profit.get_rect()
    sale = self.sale
    profit_rect.center = (sale.get_width() * 0.55, sale.get_height() * 0.45)
    sale.blit(profit, profit_rect)
    self.select_image.blit(sale, self.sale_rect)
    self.select_image.blit(self.play if can_sale else self.cant_play,
      self.play_rect if can_sale else self.cant_play_rect)
    self.image = self.select_image
    self.rect.x = self.rect.x - sale.get_width()

  # 取消选择后，需要恢复原状
  def handle_unchoose(self):
    self.image = self.shadow_image
    self.rect.x = self.rect.x + self.sale.get_width()
