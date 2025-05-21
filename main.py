import pygame

import constants
from constants import wight, height
from player_sprites import Player

def wait_start():
  global event
  start_text = constants.message_font.render("按Enter开始", True, (255, 255, 255))
  start_text_rect = start_text.get_rect()
  start_text_rect.center = (wight // 2, height // 2)
  screen.blit(start_text, start_text_rect)
  pygame.display.update()
  start_wait_input = True
  while start_wait_input:
    for event in pygame.event.get():
      # 判断用户是否点击了关闭按钮
      if event.type == pygame.QUIT:
        print("退出游戏...")
        pygame.quit()
        exit()
      # 判断用户是否按下了键盘上的Enter键
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        print("开始游戏...")
        start_wait_input = False
        break

if __name__ == '__main__':
  pygame.init()

  constants.health_font = pygame.font.SysFont("simsun", 75)
  constants.mana_font = pygame.font.SysFont("simsun", 45)
  constants.message_font = pygame.font.SysFont("simsun", 36)
  constants.card_font = pygame.font.SysFont("simsun", int(36 * constants.wight_scale))

  screen = pygame.display.set_mode((wight, height), pygame.SRCALPHA)
  constants.screen = screen
  image = pygame.image.load("./images/background-e2cg.png")
  bg = pygame.transform.scale(image, (wight, height))
  screen.blit(bg, (0, 0))
  pygame.mixer.music.load("./music/background_music.mp3")
  pygame.mixer.music.set_volume(0.3)
  pygame.mixer.music.play(-1)

  # 等待开始
  wait_start()

  screen.blit(bg, (0, 0))
  pygame.display.update()
  clock = pygame.time.Clock()
  player_one = Player(20, True)
  player_two = Player(20, False)

  run = True
  while run:
    player_one.update()
    player_one.draw(screen)
    player_two.update()
    player_two.draw(screen)
    pygame.display.update()

    def draw_bg():
      screen.blit(bg, (0, 0))
    player_one.active(screen, player_two, draw_bg, clock)

    # 事件监听
    for event in pygame.event.get():
      # 判断用户是否点击了关闭按钮
      if event.type == pygame.QUIT:
        run = False
        break
    winner = "玩家1" if player_one.health > 0 else "玩家2"
    end_text = constants.mana_font.render(winner + "赢了，按Enter重新来一局！", True, (255, 255, 255))
    end_text_rect = end_text.get_rect()
    end_text_rect.center = (wight // 2, height // 2)
    screen.blit(end_text, end_text_rect)
    pygame.display.update()
    game_wait_input = True
    while game_wait_input:
      for event in pygame.event.get():
        # 判断用户是否点击了关闭按钮
        if event.type == pygame.QUIT:
          print("退出游戏...")
          pygame.quit()
          exit()
        # 判断用户是否按下了键盘上的Enter键
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
          print("继续游戏...")
          game_wait_input = False
          break
    player_one = Player(20, True)
    player_two = Player(20, False)

  print("退出游戏...")
  pygame.quit()