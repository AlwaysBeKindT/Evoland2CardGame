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

def add_soft_shadow(image, shadow_color=(255, 100, 100), shadow_size=10, alpha=80):
  """
  为图像添加四边柔和阴影
  参数：
  - shadow_color: 阴影颜色 (默认亮红色)
  - shadow_size: 阴影大小/偏移量 (像素)
  - alpha: 阴影透明度 (0-255，值越小越透明)
  """
  # 获取原图尺寸
  img_w, img_h = image.get_size()

  # 创建带透明通道的新画布（向四周扩展阴影区域）
  expanded_size = shadow_size * 2
  shadow_surface = pygame.Surface((img_w + expanded_size, img_h + expanded_size), pygame.SRCALPHA)

  # 绘制四边阴影（渐变效果）
  for i in range(shadow_size, 0, -1):
    # 动态计算透明度
    current_alpha = int(alpha * (i / shadow_size))
    # 绘制右侧阴影
    pygame.draw.rect(shadow_surface, (*shadow_color, current_alpha), (img_w - i, i, shadow_size, img_h - i * 2))
    # 绘制底部阴影
    pygame.draw.rect(shadow_surface, (*shadow_color, current_alpha), (i, img_h - i, img_w - i * 2, shadow_size))
    # 绘制左侧阴影
    pygame.draw.rect(shadow_surface, (*shadow_color, current_alpha), (0, i, shadow_size, img_h - i * 2))
    # 绘制顶部阴影
    pygame.draw.rect(shadow_surface, (*shadow_color, current_alpha), (i, 0, img_w - i * 2, shadow_size))

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
  KURO = ("库洛", "C01", Skill.RANGED_ATTACKS, 7, 3, 5, 10)
  FIONA = ("菲娜", "C02", Skill.HEALING_ENERGY, 5, 2, 2, 8)
  VELVET = ("丝绒", "C03", None, 4, 2, 3, 8)
  MENOS = ("梅诺斯", "C04", Skill.SWIFT_TRAMPLING, 8, 3, 5, 9)
  CERES = ("刻瑞斯", "C05", None, 9, 4, 9, 9)
  DALKIN = ("达尔金", "C06", Skill.PREEMPTIVE_STRIKE, 8, 3, 7, 8)
  EMPEROR_RUSSELL = ("罗塞尔皇帝", "C07", None, 6, 3, 6, 7)
  LAGO_LEGRAND = ("拉戈·雷格兰德", "C08", Skill.RANGED_ATTACKS, 4, 2, 2, 3)
  DEMON_KING_ARTUS = ("恶魔君主阿图斯", "C09", Skill.SWIFT_TRAMPLING, 7, 3, 5, 7)
  NAWEI = ("纳威伊", "CAA", Skill.MAGIC_STRIKES, 0, 1, 0, 3)
  YODA_TREE = ("尤达树", "C10", Skill.MAGIC_STRIKES, 3, 2, 0, 12)
  WEAPON = ("武器", "C11", Skill.SWIFT_TRAMPLING, 9, 4, 12, 2)
  PROFESSOR_KILO = ("基罗教授", "C12", Skill.RANGED_ATTACKS, 6, 3, 5, 3)
  MR_MADEVILLE = ("玛德维尔先生", "C13", Skill.MAGIC_STRIKES, 2, 1, 0, 10)
  PIRATE_ROBERTS = ("海盗罗伯茨", "C14", None, 6, 3, 5, 7)
  BLUE_TASK_FORCE = ("蓝色特遣队", "C15", Skill.PREEMPTIVE_STRIKE, 1, 1, 0, 2)
  GREEN_TASK_FORCE = ("绿色特遣队", "C16", Skill.SWIFT_TRAMPLING, 1, 1, 0, 2)
  RED_TASK_FORCE = ("红色特遣队", "C17", Skill.RANGED_ATTACKS, 1, 1, 0, 2)
  LEGENDARY_BLACKSMITH = ("传奇铁匠", "C18", Skill.MAGIC_STRIKES, 2, 1, 1, 6)
  INVENTOR = ("发明家", "C19", None, 2, 1, 2, 2)
  ORC = ("半兽人", "C20", Skill.MAGIC_STRIKES, 0, 1, 1, 1)
  JON_SNOW = ("琼恩·薛诺", "C21", Skill.RANGED_ATTACKS, 5, 2, 4, 5)
  RENO = ("里诺", "C22", Skill.SWIFT_TRAMPLING, 7, 3, 5, 8)
  CHERRY = ("樱桃", "C23", Skill.RANGED_ATTACKS, 6, 3, 4, 6)
  PLUM = ("梅子", "C24", Skill.RANGED_ATTACKS, 6, 3, 4, 6)
  BIG_MAGUS = ("大马格斯", "C25", Skill.RANGED_ATTACKS, 9, 4, 10, 3)
  YATAI = ("雅塔伊", "C26", Skill.SWIFT_TRAMPLING, 7, 3, 5, 8)
  LIEUTENANT = ("中尉", "C27", Skill.PREEMPTIVE_STRIKE, 8, 3, 6, 10)
  PROPHET = ("先知", "C28", Skill.PREEMPTIVE_STRIKE, 9, 4, 8, 7)
  FLIGHT_GUARDIAN = ("飞行守护", "C29", None, 13, 5, 10, 18)
  KURO_ = ("库洛?", "C30", Skill.PREEMPTIVE_STRIKE, 7, 3, 5, 8)
  BYBLOS = ("比布鲁斯", "C31", Skill.RANGED_ATTACKS, 7, 3, 5, 7)
  SAXU = ("萨旭", "C32", Skill.RANGED_ATTACKS, 7, 3, 5, 7)
  GIANT_CLAWED_MANTIS = ("巨钳螳螂", "C33", Skill.SWIFT_TRAMPLING, 6, 3, 6, 5)
  FOREST_GUARDIAN = ("森林守护者", "C34", Skill.SWIFT_TRAMPLING, 4, 2, 3, 4)
  CAPTAIN_ABABA = ("阿巴巴船长", "C35", Skill.SWIFT_TRAMPLING, 10, 4, 9, 9)
  MALICIOUS_TROLL = ("恶毒的大巨魔", "C36", Skill.RANGED_ATTACKS, 7, 3, 7, 7)
  SPIRIT_OF_THE_WIND = ("风之精灵", "C37", Skill.RANGED_ATTACKS, 2, 1, 1, 2)
  VIKINGS = ("维京人", "C38", Skill.SWIFT_TRAMPLING, 4, 2, 2, 3)
  DEVIL = ("恶魔", "C39", Skill.SWIFT_TRAMPLING, 3, 2, 3, 2)
  LIBRARY_DIRECTOR = ("图书馆馆长", "C40", Skill.MAGIC_STRIKES, 1, 1, 0, 6)
  MARKEY = ("马基", "C41", Skill.MAGIC_STRIKES, 0, 1, 0, 4)
  PIRATE = ("海盗", "C42", Skill.PREEMPTIVE_STRIKE, 4, 2, 3, 3)
  MORIA_TROLLS = ("摩瑞亚巨魔", "C43", Skill.SWIFT_TRAMPLING, 5, 2, 4, 5)
  C4PO = ("C4PO", "C44", Skill.PREEMPTIVE_STRIKE, 4, 2, 2, 5)
  DEFORMABLE_MONSTER = ("变形怪", "C45", None, 1, 1, 1, 1)
  MOUSE = ("老鼠", "C46", None, 2, 1, 2, 1)
  BIG_EYED_DEFORMED_MONSTER = ("大眼变形怪", "C47", None, 2, 1, 3, 1)
  WIZARD = ("巫师", "C48", Skill.RANGED_ATTACKS, 4, 2, 4, 2)
  GHOST = ("幽灵", "C49", None, 3, 2, 2, 5)
  AMOS = ("阿莫斯", "C50", None, 4, 2, 1, 10)
  BAT = ("蝙蝠", "C51", None, 1, 1, 1, 2)
  MADMAN = ("狂徒", "C52", Skill.SWIFT_TRAMPLING, 3, 2, 2, 2)
  SQUIRREL = ("松鼠", "C53", Skill.RANGED_ATTACKS, 2, 1, 1, 2)
  IMPERIAL_GUARD = ("帝国守卫", "C54", Skill.PREEMPTIVE_STRIKE, 2, 1, 1, 2)
  GRIZZLY_BEAR = ("灰熊", "C55", Skill.SWIFT_TRAMPLING, 4, 2, 3, 3)
  NINJA_SQUIRREL = ("忍者松鼠", "C56", Skill.RANGED_ATTACKS, 4, 2, 3, 3)
  THE_GIANT_STONE_OF_MAYENNE = ("马耶纳巨石", "C57", None, 3, 2, 0, 11)
  MAMMOTH = ("猛犸象", "C58", None, 3, 2, 1, 8)
  CRUSHER = ("粉碎机", "C59", Skill.PREEMPTIVE_STRIKE, 5, 2, 5, 1)
  PROGRAMMER_ART = ("程序员美工", "C60", Skill.MAGIC_STRIKES, 4, 2, 5, 5)

  def __init__(self, cn, code, skill, cost, profit, damage, health):
    # 初始化函数，用于创建对象
    super().__init__()
    # 调用父类的初始化函数
    self.cn = cn
    # 将参数cn赋值给对象的cn属性
    self.code = code
    # 将参数code赋值给对象的code属性
    self.cost = cost
    # 将参数cost赋值给对象的cost属性
    self.profit = profit
    # 将参数profit赋值给对象的profit属性
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
    self.rect.x = constants.column_xs[0 if is_player_one else 5]

  def gen_new_card_image(self):
    # path = "images/card_no_skill.png"
    path = f"images/cards/{self.card.code}.png"
    # 修改后的初始化代码
    image = pygame.image.load(path)
    image = pygame.transform.scale(image,
      (constants.handle_wight(image.get_width()), constants.handle_height(image.get_height())))

    # 生成阴影图像（保持与原图相同尺寸）
    shadow_image = add_soft_shadow(image)

    # 创建选择状态画布（扩展宽度但保持中心对齐）
    sale_width = final_sale.get_width()
    select_width = image.get_width() + sale_width * 2  # 左右各加一个按钮宽度
    select_height = max(image.get_height(), final_sale.get_height())

    # 创建透明画布
    select_image = pygame.Surface((select_width, select_height), pygame.SRCALPHA)

    # 计算所有元素的中心基准点
    base_center_x = select_width // 2
    base_center_y = select_height // 2

    # 将卡牌绘制在画布中心
    card_rect = image.get_rect(center=(base_center_x, base_center_y))
    select_image.blit(shadow_image, card_rect)  # 使用阴影图像

    # 添加左右按钮（从中心点偏移）
    select_image.blit(final_sale,
      (base_center_x - sale_width - image.get_width() // 2, base_center_y - final_sale.get_height() // 2))
    select_image.blit(final_play,
      (base_center_x + image.get_width() // 2, base_center_y - final_play.get_height() // 2))

    # 统一所有图像的rect中心点
    self.rect = image.get_rect()  # 原始图像的位置基准
    self.rect_center = self.rect.center  # 存储基准中心坐标

    # 设置所有图像的rect为中心对齐
    self.image = image
    self.normal_image = image
    self.shadow_image = shadow_image
    self.select_image = select_image

    # 确保所有surface使用相同的中心坐标
    self.normal_rect = self.normal_image.get_rect(center=self.rect_center)
    self.shadow_rect = self.shadow_image.get_rect(center=self.rect_center)
    self.select_rect = self.select_image.get_rect(center=self.rect_center)
    return select_height, select_width

  # 攻击
  def attack(self, row_cards, owner_player, targets):
    if self.card.skill == Skill.MAGIC_STRIKES:
      owner_player.mana += 1
    if self.card.skill == Skill.HEALING_ENERGY and self.column == 1:
      row_cards[owner_player.card_group.front_column].health += 1
    if self.column == 1 and self.card.skill != Skill.RANGED_ATTACKS:
      return {}
    if self.card.damage == 0:
      return {}
    other_player = targets[1]
    target = targets[0][other_player.card_group.front_column]
    target = target if target is not None else other_player
    heart_objects = {self: owner_player, target: other_player}
    if self.card.skill == Skill.SWIFT_TRAMPLING:
      damage = self.card.damage
      if target.health < damage:
        damage -= target.health
        target.heart(self, target.health)
        if isinstance(target, CardSprite):
          if targets[0][1] is not None:
            other_card = targets[0][1]
            heart_objects[other_card] = other_player
            if other_card.health < damage:
              damage -= other_card.health
              other_card.heart(self, other_card.health)
            else:
              other_card.heart(self, damage)
          self.heart(target, target.card.damage)
          heart_objects[other_player] = other_player
          other_player.heart(self, damage)
      else:
        target.heart(self, damage)
    elif self.card.skill == Skill.PREEMPTIVE_STRIKE:
      target.heart(self, self.card.damage)
      if isinstance(target, CardSprite) and (target.card.skill == Skill.PREEMPTIVE_STRIKE or target.health > 0):
        self.heart(target, target.card.damage)
    else:
      if self.column != 1 or self.card.skill == Skill.RANGED_ATTACKS:
        target.heart(self, self.card.damage)
      if self.column != 1 and isinstance(target, CardSprite):
        self.heart(target, target.card.damage)
    for heart_object, player in heart_objects.items():
      if heart_object.health <= 0 and isinstance(heart_object, CardSprite):
        player_card_group = player.card_group
        cards = player_card_group.game_cards
        cards[heart_object.row][heart_object.column] = None
        card_operator.check_back_should_move_front(heart_object.row, player_card_group.front_column, cards)
    return heart_objects

  # 受伤
  def heart(self, heart_by, damage):
    print(f"card {self.card.code}-{self.card.cn} health {self.health} heart_by {heart_by.card.cn} damage {damage}")
    self.health -= damage

  def after_heart(self):
    if self.health <= 0:
      self.health = 0
      print(f"card {self.card.code}-{self.card.cn} dead")
      self.kill()

  def update_row_column(self, row, column):
    self.gen_new_card_image()
    self.row = row
    self.column = column
    self.rect.y = constants.row_ys[row]
    self.rect.x = constants.column_xs[column if self.is_player_one else 3 + column]

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
