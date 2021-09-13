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

    #加载字体
    font=pygame.font.Font(os.path.join(ROOTDIR,'font/font.TTF'),25)
    #图片加载
    flower_imgs = []
    for i in range(1, 7):
        flower_imgs.append(os.path.join(ROOTDIR, 'img/flower%s.png' % i))
    #主循环 运行游戏
    game=xiaoxiaole_game(screen,font,flower_imgs)
    score = game.start()
if __name__ == '__main__':
    main()




