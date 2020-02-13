import pygame
from random import *
pygame.init()
class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        map = randint(1,2)       #随机生成一个地图背景
        if map == 1:
            self.image = pygame.image.load('images/背景1.png').convert()
        elif map == 2:
            self.image = pygame.image.load('images/背景2.png').convert()
        
        self.rect = self.image.get_rect()       #获取地图背景矩形
        
        #生成随机样式墙壁
        self.wallGroup = pygame.sprite.Group()
        self.can_break_Group = pygame.sprite.Group()
        self.cannot_break_Group = pygame.sprite.Group()
        walls = []
        for num in range(30):       #默认生成45个墙壁
            # 随机选择生成的墙壁的状态
            wallMode = randint(1,2)      
            if wallMode == 1:
                # 生成散状墙壁
                # 随机选择生成的墙壁
                wallNum = randint(1,2)
                walls.append(pygame.sprite.Sprite())
                if wallNum == 1:
                    walls[-1].image = pygame.image.load('images/墙壁1.png').convert_alpha()
                    walls[-1].can_break = True       #设置墙壁可以被破坏
                    self.can_break_Group.add(walls[-1])
                elif wallNum == 2:
                    walls[-1].image = pygame.image.load('images/墙壁2.png').convert_alpha()
                    walls[-1].can_break = False      #设置墙壁不可被破坏
                    self.cannot_break_Group.add(walls[-1])
                # 定义一个属性mask，该属性将用于下面更精准的碰撞检测中
                walls[-1].mask = pygame.mask.from_surface(walls[-1].image)
                
                walls[-1].rect = walls[-1].image.get_rect()       #获取墙壁矩形
                
                # 随机设置墙壁位置
                walls[-1].rect.left = randint(0,self.rect.width - walls[-1].rect.width)
                walls[-1].rect.top = randint(0,self.rect.height - walls[-1].rect.height)
                
                #判断墙壁是否重合，如果重合，则重新选择墙壁位置
                while pygame.sprite.spritecollide(walls[-1],self.wallGroup,False):
                    # 重新随机设置墙壁位置
                    walls[-1].rect.left = randint(0,self.rect.width - walls[-1].rect.width)
                    walls[-1].rect.top = randint(0,self.rect.height - walls[-1].rect.height)
                                
                #将墙壁加入self.wallGroup中
                self.wallGroup.add(walls[-1])
            elif wallMode == 2:
                # 生成连体墙壁
                # 实例化一个Group类,用于后面判断连体墙壁是否与其他墙壁重叠
                lineGroup = pygame.sprite.Group()
                # 随机选择生成的墙壁
                wallNum = randint(1,2)
                # 随机确定连体的个数(1-5)
                lineNum = randint(1,5)
                # 随机确定连体方向  1是水平,2是竖直
                direction = randint(1,2)
                #向walls和lineGroup中添加墙壁
                # 定义一个布尔类型的变量firstRun,该变量可以使程序第一次执行到此处时进入循环，若没有此变量，将会直接跳过循环
                firstRun = True
                while pygame.sprite.groupcollide(lineGroup,self.wallGroup,True,False) or firstRun:
                    firstRun = False
                    for each in lineGroup:
                        lineGroup.remove(each)
                    for i in range(lineNum):        #以下的Sprite类的索引为 i+num
                        walls.append(pygame.sprite.Sprite())
                        if i == 0:
                            begin = i+num       #记录连体墙壁第一块的索引
                        if direction == 1:
                            # 生成墙壁
                            if wallNum ==1:
                                walls[-1].image = pygame.image.load('images/墙壁1.png').convert_alpha()
                                walls[-1].can_break = True
                            else:
                                walls[-1].image = pygame.image.load('images/墙壁2.png').convert_alpha()
                                walls[-1].can_break = False

                            # 定义一个属性mask，该属性将用于下面更精准的碰撞检测中
                            walls[-1].mask = pygame.mask.from_surface(walls[-1].image)
                            # 获取墙壁矩形
                            walls[-1].rect = walls[-1].image.get_rect()
                            # 设置墙壁位置
                            if i == 0:
                                # 连体墙壁的第一块位置随机
                                walls[-1].rect.left = randint(0,self.rect.width - walls[-1].rect.width * lineNum)
                                walls[-1].rect.top = randint(0,self.rect.height - walls[-1].rect.height)
                            else:
                                # 连体墙壁其它位置接着上一个墙壁的位置设定，水平向右延伸
                                walls[-1].rect.left = walls[-2].rect.left + walls[-2].rect.width
                                walls[-1].rect.top = walls[-2].rect.top
                            lineGroup.add(walls[-1])     #向self.wallGroup中添加墙壁   

                        if direction == 2:
                            # 生成墙壁
                            if wallNum ==1:
                                walls[-1].image = pygame.image.load('images/墙壁1.png').convert_alpha()
                                walls[-1].can_break = True                             
                            else:
                                walls[-1].image = pygame.image.load('images/墙壁2.png').convert_alpha()
                                walls[-1].can_break = False
                            # 定义一个属性mask，该属性将用于下面更精准的碰撞检测中
                            walls[-1].mask = pygame.mask.from_surface(walls[-1].image)                                
                            # 获取墙壁矩形
                            walls[-1].rect = walls[-1].image.get_rect()
                            # 设置墙壁位置
                            if i == 0:
                                # 连体墙壁的第一块位置随机
                                walls[-1].rect.left = randint(0,self.rect.width - walls[-1].rect.width)
                                walls[-1].rect.top = randint(0,self.rect.height - walls[-1].rect.height)
                            else:
                                # 连体墙壁其它位置接着上一个墙壁的位置设定，竖直向下延伸
                                walls[-1].rect.left = walls[-2].rect.left
                                walls[-1].rect.top = walls[-2].rect.top + walls[-2].rect.height
                            lineGroup.add(walls[-1])     #向self.wallGroup中添加墙壁

                #跳出循环后，说明此时生成的连体墙壁不与其他墙壁重合，可以添加进self.wallGroup中
                for each in lineGroup:
                    self.wallGroup.add(each)
                    if each.can_break:
                        self.can_break_Group.add(each)
                    else:
                        self.cannot_break_Group.add(each)
                # 相应地增加索引的值
                num += lineNum

    def draw(self,screen):      #将地图的墙壁绘制到地图上
        self.wallGroup.draw(screen)
