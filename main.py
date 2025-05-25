import pygame

import constants
from constants import wight, height
from player_sprites import Player, update_screen

def show_msg_and_wait_input(text, color=(255, 255, 255)):
  show_text = constants.message_font.render(text, True, color)
  start_text_rect = show_text.get_rect()
  start_text_rect.center = (wight // 2, height // 2)
  screen.blit(show_text, start_text_rect)
  pygame.display.update()
  wait_input = True
  while wait_input:
    for event in pygame.event.get():
      # 判断用户是否点击了关闭按钮
      if event.type == pygame.QUIT:
        print("退出游戏...")
        pygame.quit()
        exit()
      # 判断用户是否按下了键盘上的Enter键或空格键
      if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
        wait_input = False
        break

if __name__ == '__main__':
  pygame.init()

  constants.health_font = pygame.font.SysFont("simsun", 75)
  constants.mana_font = pygame.font.SysFont("simsun", 45)
  constants.message_font = pygame.font.SysFont("simsun", 36)
  constants.card_font = pygame.font.SysFont("simsun", int(36 * constants.wight_scale))

  screen = pygame.display.set_mode((wight, height), pygame.SRCALPHA)
  constants.screen = screen
  image = pygame.image.load("images/background.png")
  bg = pygame.transform.scale(image, (wight, height))
  screen.blit(bg, (0, 0))
  pygame.mixer.music.load("music/background_music.mp3")
  pygame.mixer.music.set_volume(0.3)
  pygame.mixer.music.play(-1)

  # 等待开始
  show_msg_and_wait_input("按回车或空格开始游戏")
  print("开始游戏...")

  screen.blit(bg, (0, 0))
  pygame.display.update()
  clock = pygame.time.Clock()
  player_one = Player(constants.player_health, True)
  player_two = Player(constants.player_health, False)

  pygame.time.wait(100)
  run = True
  while run:
    player_one.update()
    player_one.draw(screen)
    player_two.update()
    player_two.draw(screen)
    pygame.display.update()

    def draw_bg():
      screen.blit(bg, (0, 0))

    while player_one.health > 0 and player_two.health > 0:
      player_one.active(screen, player_two, draw_bg, clock)
      player_two, player_one = player_one, player_two

    update_screen(player_one, player_two, draw_bg, screen)

    pygame.time.wait(1000)
    if player_two.is_player_one:
      player_two, player_one = player_one, player_two
    winner = "玩家1" if player_one.health > 0 else "玩家2"
    show_msg_and_wait_input(winner + "赢了，按回车或空格重新来一局！")
    print("继续游戏...")

    player_one = Player(constants.player_health, True)
    player_two = Player(constants.player_health, False)

  print("退出游戏...")
  pygame.quit()
