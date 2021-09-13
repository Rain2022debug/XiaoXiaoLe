import os
import sys
import time
import pygame
import random
from pygame.locals import *
from config import *
from typing import List

# 拼图精灵类
class gameSprite(pygame.sprite.Sprite):
    def __init__(self,img_path,size,position,downlen):
        pygame.sprite.Sprite.__init__(self)
        self.img=pygame.image.load(img_path)
        self.image = pygame.transform.smoothscale(self.img, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.rect.top+=downlen
        self.downlen = downlen
        self.target_x = position[0]
        self.target_y = position[1] + downlen
        self.type=img_path.split('/')[-1].split('.')[0]
        self.fixed=True
        self.speed_x=10
        self.speed_y=10
        self.direction='down'
    '''获取坐标'''

    def getPosition(self):
        return self.rect.left, self.rect.top

    '''设置坐标'''

    def setPosition(self, position):
        self.rect.left, self.rect.top = position



            # 窗口无响应是因为没有任何注册在窗口上的事件
            # 为当前窗口增加事件
            # 利用pygame注册事件，其返回值是一个列表，
            # 存放当前注册时获取的所有事件


class xiaoxiaole_game:
    def __init__(self,screen,sounds,fonts,flowers):
        self.info='消消乐小游戏'
        self.screen =screen
        self.sounds=sounds
        self.fonts=fonts
        self.flowers_imgs=flowers
        self.same_flowers=[]
        self.reset()


    def start(self):
        #遍历整个游戏界面更新位置
        overall_moving=True
        #游戏变量
        flower_selected_xy=None
        #游戏主循环
        while True:
            #手动退出游戏
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONUP:
                    position=pygame.mouse.get_pos()
                    flower_selected_xy=self.check_selected(position)

            # if self.check_column_sprites()!=-1:
            #     for x in range(self.check_column_sprites()+1,NUMBGRID):
            #         for y in range(NUMBGRID):
            #             self.get_flower_by_pos(x, y)

            self.screen.fill((135, 206, 235))
            self.draw_grids()
            self.flowers_group.draw(self.screen)
            #有一个方块被选中时
            if flower_selected_xy and self.get_flower_by_pos(*flower_selected_xy):
                #高亮
                pygame.draw.rect(self.screen, (255, 0, 255), self.get_flower_by_pos(*flower_selected_xy), 1)
                #每一次计算都要清空上次的列表坐标
                self.same_flowers=[flower_selected_xy]
                #找出所有可消除方块并移除
                self.is_match(flower_selected_xy[0],flower_selected_xy[1])
                self.score+=len(self.same_flowers)
                if self.same_flowers:
                    self.remove_matched()
                flower_selected_xy=None
            self.draw_score()
            pygame.display.update()

    # 初始化游戏
    def reset(self):
        # 初始化游戏地图各个元素
        self.all_flowers = []
        self.flowers_group = pygame.sprite.Group()
        for x in range(NUMBGRID):
            self.all_flowers.append([])
            for y in range(NUMBGRID):
                fl = gameSprite(img_path=random.choice(self.flowers_imgs), size=(GRIDSIZE, GRIDSIZE),
                                position=[XMARGIN + x * GRIDSIZE, YMARGIN + y * GRIDSIZE - NUMBGRID * GRIDSIZE],
                                downlen=NUMBGRID * GRIDSIZE)
                self.all_flowers[x].append(fl)
                self.flowers_group.add(fl)
            # 得分
            self.score = 0
            # 奖励
            self.reward = 10

    #判断一列是否清空，如果是则需要拼接
    def check_column_sprites(self):
        for x in range(NUMBGRID):
            count=0
            for y in range(NUMBGRID):
                if not self.get_flower_by_pos(x,y).fixed:
                    count+=1
            if count==NUMBGRID:
                return x
        return -1


    def get_flower_by_pos(self,x,y):
        return self.all_flowers[x][y]

    def draw_score(self):
        score_render=self.fonts.render('SCORE: '+str(self.score),1,(85,65,0))
        rect=score_render.get_rect()
        rect.left,rect.top=(10,6)
        self.screen.blit(score_render,rect)

    #判断选中方块的行列号
    def check_selected(self,position):
        for x in range(NUMBGRID):
            for y in range(NUMBGRID):
                if self.get_flower_by_pos(x,y):
                    if self.get_flower_by_pos(x,y).rect.collidepoint(*position):
                        return [x,y]
        return None
    #从传入的坐标方块开始，搜寻周围是否有相同的连接的方块，将坐标全部加入列表
    #直接向外扩张会导致来回死循环
    def is_match(self,start_x,start_y):
        direction=[[1,0],[-1,0],[0,1],[0,-1]]
        for d in direction:
            tp=[start_x+d[0],start_y+d[1]]
            if tp in self.same_flowers:
                continue
            if tp[0]>=NUMBGRID or tp[0]<0 or tp[1]>=NUMBGRID or tp[1]<0:
                continue
            if self.get_flower_by_pos(start_x,start_y) and self.get_flower_by_pos(tp[0],tp[1]):
                    if self.get_flower_by_pos(start_x,start_y).type == self.get_flower_by_pos(tp[0],tp[1]).type:
                        self.same_flowers.append(tp)
                        self.is_match(tp[0],tp[1])


    #移除全部(同时向下移动相邻上方方块），最后判断是否有列空缺
    def remove_matched(self):
        col_number=[i[0] for i in self.same_flowers]
        col_number=list(set(col_number))
        dic={}
        for i in col_number:
            tl=[]
            for pos in self.same_flowers:
                self.flowers_group.remove(self.get_flower_by_pos(pos[0], pos[1]))
                self.all_flowers[pos[0]][pos[1]] = None
                if pos[0]==i:
                    tl.append(pos[1])
            dic[i]=tl
        for col in dic.keys():
            for j in range(max(dic[col])-1,-1,-1):
                if j in dic[col]:
                    continue
                else:
                    count=0
                    for k in dic[col]:
                       if j-k <0:
                           count+=1
                    if self.get_flower_by_pos(col, j):
                        f= self.get_flower_by_pos(col, j)
                        self.all_flowers[col][j] = None
                        f.rect.top+=GRIDSIZE*count
                        self.all_flowers[col][j+count]=f


    #绘制界面网格
    def draw_grids(self):
        for x in range(NUMBGRID):
            for y in range(NUMBGRID):
                rect=pygame.Rect(XMARGIN+x*GRIDSIZE,YMARGIN+y*GRIDSIZE,GRIDSIZE,GRIDSIZE)
                pygame.draw.rect(self.screen,(0, 0, 255),rect,1)

    def draw_add_score(self, add_score):
        score_render = self.fonts.render('+' + str(add_score), 1, (255, 100, 100))
        rect = score_render.get_rect()
        rect.left, rect.top = (250, 250)
        self.screen.blit(score_render, rect)

    def __repr__(self):
        return self.info








