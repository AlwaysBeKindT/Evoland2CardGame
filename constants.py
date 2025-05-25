wight = 2400
height = 1300
# wight = 1280
# height = 720
source_wight = 2560
source_height = 1440
wight_scale = wight / source_wight
height_scale = height / source_height

player_one_health_x = 1010
player_two_health_x = 1560
player_health_y = 180

player_one_mana_x = 880
player_two_mana_x = 1685
player_mana_y = 275

mid_width = [0, 370, 260, 273, 260, 370]
start_x = 390
column_xs = [start_x + sum(mid_width[:idx]) for idx in range(1, 7)]
column_xs = [int(x * wight_scale) for x in column_xs]
start_y = 370
mid_height = 333
row_ys = [start_y, start_y + mid_height, start_y + mid_height * 2]
row_ys = [int(y * height_scale) for y in row_ys]

health_font = None
mana_font = None
card_font = None
message_font = None
screen = None

player_health = 20

def handle_wight(wight_arg):
  return wight_arg * wight_scale

def handle_height(height_arg):
  return height_arg * height_scale
