def sale_card(card_group, cards):
  cards[card_group.select.row][card_group.select.column] = None
  card_group.select = None

def normal_can_move_up(self, card_group, cards):
  if self.row == 0:
    return False
  front_column = card_group.front_column
  is_row_0_any_none = cards[0][1] is None or cards[0][front_column] is None
  if self.row == 1:
    return is_row_0_any_none
  return is_row_0_any_none or cards[1][1] is None or cards[1][front_column]

def normal_can_move_down(self, card_group, cards):
  if self.row == 2:
    return False
  front_column = card_group.front_column
  is_row_2_any_none = cards[2][1] is None or cards[2][front_column] is None
  if self.row == 1:
    return is_row_2_any_none
  return cards[1][1] is None or cards[1][front_column] is None or is_row_2_any_none

def check_back_should_move_front(row, front_column, cards):
  if cards[row][1] is not None:
    cards[row][1].column = front_column
    cards[row][1], cards[row][front_column] = cards[row][front_column], cards[row][1]

class CardLocation:
  def __init__(self, row):
    self.row = row

  def get_column(self, card_group):
    raise Exception("Not implemented")

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
    super().__init__(row)

  def get_column(self, card_group):
    return 0 if card_group.is_player_one else 2

  def can_move_up(self, card_group, cards):
    return False

  def can_move_down(self, card_group, cards):
    return False

  def can_play_card(self, card_group, cards):
    # 当前卡片被选中且是手牌区的卡片
    current_card = cards[self.row][card_group.hand_column]
    if card_group.select is None or card_group.select != current_card:
      return False
    # 检查所有行、右侧两列区域是否有空位
    return any(cards[row][col] is None for row in range(3) for col in [1, 2])

  def can_move_left(self, card_group, cards):
    return True if card_group.is_player_one else self.can_play_card(card_group, cards)

  def can_move_right(self, card_group, cards):
    return self.can_play_card(card_group, cards) if card_group.is_player_one else True

  def play_card(self, card_group, cards):
    hand_column = card_group.hand_column
    if card_group.select is None or card_group.select != cards[self.row][hand_column]:
      raise ValueError("select and focus not equal!")
    front_column = card_group.front_column
    if cards[self.row][front_column] is None:
      cards[self.row][hand_column].source_row = self.row
      cards[self.row][hand_column].column = front_column
      cards[self.row][front_column], cards[self.row][hand_column] = cards[self.row][hand_column], cards[self.row][
        front_column]
      return
    if cards[self.row][1] is None:
      cards[self.row][hand_column].source_row = self.row
      cards[self.row][hand_column].column = 1
      cards[self.row][1], cards[self.row][hand_column] = cards[self.row][hand_column], cards[self.row][1]
      return
    for row in range(3):
      if cards[row][front_column] is None:
        cards[self.row][hand_column].source_row = self.row
        cards[self.row][hand_column].column = front_column
        cards[self.row][hand_column].row = row
        cards[row][front_column], cards[self.row][hand_column] = cards[self.row][hand_column], cards[row][front_column]
        return
      if cards[row][1] is None:
        cards[self.row][hand_column].source_row = self.row
        cards[self.row][hand_column].column = 1
        cards[self.row][hand_column].row = row
        cards[row][1], cards[self.row][hand_column] = cards[self.row][hand_column], cards[row][1]
        return

  def move_right(self, card_group, cards):
    if not self.can_move_right(card_group, cards):
      raise Exception("can not move right")
    if card_group.is_player_one:
      self.play_card(card_group, cards)
    else:
      sale_card(card_group, cards)

  def move_left(self, card_group, cards):
    if not self.can_move_left(card_group, cards):
      raise Exception("can not move left")
    if card_group.is_player_one:
      sale_card(card_group, cards)
    else:
      self.play_card(card_group, cards)

class Back(CardLocation):
  def __init__(self, row):
    super().__init__(row)

  def get_column(self, card_group):
    return 1

  def can_move_left(self, card_group, cards):
    return True

  def can_move_right(self, card_group, cards):
    return True

  def can_move_up(self, card_group, cards):
    return normal_can_move_up(self, card_group, cards)

  def can_move_down(self, card_group, cards):
    return normal_can_move_down(self, card_group, cards)

  def card_return_hand(self, card_group, cards):
    hand_column = card_group.hand_column
    cards[self.row][1].row = cards[self.row][1].source_row
    cards[self.row][1].column = hand_column
    cards[cards[self.row][1].source_row][hand_column], cards[self.row][1] = cards[self.row][1], \
      cards[cards[self.row][1].source_row][hand_column]

  def exchange_with_front(self, card_group, cards):
    front_column = card_group.front_column
    cards[self.row][1].column = front_column
    cards[self.row][front_column], cards[self.row][1] = cards[self.row][1], cards[self.row][front_column]

  def move_left(self, card_group, cards):
    if card_group.is_player_one:
      self.card_return_hand(card_group, cards)
    else:
      self.exchange_with_front(card_group, cards)

  def move_right(self, card_group, cards):
    if card_group.is_player_one:
      self.exchange_with_front(card_group, cards)
    else:
      self.card_return_hand(card_group, cards)

  def back_move_up_or_down_one_row(self, cards, row, front_column):
    if cards[row][front_column] is None:
      cards[self.row][1].column = front_column
      cards[self.row][1].row = row
      cards[row][front_column], cards[self.row][1] = cards[self.row][1], cards[row][front_column]
      return True
    if cards[row][1] is None:
      cards[self.row][1].column = 1
      cards[self.row][1].row = row
      cards[row][1], cards[self.row][1] = cards[self.row][1], cards[row][1]
      return True
    return False

  def move_up_or_down(self, card_group, cards, row_func, head_row, back_row):
    front_column = card_group.front_column
    cal_row = row_func(self.row)
    if self.back_move_up_or_down_one_row(cards, cal_row, front_column):
      return
    if self.row == back_row:
      self.back_move_up_or_down_one_row(cards, head_row, front_column)

  def move_up(self, card_group, cards):
    if not self.can_move_up(card_group, cards):
      raise Exception("can not move up")
    self.move_up_or_down(card_group, cards, lambda row: row - 1, 0, 2)

  def move_down(self, card_group, cards):
    if not self.can_move_down(card_group, cards):
      raise Exception("can not move down")
    self.move_up_or_down(card_group, cards, lambda row: row + 1, 2, 0)

class Front(CardLocation):
  def __init__(self, row):
    super().__init__(row)

  def get_column(self, card_group):
    return 2 if card_group.is_player_one else 0

  def can_move_left(self, card_group, cards):
    return card_group.is_player_one

  def can_move_right(self, card_group, cards):
    return not card_group.is_player_one

  def can_move_up(self, card_group, cards):
    return normal_can_move_up(self, card_group, cards)

  def can_move_down(self, card_group, cards):
    return normal_can_move_down(self, card_group, cards)

  def move_back_or_return_hand(self, card_group, cards):
    self_row = self.row
    self_column = self.get_column(card_group)
    if cards[self_row][1] is not None:
      cards[self_row][self_column].column = 1
      cards[self_row][1], cards[self_row][self_column] = cards[self_row][self_column], cards[self_row][1]
    else:
      hand_column = card_group.hand_column
      cards[self_row][self_column].column = hand_column
      cards[self_row][self_column].row = cards[self_row][self_column].source_row
      cards[cards[self_row][self_column].source_row][hand_column], cards[self_row][self_column] = (cards[self_row][self_column],
        cards[cards[self_row][self_column].source_row][hand_column])

  def move_left(self, card_group, cards):
    if not self.can_move_left(card_group, cards):
      raise Exception("can not move left")
    if card_group.is_player_one:
      self.move_back_or_return_hand(card_group, cards)
    else:
      raise Exception("can not move left")

  def move_right(self, card_group, cards):
    if not self.can_move_right(card_group, cards):
      raise Exception("can not move right")
    if card_group.is_player_one:
      raise Exception("can not move right")
    else:
      self.move_back_or_return_hand(card_group, cards)

  def front_move_up_or_down_one_row(self, card_group, cards, row, front_column):
    if cards[row][front_column] is None:
      cards[self.row][front_column].column = front_column
      cards[self.row][front_column].row = row
      cards[row][front_column], cards[self.row][front_column] = cards[self.row][front_column], cards[row][front_column]
      check_back_should_move_front(self.row, card_group.front_column, cards)
      return True
    if cards[row][1] is None:
      cards[row][front_column].column = 1
      cards[self.row][front_column].row = row
      cards[row][1], cards[row][front_column] = cards[row][front_column], cards[row][1]
      cards[row][front_column], cards[self.row][front_column] = cards[self.row][front_column], cards[row][front_column]
      check_back_should_move_front(self.row, card_group.front_column, cards)
      return True
    return False

  def move_up_or_down(self, card_group, cards, row_func, head_row, back_row):
    front_col = card_group.front_column
    cal_rwo = row_func(self.row)
    if self.front_move_up_or_down_one_row(card_group, cards, cal_rwo, front_col):
      return
    if self.row == back_row:
      self.front_move_up_or_down_one_row(card_group, cards, head_row, front_col)

  def move_up(self, card_group, cards):
    if not self.can_move_up(card_group, cards):
      raise Exception("can not move up")
    self.move_up_or_down(card_group, cards, lambda row: row - 1, 0, 2)

  def move_down(self, card_group, cards):
    if not self.can_move_down(card_group, cards):
      raise Exception("can not move down")
    self.move_up_or_down(card_group, cards, lambda row: row + 1, 2, 0)
