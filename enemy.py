import pygame
import my_tank
from random import randint
pygame.init()

firstFind = True

class Enemy(my_tank.MyTank):
    def __init__(self,map,other = None,me = None):
        my_tank.MyTank.__init__(self,map,other,'computer',me)
        # index = randint(1,2)
        # img = 'images/enemy{0}.png'.format(str(index))          #随机生成一个数后，对路径格式化，相当于随机选择坦克图像
        # self.image= pygame.image.load(img).convert_alpha()      #加载图像
        # self.mask = pygame.mask.from_surface(self.image)        #更新mask属性
        # 随机设置坦克位置，判断坦克是否卡住墙壁，如果是，则重新设置位置
        firstRun = True
        self.order = None
        self.others.remove(self)
        self.testWay = pygame.sprite.Sprite()       #定义一个精灵，用于探测路上有无障碍，并引导坦克进行移动
        while pygame.sprite.spritecollide(self, self.others, False) or firstRun:
            firstRun = False
            self.rect.left, self.rect.top = \
                randint(0, map.rect.width - self.rect.width), \
                randint(0, map.rect.height - self.rect.height)

    def findWay(self,me):      #此函数可以帮助坦克有目的性地、智能地运动，这是整个程序的核心与亮点
        # pass
        global firstFind
        if firstFind:
            self.order = randint(1,2)
            firstFind = False
        if self.order == 1:
            if me.rect.left - self.rect.left < -30:         #玩家操控坦克在电脑操控坦克的左边
                self.left()
            elif me.rect.left-self.rect.left > 30:          #玩家操控坦克在电脑操控坦克的右边
                self.right()
            elif me.rect.top - self.rect.top < -30:           #玩家操控坦克在电脑操控坦克的上边
                self.up()
            elif me.rect.top - self.rect.top > 30:           #玩家操控坦克在电脑操控坦克的下边
                self.down()
        elif self.order == 2:
            if me.rect.top - self.rect.top < -30:         #玩家操控坦克在电脑操控坦克的左边
                self.up()
            elif me.rect.top-self.rect.top > 30:          #玩家操控坦克在电脑操控坦克的右边
                self.down()
            elif me.rect.left - self.rect.left < -30:           #玩家操控坦克在电脑操控坦克的上边
                self.left()
            elif me.rect.left - self.rect.left > 30:           #玩家操控坦克在电脑操控坦克的下边
                self.right()            
