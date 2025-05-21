from enum import Enum

wight = 1280
height = 720
source_wight = 2560
source_height = 1440
wight_scale = wight / source_wight
height_scale = height / source_height

player_one_health_x = 1040
player_two_health_x = 1525
player_health_y = 160

player_one_mana_x = 935
player_two_mana_x = 1630
player_mana_y = 250

card_row_one_up_bord = 365 * wight_scale
card_row_two_up_bord = 698 * wight_scale
card_row_three_up_bord = 1031 * wight_scale
player_one_hand_card_one_x = 370 * height_scale
player_one_hand_card_one_y = card_row_one_up_bord
player_one_hand_card_two_x = 370 * height_scale
player_one_hand_card_two_y = card_row_two_up_bord
player_one_hand_card_three_x = 370 * height_scale
player_one_hand_card_three_y = card_row_three_up_bord
player_one_back_card_one_x = 740 * height_scale
player_one_back_card_one_y = card_row_one_up_bord
player_one_back_card_two_x = 740 * height_scale
player_one_back_card_two_y = card_row_two_up_bord
player_one_back_card_three_x = 740 * height_scale
player_one_back_card_three_y = card_row_three_up_bord
player_one_front_card_one_x = 1000 * height_scale
player_one_front_card_one_y = card_row_one_up_bord
player_one_front_card_two_x = 1000 * height_scale
player_one_front_card_two_y = card_row_two_up_bord
player_one_front_card_three_x = 1000 * height_scale
player_one_front_card_three_y = card_row_three_up_bord

player_two_front_card_one_x = 1275 * height_scale
player_two_front_card_one_y = card_row_one_up_bord
player_two_front_card_two_x = 1275 * height_scale
player_two_front_card_two_y = card_row_two_up_bord
player_two_front_card_three_x = 1275 * height_scale
player_two_front_card_three_y = card_row_three_up_bord
player_two_back_card_one_x = 1535 * height_scale
player_two_back_card_one_y = card_row_one_up_bord
player_two_back_card_two_x = 1535 * height_scale
player_two_back_card_two_y = card_row_two_up_bord
player_two_back_card_three_x = 1535 * height_scale
player_two_back_card_three_y = card_row_three_up_bord
player_two_hand_card_one_x = 1905 * height_scale
player_two_hand_card_one_y = card_row_one_up_bord
player_two_hand_card_two_x = 1905 * height_scale
player_two_hand_card_two_y = card_row_two_up_bord
player_two_hand_card_three_x = 1905 * height_scale
player_two_hand_card_three_y = card_row_three_up_bord

column_one_xs = [player_one_hand_card_one_x, player_one_back_card_one_x,
                 player_one_front_card_one_x, player_two_front_card_one_x,
                 player_two_back_card_one_x, player_two_hand_card_one_x]
column_two_xs = [player_one_hand_card_two_x, player_one_back_card_two_x,
              player_one_front_card_two_x, player_two_front_card_two_x,
              player_two_back_card_two_x, player_two_hand_card_two_x]
column_three_xs = [player_one_hand_card_three_x, player_one_back_card_three_x,
                player_one_front_card_three_x, player_two_front_card_three_x,
                player_two_back_card_three_x, player_two_hand_card_three_x]
column_xs = [column_one_xs, column_two_xs, column_three_xs]
row_ys = [card_row_one_up_bord, card_row_two_up_bord,
             card_row_three_up_bord]

health_font = None
mana_font = None
card_font = None
message_font = None
screen = None

def handle_wight(wight):
  return wight * wight_scale

def handle_height(height):
  return height * height_scale