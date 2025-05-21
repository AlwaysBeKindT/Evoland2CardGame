import pygame

from card_group import Direction

def move_choose1(self, direction):
  if direction is None:
    raise ValueError("direction is None")
  if self.select is None:
    if direction == Direction.LEFT or direction == Direction.RIGHT:
      return
    if direction == Direction.UP and self.focus == self.game_cards[0][0]:
      return
    if direction == Direction.DOWN and self.focus == self.game_cards[2][0]:
      return
    if direction == Direction.UP:
      idx = 1 if self.focus == self.game_cards[1][0] else 2
      self.focus = self.game_cards[idx - 1][0]
      self.focus.handle_focus()
      self.row = idx - 1
      return
    if direction == Direction.DOWN:
      idx = 1 if self.focus == self.game_cards[1][0] else 0
      self.focus = self.game_cards[idx + 1][0]
      self.focus.handle_focus()
      self.row = idx + 1
      return

  if (direction == Direction.UP or direction == Direction.DOWN) and self.column == 0:
    return
  row = self.row
  column = self.column
  cards = self.game_cards
  if direction == Direction.LEFT:
    if column == 0:
      return
    cards[row][column - 1], cards[row][column] = cards[row][column], cards[row][column - 1]
    self.column -= 1
    if column == 2 and cards[row][2] is None:
      cards[self.source_row][0] = cards[row][1]
      cards[row][1] = None
      self.column -= 1
      self.row = self.source_row
  elif direction == Direction.RIGHT:
    if column == 2:
      return
    if column == 0:
      self.source_row = row
    cards[row][column + 1], cards[row][column] = cards[row][column], cards[row][column + 1]
    self.column += 1
    if column == 0 and cards[row][2] is None:
      cards[row][2] = cards[row][1]
      cards[row][1] = None
      self.column += 1
  elif direction == Direction.UP:
    if row == 0:
      return
    if cards[row - 1][column] is None:
      cards[row - 1][column], cards[row][column] = cards[row][column], cards[row - 1][column]
      self.row -= 1
    else:
      if row == 1 and column == 1:
        return
      if row == 2 and column == 1 and cards[row - 2][column] is not None:
        return
      if column == 2 and cards[row - 1][column - 1] is None:
        cards[row - 1][column - 1], cards[row - 1][column] = cards[row - 1][column], cards[row - 1][column - 1]
        cards[row - 1][column], cards[row][column] = cards[row][column], cards[row - 1][column]
        self.row -= 1
      elif row == 2 and cards[row - 2][column] is None:
        cards[row - 2][column], cards[row][column] = cards[row][column], cards[row - 2][column]
        self.row -= 2
      elif row == 2 and cards[row - 2][column - 1] is None:
        cards[row - 2][column - 1], cards[row - 2][column] = cards[row - 2][column], cards[row - 2][column - 1]
        cards[row - 2][column], cards[row][column] = cards[row][column], cards[row - 2][column]
        self.row -= 2
  elif direction == Direction.DOWN:
    if row == 2:
      return
    if cards[row + 1][column] is None:
      cards[row + 1][column], cards[row][column] = cards[row][column], cards[row + 1][column]
      self.row += 1
    else:
      if row == 1 and column == 1:
        return
      if row == 0 and column == 1 and cards[row + 2][column] is not None:
        return
      if column == 2 and cards[row + 1][column - 1] is None:
        cards[row + 1][column - 1], cards[row + 1][column] = cards[row + 1][column], cards[row + 1][column - 1]
        cards[row + 1][column], cards[row][column] = cards[row][column], cards[row + 1][column]
        self.row += 1
      elif row == 0 and cards[row + 2][column] is None:
        cards[row + 2][column], cards[row][column] = cards[row][column], cards[row + 2][column]
        self.row += 2
      elif row == 0 and cards[row + 2][column - 1] is None:
        cards[row + 2][column - 1], cards[row + 2][column] = cards[row + 2][column], cards[row + 2][column - 1]
        cards[row + 2][column], cards[row][column] = cards[row][column], cards[row + 2][column]
        self.row += 2
  for row in range(3):
    for column in range(3):
      card = cards[row][column]
      if card is not None:
        card.update_row_column(row, column)




def add_border(surface, border_color, border_width=2):
  """在原图表面直接绘制边框"""
  w, h = surface.get_size()
  bordered_surface = surface.copy()
  # 绘制四个边的矩形
  pygame.draw.rect(bordered_surface, border_color, (0, 0, w, border_width))  # 上边
  pygame.draw.rect(bordered_surface, border_color, (0, h - border_width, w, border_width))  # 下边
  pygame.draw.rect(bordered_surface, border_color, (0, 0, border_width, h))  # 左边
  pygame.draw.rect(bordered_surface, border_color, (w - border_width, 0, border_width, h))  # 右边
  return bordered_surface
