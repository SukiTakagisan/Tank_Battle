import pygame,time,random
_display = pygame.display
#设置长宽高
SCREEN_WIDTH = 800
SCREEN_HIGHT = 500
#设置颜色
BLACK_COLOR = pygame.Color(0,0,0)
COLOR_RED = pygame.Color(255,0,0)
#继承精灵类
class BaseIteam(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
#主逻辑类
class MainGame():
    window = None
    #创建我方坦克
    TANK_PI = None
    #敌方坦克列表
    ENME_TANK_LIST = []
    #敌方坦克数量
    ENME_TANK_COUNT = 5
    #我方坦克子弹列表
    TANK_PI_BULLET = []
    #敌方坦克子弹列表
    ENMY_TANK_BULLET_LIST = []
    #爆炸列表
    TANK_EXPLOD = []
    #墙壁列表
    WALL_LIST = []
    def __init__(self):
        pass
    #开始游戏
    def startgame(self):
        #初始化
        _display.init()
        #创建窗口
        MainGame.window = _display.set_mode([SCREEN_WIDTH,SCREEN_HIGHT])
        #创建我方坦克
        self.createmytank()
        #创建敌方坦克
        self.createEnemyTANK()
        #创建墙壁
        self.createlayWalls()
        #设置窗口标题
        _display.set_caption("坦克世界")
        #一直刷新窗口
        while True:
            #设置窗口背景颜色为黑色,给窗口填充颜色
            MainGame.window.fill(BLACK_COLOR)
            # 在循环中一直运行事件
            self.getevent()
            # 将绘制文本粘贴到小画布里面
            MainGame.window.blit(self.getTextSurface('剩余敌方坦克%d辆'%len(MainGame.ENME_TANK_LIST)), (5, 5))
            #将我方坦克粘贴到窗口当中
            #如果我方坦克活着，那么展示
            if MainGame.TANK_PI and MainGame.TANK_PI.live:
                MainGame.TANK_PI.displatTank()
            else:
                #否则就删除我方坦克
                del MainGame.TANK_PI
                MainGame.TANK_PI = None
            #将地方坦克粘贴到窗口当中
            self.bilitEnemy()
            #一直调用坦克移动
            if MainGame.TANK_PI and not MainGame.TANK_PI.stop:
                #调用坦克移动方法
                MainGame.TANK_PI.move()
                #调用我方坦克撞墙停止方法
                MainGame.TANK_PI.HitTankWall()
                #调用我方坦克撞上敌方坦克停止方法
                MainGame.TANK_PI.HitEnmyTank()
            #将我方坦克子弹加入到窗口钟
            self.bilitMyTankBULLET()
            #展示敌方子弹
            self.bilitEnmyTankBullet()
            #展示爆炸效果
            self.displayexplod()
            #展示墙壁
            self.displaywalls()
            #休眠
            time.sleep(0.02)
            #刷新
            _display.update()
    #创建敌方坦克
    def createEnemyTANK(self):
        top = 100
        speed = random.randint(2,6)
        for i in range(MainGame.ENME_TANK_COUNT):
            left = random.randint(1, 7)
            eTank = EnemyTank(left*100,top,speed)
            MainGame.ENME_TANK_LIST.append(eTank)
    #将坦克加入到窗口当中
    def bilitEnemy(self):
        for eTank in self.ENME_TANK_LIST:
            if eTank.live == True:
                eTank.displatTank()
                # 敌方坦克的随机移动方法
                eTank.randMove()
                #让敌方坦克不能碰撞到墙壁
                eTank.HitTankWall()
                #如果我方坦克活着
                if MainGame.TANK_PI and MainGame.TANK_PI.live:
                    # 调用敌方坦克撞上我方坦克的方法
                    eTank.HitMytank()
                # 调用敌方坦克的射击方法
                eBullet = eTank.shot()
                # 将子弹存储在敌方坦克子弹的列表
                if eBullet:
                    MainGame.ENMY_TANK_BULLET_LIST.append(eBullet)
            else:
                MainGame.ENME_TANK_LIST.remove(eTank)
    #展示我方子弹
    def bilitMyTankBULLET(self):
        for bullet in MainGame.TANK_PI_BULLET:
            #判断子弹是否位真，如果是真那么就展示
            if bullet.live == True:
                bullet.displayBullet()
                #调用子弹移动方法
                bullet.move()
                # 调用碰撞方法
                bullet.hitWalls()
                bullet.hitenmytank()
            else:
                #如果是False那么就从子弹列表中移除
                MainGame.TANK_PI_BULLET.remove(bullet)
    #展示敌方子弹
    def bilitEnmyTankBullet(self):
        for eBullet in MainGame.ENMY_TANK_BULLET_LIST:
            # 判断子弹是否位真，如果是真那么就展示
            if eBullet.live == True:
                #调用敌方子弹展示方法
                eBullet.displayBullet()
                #调用敌方子弹移动方法
                eBullet.move()
                #调用敌方坦克击中墙壁子弹消失方法
                eBullet.hitWalls()
                #如果我方坦克海活着那么就调用敌方子弹击中我方坦克方法
                if MainGame.TANK_PI and MainGame.TANK_PI.live:
                    # 调用敌方子弹打中我方坦克方法
                    eBullet.hitmytank()
            else:
                # 如果是False那么就从子弹列表中移除
                MainGame.ENMY_TANK_BULLET_LIST.remove(eBullet)
    #展示爆炸效果
    def displayexplod(self):
        for explod in MainGame.TANK_EXPLOD:
            if explod.live:
                explod.displayExplode()
            else:
                MainGame.TANK_EXPLOD.remove(explod)
    #获取事件
    def getevent(self):
        #获取所有事件
        eventList = pygame.event.get()
        #对事件进行判断处理（1.点击关闭按钮 2.按下键盘某个按钮）
        for event in eventList:
            #判断事件是否为QUIT如果是那么就执行endgame()退出
            if event.type == pygame.QUIT:
                self.endgame()
            #判断事件是否为按下按键
            if event.type == pygame.KEYDOWN:
                #判断坦克是否被删除，如果按下f按键并且，TANK_PI是死的那么就重新生城我方坦克
                if event.key == pygame.K_f and not MainGame.TANK_PI:
                    self.createmytank()
                #判断坦克是否存活如果存活那么就执行下面语句
                if MainGame.TANK_PI and MainGame.TANK_PI.live:
                    # 如果按下了按键判断是那个按键
                    if event.key == pygame.K_LEFT:
                        print("左移动")
                        #让坦克向左调头
                        MainGame.TANK_PI.direction = 'L'
                        # MainGame.TANK_PI.move()
                        #按下按键让stop变成false触发move方法
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print("右移动")
                        MainGame.TANK_PI.direction = 'R'
                        # MainGame.TANK_PI.move()
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_UP:
                        print("上移动")
                        MainGame.TANK_PI.direction = 'U'
                        # MainGame.TANK_PI.move()
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("下移动")
                        MainGame.TANK_PI.direction = 'D'
                        # MainGame.TANK_PI.move()
                        MainGame.TANK_PI.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("空格")
                        #判断屏幕中的子弹是否小于三个
                        if len(MainGame.TANK_PI_BULLET) < 3:
                            # 创建一颗子弹
                            m = Bullet(MainGame.TANK_PI)
                            # 把创建好的子弹放入列表
                            MainGame.TANK_PI_BULLET.append(m)
                        else:
                            print("子弹不足")
                        print("子弹剩余%d"%len(MainGame.TANK_PI_BULLET))
            #松开的如果是方向键按键,就停止坦克运动
            if event.type == pygame.KEYUP:
                if MainGame.TANK_PI and MainGame.TANK_PI.live:
                    if event.key == pygame.K_UP:
                        MainGame.TANK_PI.stop = True
                    elif event.key == pygame.K_DOWN:
                        MainGame.TANK_PI.stop = True
                    elif event.key == pygame.K_LEFT:
                        MainGame.TANK_PI.stop = True
                    elif event.key == pygame.K_RIGHT:
                        MainGame.TANK_PI.stop = True
    #绘制字体
    def getTextSurface(self, text):
        # 初始化字体模块
        pygame.font.init()
        # 选中一个合适的字体    18是字体大小
        font = pygame.font.SysFont('kaiti',18)
        # 使用对应的字符完成相关内容的绘制（画布）
        textSurface = font.render(text, True, COLOR_RED)
        return textSurface
    #创建我方坦克
    def createmytank(self):
        MainGame.TANK_PI = MyTank(250,400)
        # #加载音乐
        # music = Music()
        # #播放音乐
        # music.play()
    #创建墙壁
    def createlayWalls(self):
        top = 240
        for i in range(1,7):
            wall = Wall(i*100,top)
            MainGame.WALL_LIST.append(wall)
    #展示墙壁
    def displaywalls(self):
        for wall in MainGame.WALL_LIST:
            if wall.live:
                wall.DisplayWall()
            else:
                MainGame.WALL_LIST.remove(wall)
    #结束游戏
    def endgame(self):
        print("结束")
        exit()

#坦克类
class Tank(BaseIteam):
    def __init__(self,left,top):
        #设置坦克速度
        self.speed = 5
        #设置状态
        self.stop = True
        self.live = True
        #加载图片
        self.images = {
            'U':pygame.image.load('img/p1tankU.gif'),
            'D':pygame.image.load('img/p1tankD.gif'),
            'L':pygame.image.load('img/p1tankL.gif'),
            'R':pygame.image.load('img/p1tankR.gif'),
        }
        #设定坦克默认朝向
        self.direction = 'U'
        self.image = self.images[self.direction]
        #坦克所在区域
        self.rect = self.image.get_rect()
        #指定坦克初始化位置分别对应的是x,y
        self.rect.left = left
        self.rect.top = top
        #添加坦克速度

    #坦克移动
    def move(self):
        #设置上一个坐标点
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if self.direction == 'L':
            #如果往左边走，那么当前的left减去速度值
            if self.rect.left > 0:
                #解决bug，让坦克不能走出边界，左边走不能小于0
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HIGHT:
                self.rect.top += self.speed
    #坦克射击
    def shot(self):
        #发射子弹
        return Bullet(self)
    #展示坦克
    def displatTank(self):
        #重新设置坦克图片
        self.image = self.images[self.direction]
        #将坦克图片粘贴到窗口当中
        MainGame.window.blit(self.image,self.rect)
    #定义坦克回到上一个坐标点方法
    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop
    #定义坦克撞到墙壁的处理方法
    def HitTankWall(self):
        for wall in MainGame.WALL_LIST:
            if pygame.sprite.collide_rect(wall,self):
                self.stay()

#继承Tank类
class MyTank(Tank):
    def __init__(self,left,top):
        #调用父类的init方法
        super(MyTank, self).__init__(left,top)
    #让我方坦克撞上敌方坦克方法
    def HitEnmyTank(self):
        for eTank in MainGame.ENME_TANK_LIST:
            if pygame.sprite.collide_rect(eTank,self):
                self.stay()
#继承坦克类
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        #图片集不一样
        #方向
        #rect
        #速度
        #live是否活着
        self.live = True
        #添加敌方坦克步数
        self.step = 50
        #加载地方坦克图片
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif'),
        }
        #调用随机方向
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
    #生成随机数，来匹配上下左右
    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
    #让敌方坦克随机移动
    def randMove(self):
        #如果步数为0，就复位，随机调头坦克
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1
    #让敌方坦克开炮
    def shot(self):
        num = random.randint(1,1000)
        if num <= 20:
            return Bullet(self)
    #敌方坦克撞上我方坦克的方法处理
    def HitMytank(self):
        if pygame.sprite.collide_rect(MainGame.TANK_PI,self):
            self.stay()
#子弹类
#有个图片
#方向
#意味着子弹往那个敌方走
#子弹的方向和坦克的方向是一致的
class Bullet(BaseIteam):
    def __init__(self, tank):
        #子弹速度
        self.speed = 7
        #记录子弹状态
        self.live = True
        self.image = pygame.image.load('img/enemymissile.gif')
        # 坦克的方向
        self.direction = tank.direction
        # 子弹的位置
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
            self.rect.left = tank.rect.left + tank.rect.width
    #子弹移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                #子弹状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
    #展示子弹
    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)
    #添加我方子弹打中敌方坦克碰撞方法
    def hitenmytank(self):
         for eTank in MainGame.ENME_TANK_LIST:
             if pygame.sprite.collide_rect(eTank,self):
                 explod = Explode(eTank)
                 MainGame.TANK_EXPLOD.append(explod)
                 self.live = False
                 eTank.live = False
    #添加敌方坦克打中我方坦克的方法
    def hitmytank(self):
        if pygame.sprite.collide_rect(self,MainGame.TANK_PI):
            explod = Explode(MainGame.TANK_PI)
            MainGame.TANK_EXPLOD.append(explod)
            self.live = False
            MainGame.TANK_PI.live = False
    #添加子弹打中墙壁的方法
    def hitWalls(self):
        for wall in MainGame.WALL_LIST:
            if pygame.sprite.collide_rect(wall,self):
                #每次如果子弹打中墙壁，那么墙壁的hp减1
                wall.hp -=1
                #如果墙壁的血量等于1置换那么状态就修改成False
                if wall.hp <= 0:
                    wall.live = False
                self.live = False

#爆炸类+
class Explode():
    def __init__(self,tank):
        #坦克爆炸的位置就是爆炸效果展示的位置
        self.rect = tank.rect
        #设置状态
        self.live = True
        #设置下标
        self.step = 0
        #加载图片
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
        ]
        #让图片第一个初始为0
        self.image = self.images[self.step]
    #展示爆炸效果
    def displayExplode(self):
        #如果step小于images里面的图片那么就展示而且是循环展示
        if self.step < len(self.images):
            MainGame.window.blit(self.image,self.rect)
            #先更换图片，然后在展示
            self.image = self.images[self.step]
            self.step += 1
        else:
            #否则如果大于了images里面的图片，那么就停止
            self.live = False
            self.step = 0
#墙壁类
class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        #给墙壁设置生命值
        self.hp = 5
        #给墙壁设置属性
        self.live = True
        self.rect.left = left
        self.rect.top = top
    #展示墙壁
    def DisplayWall(self):
        MainGame.window.blit(self.image,self.rect)
#音效类
# class Music():
#     def __init__(self,filename):
#         self.filename = filename
#         #初始化音乐流
#         pygame.mixer.init()
#         #加载音乐
#         pygame.mixer.music.load(self.filename)
#     #播放音乐
#     def play(self):
#         pygame.mixer.music.play(self.filename)

MainGame().startgame()