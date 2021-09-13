import os
import pygame
from game_window import *
from config import *

# 游戏主程序
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('消消乐')
    #加载背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(ROOTDIR,'audios\\bgm.mp3'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    #加载音效
    sounds={}
    sounds['mismatch']=pygame.mixer.Sound(os.path.join(ROOTDIR,'audios/mismatch.wav'))
    sounds['match']=[]
    for temp1 in range(6):
        sounds['match'].append(pygame.mixer.Sound(os.path.join(ROOTDIR,'audios/match%s.wav'%temp1)))
    #加载字体
    font=pygame.font.Font(os.path.join(ROOTDIR,'font/font.TTF'),25)
    #图片加载
    flower_imgs = []
    for i in range(1, 7):
        flower_imgs.append(os.path.join(ROOTDIR, 'img/flower%s.png' % i))
    #主循环 运行游戏
    game=xiaoxiaole_game(screen,sounds,font,flower_imgs)
    while True:
        score=game.start()
        flag=False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                    flag = True
            if flag:
                break
            screen.fill((135, 206, 235))
            text0 = 'Final score: %s' % score
            text_render = font.render(text0, 1, (85, 65, 0))
            rect = text_render.get_rect()
            rect.left, rect.top = (212, 150)
            screen.blit(text_render, rect)
            pygame.display.update()
        game.reset()
if __name__ == '__main__':
    main()




