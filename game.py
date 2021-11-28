import pygame

pygame.init() #инициализация (запуск библиотеки pygame)
win = pygame.display.set_mode((500,500)) #размеры окна 500х500

pygame.display.set_caption("Cubes") # название игры(заголовок окна)

walkRight = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'), pygame.image.load('right_3.png'), pygame.image.load('right_4.png'), pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]

walkLeft = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'), pygame.image.load('left_3.png'), pygame.image.load('left_4.png'), pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]

bg = pygame.image.load('bg.jpg')
playerStand = pygame.image.load('idle.png')

clock = pygame.time.Clock()

x = 50 #координаты начинаются с вернего левого угла
y = 425
width = 60 #положение игрока
height = 71
speed = 5

isJump = False #прыгает ли игрок в данный момент
jumpCount = 10 #величина прыжка

left = False  #по умолчанию в начале игры игрок неподвижен
right = False
animCount = 0
lastMove = 'right'

class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing #скорость
    
    def draw(self, win): #отрисовываем пулю
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def drawWindow():
    global animCount
    win.blit(bg,(0,0)) #постоянная отрисовка цвета заднего фона, чтобы не отображался след игрока, или картинки
    if animCount + 1 >= 30: #в игре 30 кадров в сек. Если animcount превысило 30, то обходим картинки заново
        animCount = 0
    if left:
        win.blit(walkLeft[animCount // 5], (x,y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (x,y))
        animCount += 1
    else:
        win.blit(playerStand,(x,y)) #если стоит на месте
    for bullet in bullets:
        bullet.draw(win)
    
    #pygame.draw.rect(win, (0,0,255), (x,y, width, height)) #draw - команда рисования игрока, rect - квадрат, win - окно
    pygame.display.update() #постоянное обновление окна

run = True

bullets = []
 
while run: #бесконечный цикл, для поддержания игры
    clock.tick(30) #выполнение 30 фреймов (кадров в секунду)
    #pygame.time.delay(50) #выполнение цикла каждые 100 мсек

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #если пришла команда quit: закрытие цикла
            run = False


    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0: #если пуля не выщла из рамок игры
            bullet.x += bullet.vel # движение пули, если она в рамках  игры
        else:
            bullets.pop(bullets.index(bullet)) # удаление пули


    keys = pygame.key.get_pressed() #отслеживание нажатых клавиш
    if keys[pygame.K_f]: #выпуск снаряда
        if lastMove == 'right':
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5: #меньше 5 снарядов
            bullets.append(snaryad(round(x + width // 2), round(y + height // 2), 5, (255,0,0), facing))
    if keys[pygame.K_LEFT] and x > 5: #отслеживание нажатых клавиш : помещаем в список
        x -= speed
        left = True
        right = False
        lastMove = 'left'
    elif keys[pygame.K_RIGHT] and x < 500 - width - 5: #отслеживание нажатых клавиш : помещаем в список
        x += speed    
        left = False
        right = True
        lastMove = 'right'
    else:
        left = False
        right = False
        animCount = 0
    if not(isJump): #проверка находится ли  игрок в прыжке
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:  #если условие выполняется, то игрок прыгает
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
            else:
                y -= (jumpCount ** 2) / 2
            jumpCount -= 1 #уменьшение скорости прыжка
        else: #если условие не выполняется,  то прыжок закончили
            isJump = False
            jumpCount = 10

    drawWindow()

pygame.quit() # дублирование команды закрытия приложения