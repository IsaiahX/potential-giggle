import pygame
import map
from random import randint
pygame.init()


class MyTank(pygame.sprite.Sprite):
    map = None
    def __init__(self, Map,other = None,type_ = 'player',me = None):
        global map
        map = Map  # 将map引入类中
        if type_ == 'player':
            self.img = 'images/me.png'
        else:
            index = randint(1,2)
            self.img = 'images/enemy{0}.png'.format(str(index))          #随机生成一个数后，对路径格式化，相当于随机选择坦克图像
        pygame.sprite.Sprite.__init__(self)
        self.others = pygame.sprite.Group()     #创建一个精灵组，将除了自己以外的所有精灵全部装进来，因为坦克不能穿过其他任何东西，所以这样做能更方便于碰撞检测，来确定坦克是否触碰其他对象
        self.other_tanks = pygame.sprite.Group()    #创建一个精灵组，将除了自己以外的所有坦克全部装进来，这样便于判断自己发出的子弹是否击中敌人
        self.type = type_           #用于识别该类的实例是玩家控制的还是电脑控制的
        if other:
            for each in other:
                self.others.add(each)       #将其他坦克加进来
                self.other_tanks.add(each)  #将其他坦克放进来，用来检测是否被我方子弹射中
        for each in map.wallGroup:
            self.others.add(each)       #将其他墙壁加入进来
        if self.type == 'computer':
            self.other_tanks.add(me)
            self.others.add(me)

        self.image = pygame.image.load(self.img).convert_alpha()
        # 定义一个属性mask，该属性将用于下面更精准的碰撞检测中
        self.mask = pygame.mask.from_surface(self.image)
        # 获取我方坦克的矩形
        self.rect = self.image.get_rect()
        print(self.rect.width)
        # 随机设置我方坦克位置，判断我方坦克是否卡住墙壁，如果是，则重新设置位置
        firstRun = True
        while pygame.sprite.spritecollide(self, self.others, False) or firstRun:
            firstRun = False
            self.rect.left, self.rect.top = \
                randint(0, map.rect.width - self.rect.width), \
                randint(0, map.rect.height - self.rect.height)
        # 定义一个字典，用于储存各种方向坦克的角度
        self.angles = {'up': 0, 'left': 90, 'down': 180, 'right': 270}
        # 定义一个变量，这个变量可以记录我方坦克上一次执行的操作，默认为'up'，因为坦克一开始就朝向上方
        self.once = self.angles['up']
        # 定义一个变量，这个变量可以记录我方坦克当前执行的操作，默认为'up'，因为坦克一开始就朝向上方
        self.now = self.angles['up']
        # 定义一个变量，用于表示发出的子弹
        self.bulltes = pygame.sprite.Group()

    def turnTest(self):     #该方法可预判坦克转向后是否会嵌入墙内
        self.image = pygame.image.load(self.img).convert_alpha()
        self.image = pygame.transform.rotate(self.image, self.now).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)  # 更新坦克mask
        turnT = pygame.sprite.spritecollide(self, self.others, False, pygame.sprite.collide_mask)
        return turnT

    def turnBack(self):     #与turnTest方法配合使用，预判完毕后恢复原状
        self.image = pygame.image.load(self.img).convert_alpha() 
        self.image = pygame.transform.rotate(self.image,self.once).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)  # 还原坦克mask

    # 定义一个方法，这个方法下面会用于翻转坦克的朝向
    def turnTank(self):
        if self.once == self.now:
            return False
        if self.turnTest():
            self.turnBack()
            print('此时若转向，会卡住墙壁')
            return False
        return True

    # 定义一个方法，这个方法限制坦克不能穿过墙壁
    def crossWall(self, map):
        if pygame.sprite.spritecollide(self, self.others, False, pygame.sprite.collide_mask):
            if self.now == 0:  # 正在向上
                self.rect.top += 1
            if self.now == 180:  # 正在向下
                self.rect.top -= 1
            if self.now == 90:  # 正在向左
                self.rect.left += 1
            if self.now == 270:  # 正在向右
                self.rect.left -= 1

    # 向上走
    def up(self):
        self.now = self.angles['up']
        if self.turnTank():
            self.once = self.angles['up']
        if self.rect.top > 0:  # 判断我方坦克是否越界
            self.rect.top -= 1
        else:
            self.rect.top = 0
        print(self.rect)
        self.crossWall(map)

    # 向下走
    def down(self):
        self.now = self.angles['down']
        if self.turnTank():
            self.once = self.angles['down']
        if self.rect.top < map.rect.height - self.rect.height:  # 判断我方坦克是否越界
            self.rect.top += 1
        else:
            self.rect.top = map.rect.height - self.rect.height
        print(self.rect)
        self.crossWall(map)

    # 向左走
    def left(self):
        self.now = self.angles['left']
        if self.turnTank():
            self.once = self.angles['left']
        if self.rect.left > 0:  # 判断我方坦克是否越界
            self.rect.left -= 1
        else:
            self.rect.left = 0
        print(self.rect)
        self.crossWall(map)

    # 向右走
    def right(self):
        self.now = self.angles['right']
        if self.turnTank():
            self.once = self.angles['right']
        if self.rect.left <  map.rect.width - self.rect.height:  # 判断我方坦克是否越界
            self.rect.left += 1
        else:
            self.rect.left = map.rect.width - self.rect.height
        print(self.rect)
        self.crossWall(map)

    # 开火
    def fire(self):
        bullte = pygame.sprite.Sprite()
        bullte.image = pygame.image.load('images\炮弹\炮弹.png').convert_alpha()  # 生成一发子弹
        bullte.mask = pygame.mask.from_surface(bullte.image)        #设定子弹的非透明区域，用作碰撞检测
        bullte.rect = bullte.image.get_rect()  # 获取子弹矩形
        if self.once == 0:      #面朝上方
            bullte.rect.top, bullte.rect.left = \
                self.rect.top + 3, self.rect.width / 2 + self.rect.left - 5
            bullte.now = 0
        elif self.once == 90:   #面朝左边
            bullte.rect.top,bullte.rect.left = \
                self.rect.top + 16 , self.rect.left + 1
            bullte.now = 90
        elif self.once == 180:   #面朝下面       
            bullte.rect.top,bullte.rect.left = \
                self.rect.top + self.rect.height-1 , self.rect.left + 16
            bullte.now = 180
        elif self.once == 270:   #面朝右边
            bullte.rect.top,bullte.rect.left = \
                self.rect.top + 16 , self.rect.left + self.rect.width - 1
            bullte.now = 270
        self.bulltes.add(bullte)

    def fireMove(self):         #用于移动子弹
        for each in self.bulltes:
            if each.now == 0:  # 正在向上
                each.rect.top -= 6
            if each.now == 180:  # 正在向下
                each.rect.top += 6
            if each.now == 90:  # 正在向左
                each.rect.left -= 6
            if each.now == 270:  # 正在向右
                each.rect.left += 6

    def testCollide(self,screen):       #用于检测子弹是否与其他精灵发生碰撞,并作出相应处理
        # for each in self.bulltes：
        if pygame.sprite.groupcollide(self.bulltes,map.can_break_Group,True,True,pygame.sprite.collide_mask):
            # screen.blit(map.image,map.rect)
            # for each in collide:
                # del each
            map.wallGroup.draw(screen)

        if pygame.sprite.groupcollide(self.bulltes,map.cannot_break_Group,True,False,pygame.sprite.collide_mask):
            # screen.blit(map.image,map.rect)
            # map.wallGroup.draw(screen)
            pass
            
        pygame.sprite.groupcollide(self.bulltes,self.other_tanks,True,True,pygame.sprite.collide_mask)
        
