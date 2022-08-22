from http.client import HTTPResponse
from django.shortcuts import render
from pygame.math import Vector2
import pygame, sys, time, random
from pygame.constants import KEYDOWN

games = [
  {'title':'테트리스', 'image':'tetris', 'info':'네개의 사각형으로 이뤄진 블록을 쌓는 게임이다.'},
  {'title':'팩맨', 'image':'packman', 'info':'몬스터를 피해서 미로에 있는 쿠키를 먹는 게임이다.'},
  {'title':'스네이크', 'image':'snake', 'info':'사과를 먹으며 뱀을 길게 만드는 게임이다.'},
  {'title':'비행기', 'image':'plane', 'info':'장애물을 피해 날아가는 게임이다.'},
  {'title':'벽돌부수기', 'image':'packman', 'info':'벽돌을 부수는 게임이다.'},
]

# Create your views here.
def main(request):
  context = {'games' : games}
  return render(request, 'basic/main.html', context)

def play(request, title):
  games1 = None
  
  for i in games:
    if i['title'] == title:
      games1 = i

  context = {'games1' : games1}
  return render(request, 'basic/play.html', context)


# Game
 
def snake(request):
    snake_block = 20
    cells = 30

    class FOOD:
        def __init__(self):
            self.x = random.randint(0, cells - 1)
            self.y = random.randint(0, cells - 1)
            self.pos = Vector2(self.x, self.y)

        def food_draw(self):
            food_rect = pygame.Rect(self.pos.x * snake_block, self.pos.y * snake_block, snake_block, snake_block)
            pygame.draw.rect(display,(pygame.Color('red')), food_rect)

        def randomiser(self):
            self.x = random.randint(0, cells - 1)
            self.y = random.randint(0, cells - 1)
            self.pos = Vector2(self.x, self.y)

    class SNAKE:
        def __init__(self):
            self.body = [Vector2(6, 10), Vector2(7, 10), Vector2(8, 10)]
            self.dir = Vector2(1, 0)
            self.grow = False

        def draw_snake(self):
                for block in self.body:
                    snake_rect = pygame.Rect(block.x * snake_block, block.y * snake_block, snake_block, snake_block)
                    pygame.draw.rect(display, (pygame.Color('gold')), snake_rect)

        def move(self):
            if self.grow == False:
                step = self.body[:-1]
                step.insert(0, step[0] + self.dir)
                self.body = step[:]
            else:
                step = self.body[:]
                step.insert(0, step[0] + self.dir)
                self.body = step[:]
                self.grow = False

        def add(self):
            self.grow = True

    class MAIN:
        def __init__(self):
            self.snake = SNAKE()
            self.food = FOOD()

        def update(self):
            self.snake.move()

        def draw(self):
            self.food.food_draw()
            self.snake.draw_snake()

        def eat(self):
            if self.food.pos == self.snake.body[0]:
                self.food.randomiser()
                self.snake.add()

        #def cut(self):
        #    if not 0 <= self.snake.body[0] <= 

    context = {'games' : games}

    pygame.init()

    game = MAIN()

    SCREENUPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREENUPDATE, 150)

    dis_height = snake_block * cells
    dis_width = snake_block * cells

    display = pygame.display.set_mode((dis_height, dis_width))
    pygame.display.set_caption('Snake Game By Amadeus')

    clock = pygame.time.Clock()

    snake = 10
    speed = 60

    surface = pygame.Surface((100, 200))

    lightblue = (135, 206, 235)

    gameover = False
    close = False
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return render(request, 'basic/main.html', context)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.dir = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    game.snake.dir = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    game.snake.dir = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.snake.dir = Vector2(1, 0)
            if event.type == SCREENUPDATE:
                game.snake.move()
        display.fill(lightblue)
        game.draw()
        game.eat()
        pygame.display.update()
        clock.tick(speed)
    pygame.quit()

    return render(request, 'basic/play.html')


def plane(request):
    def drawObject(obj, x, y):
        screen.blit(obj, (x, y))

    # pygame 초기화
    pygame.init()

    fires = []

    WHITE = (255,255,255)
    screen_width = 580
    screen_height = 350

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Airplane Game')

    aircraft = pygame.image.load('./static/image/plane.png')
    aircraft = pygame.transform.scale(aircraft, (60, 45))

    background1 = pygame.image.load('./static/image/background.png')
    background1 = pygame.transform.scale(background1, (screen_width, screen_height))
    background2 = background1.copy()

    bat = pygame.image.load('./static/image/bat.png')
    bat = pygame.transform.scale(bat, (90, 50))

    fires.append(pygame.image.load('./static/image/fireball.png'))
    fires.append(pygame.image.load('./static/image/fireball2.png'))
    for i in range(5):
        fires.append(None)

    clock = pygame.time.Clock()

    # rungame
    x = screen_width * 0.05
    y = screen_height * 0.8
    y_change = 0
    x_change = 0

    background1_x = 0
    background2_x = screen_width

    bat_x = screen_width
    bat_y = random.randrange(0, screen_width)

    fire_x = screen_width
    fire_y = random.randrange(0, screen_width)
    random.shuffle(fires)
    fire = fires[0]

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
        y += y_change
        x += x_change
        screen.fill(WHITE)

        background1_x -= 2
        background2_x -= 2

        bat_x -= 7
        if bat_x <= 0:
            bat_x = screen_width
            bat_y = random.randrange(0, screen_width)
        
        if fire == None:
            fire_x -= 30
        else:
            fire_x -= 15
        if fire_x <= 0:
            fire_x = screen_width
            fire_y = random.randrange(0, screen_height)
            random.shuffle(fires)
            fire = fires[0]

        if background1_x == -screen_width:
            background1_x = screen_width            
        if background2_x == -screen_width:
            background2_x = screen_width
                
        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)
        drawObject(bat, bat_x, bat_y)
        if fire != None:
            drawObject(fire, fire_x, fire_y)
        drawObject(aircraft, x, y)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    
    context = {'games' : games}
    return render(request, 'basic/main.html', context)