class CardLocation:
  def __init__(self, row, column):
    self.row = row
    self.column = column

  def can_move_right(self, card_group, cards):
    # 判断卡片是否可以向右移动
    raise Exception("Not implemented")

  def can_move_left(self, card_group, cards):
    # 判断卡片是否可以向左移动
    raise Exception("Not implemented")

  def can_move_up(self, card_group, cards):
    # 判断卡片是否可以向上移动
    raise Exception("Not implemented")

  def can_move_down(self, card_group, cards):
    # 判断卡片是否可以向下移动
    raise Exception("Not implemented")

  def move_right(self, card_group, cards):
    # 卡片向右移动
    raise Exception("Not implemented")

  def move_left(self, card_group, cards):
    # 卡片向左移动
    raise Exception("Not implemented")

  def move_up(self, card_group, cards):
    # 卡片向上移动
    raise Exception("Not implemented")

  def move_down(self, card_group, cards):
    # 卡片向下移动
    raise Exception("Not implemented")

class Hand(CardLocation):
  def __init__(self, row):
    super().__init__(row, 0)

  def can_move_left(self, card_group, cards):
    return True

  def can_move_up(self, card_group, cards):
    return False

  def can_move_down(self, card_group, cards):
    return False

  def can_move_right(self, card_group, cards):
    # 当前卡片被选中且是手牌区的卡片
    current_card = cards[self.row][0]
    if card_group.select is None or card_group.select != current_card:
      return False
    # 检查所有行、右侧两列区域是否有空位
    return any(cards[row][col] is None for row in range(3) for col in [1, 2])

  def move_right(self, card_group, cards):
    if card_group.select is None or card_group.select != cards[self.row][0]:
      raise ValueError("select and focus not equal!")
    if cards[self.row][2] is None:
      cards[self.row][0].source_row = self.row
      cards[self.row][0].column = 2
      cards[self.row][2], cards[self.row][0] = cards[self.row][0], cards[self.row][2]
      return
    if cards[self.row][1] is None:
      cards[self.row][0].source_row = self.row
      cards[self.row][0].column = 1
      cards[self.row][1], cards[self.row][0] = cards[self.row][0], cards[self.row][1]
      return
    for row in range(3):
      if cards[row][2] is None:
        cards[self.row][0].source_row = self.row
        cards[self.row][0].column = 2
        cards[self.row][0].row = row
        cards[row][2], cards[self.row][0] = cards[self.row][0], cards[row][2]
        return
      if cards[row][1] is None:
        cards[self.row][0].source_row = self.row
        cards[self.row][0].column = 1
        cards[self.row][0].row = row
        cards[row][1], cards[self.row][0] = cards[self.row][0], cards[row][1]
        return
  def move_left(self, card_group, cards):
    cards[card_group.select.row][card_group.select.column] = None
    card_group.select = None

def normal_can_move_up(self, cards):
  if self.row == 0:
    return False
  is_row_0_any_none = cards[0][1] is None or cards[0][2] is None
  if self.row == 1:
    return is_row_0_any_none
  return is_row_0_any_none or cards[1][1] is None or cards[1][2]

def normal_can_move_down(self, cards):
  if self.row == 2:
    return False
  is_row_2_any_none = cards[2][1] is None or cards[2][2] is None
  if self.row == 1:
    return is_row_2_any_none
  return cards[1][1] is None or cards[1][2] is None or is_row_2_any_none

class Back(CardLocation):
  def __init__(self, row):
    super().__init__(row, 1)

  def can_move_left(self, card_group, cards):
    return True

  def can_move_right(self, card_group, cards):
    return True

  def can_move_up(self, card_group, cards):
    return normal_can_move_up(self, cards)

  def can_move_down(self, card_group, cards):
    return normal_can_move_down(self, cards)

  def move_left(self, card_group, cards):
    if not self.can_move_left(card_group, cards):
      raise Exception("can not move left")
    cards[self.row][1].row = cards[self.row][1].source_row
    cards[self.row][1].column = 0
    cards[cards[self.row][1].source_row][0], cards[self.row][1] = cards[self.row][1], \
      cards[cards[self.row][1].source_row][0]

  def move_right(self, card_group, cards):
    if not self.can_move_right(card_group, cards):
      raise Exception("can not move right")
    cards[self.row][1].column = 2
    cards[self.row][2], cards[self.row][1] = cards[self.row][1], cards[self.row][2]

  def move_up(self, card_group, cards):
    if not self.can_move_up(card_group, cards):
      raise Exception("can not move up")
    if cards[self.row - 1][2] is None:
      cards[self.row][1].column = 2
      cards[self.row][1].row = self.row - 1
      cards[self.row - 1][2], cards[self.row][1] = cards[self.row][1], cards[self.row - 1][2]
      return
    if cards[self.row - 1][1] is None:
      cards[self.row][1].column = 1
      cards[self.row][1].row = self.row - 1
      cards[self.row - 1][1], cards[self.row][1] = cards[self.row][1], cards[self.row - 1][1]
      return
    if self.row == 2:
      if cards[0][2] is None:
        cards[self.row][1].row = 0
        cards[self.row][1].column = 2
        cards[0][2], cards[self.row][1] = cards[self.row][1], cards[0][2]
        return
      if cards[0][1] is None:
        cards[self.row][1].row = 0
        cards[self.row][1].column = 1
        cards[0][1], cards[self.row][1] = cards[self.row][1], cards[0][1]
        return

  def move_down(self, card_group, cards):
    if not self.can_move_down(card_group, cards):
      raise Exception("can not move down")
    if cards[self.row + 1][2] is None:
      cards[self.row][1].column = 2
      cards[self.row][1].row = self.row + 1
      cards[self.row + 1][2], cards[self.row][1] = cards[self.row][1], cards[self.row + 1][2]
      return
    if cards[self.row + 1][1] is None:
      cards[self.row][1].column = 1
      cards[self.row][1].row = self.row + 1
      cards[self.row + 1][1], cards[self.row][1] = cards[self.row][1], cards[self.row + 1][1]
      return
    if self.row == 0:
      if cards[2][2] is None:
        cards[self.row][1].row = 2
        cards[self.row][1].column = 2
        cards[2][2], cards[self.row][1] = cards[self.row][1], cards[2][2]
        return
      if cards[2][1] is None:
        cards[self.row][1].row = 2
        cards[self.row][1].column = 1
        cards[2][1], cards[self.row][1] = cards[self.row][1], cards[2][1]
        return

class Front(CardLocation):
  def __init__(self, row):
    super().__init__(row, 2)

  def can_move_left(self, card_group, cards):
    return True

  def can_move_right(self, card_group, cards):
    return False

  def can_move_up(self, card_group, cards):
    return normal_can_move_up(self, cards)

  def can_move_down(self, card_group, cards):
    return normal_can_move_down(self, cards)

  def move_left(self, card_group, cards):
    if not self.can_move_left(card_group, cards):
      raise Exception("can not move left")
    if cards[self.row][1] is not None:
      cards[self.row][2].column = 1
      cards[self.row][1], cards[self.row][2] = cards[self.row][2], cards[self.row][1]
    else:
      cards[self.row][2].column = 0
      cards[self.row][2].row = cards[self.row][2].source_row
      cards[cards[self.row][2].source_row][0], cards[self.row][2] = (cards[self.row][2],
        cards[cards[self.row][2].source_row][0])

  def check_left_should_move(self, cards):
    if cards[self.row][1] is not None:
      cards[self.row][1].column = 2
      cards[self.row][1], cards[self.row][2] = cards[self.row][2], cards[self.row][1]

  def move_up(self, card_group, cards):
    if not self.can_move_up(card_group, cards):
      raise Exception("can not move up")
    if cards[self.row - 1][2] is None:
      cards[self.row][2].row = self.row - 1
      cards[self.row - 1][2], cards[self.row][2] = cards[self.row][2], cards[self.row - 1][2]
      self.check_left_should_move(cards)
      return
    if cards[self.row - 1][1] is None:
      cards[self.row - 1][2].column = 1
      cards[self.row][2].column = 1
      cards[self.row][2].row = self.row - 1
      cards[self.row - 1][1], cards[self.row - 1][2] = cards[self.row - 1][2], cards[self.row - 1][1]
      cards[self.row - 1][2], cards[self.row][2] = cards[self.row][2], cards[self.row - 1][2]
      self.check_left_should_move(cards)
      return
    if self.row == 2:
      if cards[0][2] is None:
        cards[self.row][2].row = 0
        cards[self.row][2].column = 2
        cards[0][2], cards[self.row][2] = cards[self.row][2], cards[0][2]
        self.check_left_should_move(cards)
        return
      if cards[0][1] is None:
        cards[0][2].column = 1
        cards[self.row][2].row = 0
        cards[self.row][2].column = 2
        cards[0][2], cards[0][1] = cards[0][1], cards[0][2]
        cards[0][2], cards[self.row][2] = cards[self.row][2], cards[0][2]
        self.check_left_should_move(cards)
        return

  def move_down(self, card_group, cards):
    if not self.can_move_down(card_group, cards):
      raise Exception("can not move down")
    if cards[self.row + 1][2] is None:
      cards[self.row + 1][2], cards[self.row][2] = cards[self.row][2], cards[self.row + 1][2]
      self.check_left_should_move(cards)
      return
    if cards[self.row + 1][1] is None:
      cards[self.row + 1][1], cards[self.row + 1][2] = cards[self.row + 1][2], cards[self.row + 1][1]
      cards[self.row + 1][2], cards[self.row][2] = cards[self.row][2], cards[self.row + 1][2]
      self.check_left_should_move(cards)
      return
    if self.row == 0:
      if cards[2][2] is None:
        cards[self.row][2].row = 2
        cards[self.row][2].column = 2
        cards[2][2], cards[self.row][2] = cards[self.row][2], cards[2][2]
        self.check_left_should_move(cards)
        return
      if cards[2][1] is None:
        cards[2][2].column = 1
        cards[self.row][2].row = 2
        cards[self.row][2].column = 2
        cards[2][1], cards[2][2] = cards[2][2], cards[2][1]
        cards[2][2], cards[self.row][2] = cards[self.row][2], cards[2][2]
        self.check_left_should_move(cards)
