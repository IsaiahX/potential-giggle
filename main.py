import pygame,random,map,my_tank,enemy
from pygame.locals import *

# 初始化
pygame.init()
pygame.mixer.init()

# 设置游戏窗口大小
bg_size = width,height = 750,750
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('|----欢迎来到坦克大战----|')

# 生成地图
gameMap = map.Map()

# 修改窗口大小
bg_size = gameMap.rect.width, gameMap.rect.height
screen = pygame.display.set_mode(bg_size)

#载入地图
screen.blit(gameMap.image,(0,0))

# 载入游戏音乐
pygame.mixer.music.load('sound\Overworld Night - Scott Lloyd Shelly.mp3')
pygame.mixer.music.set_volume(0.1)
bullte_sound = pygame.mixer.Sound('sound\爆炸.wav')
bullte_sound.set_volume(0.3)
fire_sound = pygame.mixer.Sound('sound\发射子弹.wav')
fire_sound.set_volume(0.2)

def main():
    #创建一个变量isFire,用来记录我方坦克是否发出子弹,默认不发出
    isFire = False
    canFire = True

    # 创建敌对坦克组
    enemies = pygame.sprite.Group()

    # 播放背景音乐
    pygame.mixer.music.play(-1)

    # 生成游戏时钟
    clock = pygame.time.Clock()

    # 生成我方坦克 
    me = my_tank.MyTank(gameMap,enemies)

    # 生成敌方坦克
    for num in range(4):
        enemy1 = enemy.Enemy(gameMap,other = enemies , me = me)
        enemies.add(enemy1)
        me.others.add(enemy1)       
        me.other_tanks.add(enemy1)

    # me = my_tank.MyTank(gameMap,enemies)        

    fireTime = 100      #变量fireTime用于每次开火的延迟

    while True:
        if not canFire:         #当处于冷却时间时，加载冷却时间
            fireTime -= 1        
        if not fireTime % 100:       #每90帧激活一次发射子弹的机会
            canFire = True
        screen.blit(gameMap.image,(0,0))    #绘制游戏地图背景
        gameMap.draw(screen)        #绘制墙壁

        # 移动敌方坦克
        for each in enemies:
            each.findWay(me)
            screen.blit(each.image,each.rect)

        # 检测键盘操作
        keyList = pygame.key.get_pressed()
        if keyList[K_w] or keyList[K_UP]:
            me.up()         # 移动我方坦克

        elif keyList[K_s] or keyList[K_DOWN]:
            me.down()       #移动我方坦克

        elif keyList[K_a] or keyList[K_LEFT]:
            me.left()       # 移动我方坦克

        elif keyList[K_d] or keyList[K_RIGHT]:
            me.right()      #移动我方坦克 

        if canFire:         #检测子弹发射冷却时间有没有过
            if keyList[K_SPACE]:
                me.fire()       #发射子弹
                fire_sound.play()     #播放音效
                isFire = True
                canFire = False     #重新等待冷却时间

        # 更新屏幕
        screen.blit(me.image,me.rect)       #绘制我方坦克
        enemies.draw(screen)       #绘制敌方坦克

        if isFire:      #让子弹飞起来
            me.fireMove()
            me.testCollide(screen)        #检测子弹有没有撞击墙壁
            # for each in me.bulltes:     #绘制子弹
            #     screen.blit(each.image,each.rect)
            me.bulltes.draw(screen)
        if fireTime == 0:
            fireTime = 100
        pygame.display.flip()
        clock.tick(100)

        # 检测用户是否退出
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()       # 更"友善"地退出
                exit()

if __name__ == '__main__':
    main()
