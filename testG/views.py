from http.client import HTTPResponse
from django.shortcuts import render
from pygame.math import Vector2
import pygame, sys, time, random
from pygame.constants import KEYDOWN
from math import sqrt
from random import randint
from time import sleep
import os
import pygame.transform

os.environ['SDL_VIDEODRIVER'] = 'dummy'
# 모든 게임 수정

games = [
#   {'title':'테트리스', 'image':'tetris', 'info':'네개의 사각형으로 이뤄진 블록을 쌓는 게임이다.'},
#   {'title':'팩맨', 'image':'packman', 'info':'몬스터를 피해서 미로에 있는 쿠키를 먹는 게임이다.'},
  {'title':'스네이크', 'image':'snake', 'info':'사과를 먹으며 뱀을 길게 만드는 게임이다.'},
  {'title':'비행기', 'image':'plane', 'info':'박쥐와 불덩이를 피해 날아가는 게임이다.'},
  {'title':'벽돌부수기', 'image':'bricksbreak', 'info':'벽돌을 부수는 게임이다.'},
  {'title':'공룡 달리기', 'image':'dino', 'info':'선인장과 익룡을 피해 달리는 게임이다.'},
]

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
# Snake 게임
def snake(request):
    context = {'games' : games}

    check_errors = pygame.init()
    # Here first we will check if the pygame successfully Initialized?

    if check_errors[1] > 0:
        print("(!) had {0} initializing errors, exiting....".format(check_errors[1]))
        sys.exit(-1)
    else:
        print("(!) PyGame Initialized Successfully!!!")


    # Play Surface
    playSurface = pygame.display.set_mode((720, 460)) # To set the console window where game will run, the set_mode expects a tupple having dimensions of the console
    pygame.display.set_caption('!!! SNAKE GAME !!!') # To set the Upper heading of the game console window


    #Colors
    # The color method expects three parameters r,g,b combination to give the color
    red = pygame.Color(255, 0 ,0) #red color-gameover
    green = pygame.Color(0, 255, 0) #green-snake
    black = pygame.Color(0, 0, 0) #black-score
    white = pygame.Color(255, 255, 255) #white-screen
    brown = pygame.Color(165, 42, 42) #brown-food


    # fps controller
    fpsController = pygame.time.Clock()

    # important varibles for the gameover
    snakePos = [100, 50] #initial coordinate of the snake head
    snakeBody = [[100, 50], [90, 50], [80, 50]] #snake snakeBody
    foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10] #random food positioning
    foodSpawn = True
    direction = 'RIGHT'
    changeTo = direction
    score = 0
    level = 15
    initscore = 0

    # Game Over function
    def gameOver():
        myFont = pygame.font.SysFont('monaco', 72) #choose font name and size
        GOsurf = myFont.render(' GAME OVER !!!', True, red) # this is the surface where game over will display having 3 args : the message, antialiasing,and Color
        GOrect = GOsurf.get_rect() #to get rect coordinates of the game over text surface
        GOrect.midtop = (360, 15)
        playSurface.blit(GOsurf, GOrect) # bind the gameover text to the main surface
        showScore(0)
        pygame.display.flip() # to set the fps
        time.sleep(3)
        # pygame.quit() # exit game window
        
        # sys.exit() # exit cmd console
        

    def showScore(choice=1):
        sFont = pygame.font.SysFont('monaco', 42) #choose font name and size
        Ssurf = sFont.render('SCORE : {0}'.format(score), True, black) # this is the surface where game over will display having 3 args : the message, antialiasing,and Color
        Srect = Ssurf.get_rect() #to get rect coordinates of the game over text surface
        if choice == 1:
            Srect.midtop = (80, 10)
        else:
            Srect.midtop = (360, 120)

        playSurface.blit(Ssurf, Srect) # bind the gameover text to the main surface
        pygame.display.flip() # to set the fps

    
    # Main Logic Of The GAME
    while True:
        for event in pygame.event.get(): # accepts the event
            if event.type == pygame.QUIT: # quit event
                pygame.quit()
                
                return render(request, 'basic/main.html', context)
            elif event.type == pygame.KEYDOWN: # when keyboard key is pressed
                if event.key == pygame.K_RIGHT or event.key == ord('d'): # Right Move
                    changeTo = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'): # Left Move
                    changeTo = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'): # Up Move
                    changeTo = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'): # Down Move
                    changeTo = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))  # post function first creates a event and inside it we emit a quit event

        # validation of direction
        if changeTo == 'LEFT' and not direction =='RIGHT':
            direction = 'LEFT'
        if changeTo == 'RIGHT' and not direction =='LEFT':
            direction = 'RIGHT'
        if changeTo == 'UP' and not direction =='DOWN':
            direction = 'UP'
        if changeTo == 'DOWN' and not direction =='UP':
            direction = 'DOWN'

        # Value change after direction change
        if direction == 'RIGHT':
            snakePos[0] += 10
        if direction == 'LEFT':
            snakePos[0] -= 10
        if direction == 'UP':
            snakePos[1] -= 10
        if direction == 'DOWN':
            snakePos[1] += 10

        # Snake Body Mechanism
        snakeBody.insert(0, list(snakePos))
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            score += 1
            foodSpawn = False
        else:
            snakeBody.pop()
        # food spawn
        if foodSpawn == False:
            foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
        foodSpawn = True
        playSurface.fill(white)
        for pos in snakeBody:
            pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
        pygame.draw.rect(playSurface,brown,pygame.Rect(foodPos[0],foodPos[1],10,10))

        # Boundary Condition
        if snakePos[0] > 710 or snakePos[0] < 0:
            gameOver()
            pygame.quit()
            return render(request, 'basic/main.html', context)
        if snakePos[1] > 450 or snakePos[1] < 0:
            gameOver()
            pygame.quit()
            return render(request, 'basic/main.html', context)

        # Self Body Collision
        for block in snakeBody[1:]:
            if snakePos[0] == block[0] and snakePos[1] == block[1]:
                gameOver()
                pygame.quit()
                return render(request, 'basic/main.html', context)

        showScore() # To show the score
        # FPS CONTROL
        pygame.display.flip()
        #pygame.display.update()
        if score == initscore+5:
            level+=5
            initscore = score
        fpsController.tick(level)

    return render(request, 'basic/main.html', context)

# 비행기게임
def plane(request):
    def drawObject(obj, x, y):
        screen.blit(obj, (x, y))

    def crash():
        message_over = largefont.render("Game Over!", True, (255, 0, 0))
        message_rect = message_over.get_rect()
        message_rect.center = ((screen_width/2), (screen_height/2))
        screen.blit(message_over, message_rect)
        pygame.display.update()

    # pygame 초기화
    pygame.init()

    largefont = pygame.font.SysFont(None, 72)

    fires = []

    WHITE = (255,255,255)
    screen_width = 580
    screen_height = 380

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Airplane Game')

    aircraft = pygame.image.load('./static/image/airplane.png')
    aircraft = pygame.transform.scale(aircraft, (60, 45))

    background1 = pygame.image.load('./static/image/background.png')
    background1 = pygame.transform.scale(background1, (screen_width, screen_height))
    background2 = background1.copy()

    bat = pygame.image.load('./static/image/bat.png')
    bat = pygame.transform.scale(bat, (90, 50))

    boom = pygame.image.load('./static/image/boom.png')

    fires.append((0, pygame.image.load('./static/image/fireball.png')))
    fires.append((1, pygame.image.load('./static/image/fireball2.png')))
    for i in range(3):
        fires.append((i+2, None))

    bullet = pygame.image.load('./static/image/bullet.png')

    clock = pygame.time.Clock()

    # rungame
    isShotBat = False
    boom_count = 0

    bullet_xy = []

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

    context = {'games' : games}

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # crashed = True
                return render(request, 'basic/main.html', context)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_SPACE:
                    bullet_x = x + 30
                    bullet_y = y + 45/2
                    bullet_xy.append([bullet_x, bullet_y])

        screen.fill(WHITE)

        # 배경
        background1_x -= 2
        background2_x -= 2

        if background1_x == -screen_width:
            background1_x = screen_width            
        if background2_x == -screen_width:
            background2_x = screen_width
                
        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        # 비행기 위치
        y += y_change
        if y < 0:
            y = 0
        elif y > screen_height - 45:
            y = screen_height - 45
        x += x_change
        if x < 0:
            x = 0
        elif x > screen_width - 60:
            x = screen_width - 60

        # 배트맨
        bat_x -= 7
        if bat_x <= 0:
            bat_x = screen_width
            bat_y = random.randrange(0, screen_width)
        
        # 불
        if fire == None:
            fire_x -= 30
        else:
            fire_x -= 15
        if fire_x <= 0:
            fire_x = screen_width
            fire_y = random.randrange(0, screen_height)
            random.shuffle(fires)
            fire = fires[0]

        # 총알
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                if bxy[0] > bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + 67:
                        bullet_xy.remove(bxy)
                        isShotBat = True

                if bxy[0] >= screen_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
        
        # 공격 받으면 죽음
        if x + 60 > bat_x:
            if (y > bat_y and y < 67) or (y + 45 > bat_y and y + 45 < bat_y + 67):
                crash()
                sleep(3)
                crashed = True
        if fire[1] != None:
            if fire[0] == 0:
                fireball_width = 140
                fireball_height = 60
            elif fire[0] == 1:
                fireball_width = 86
                fireball_height = 60
            
            if x + 60 > fire_x:
                if (y > fire_y and y < fire_y + fireball_height) or \
                (y + 45 > fire_y and y + 45 < fire_y + fireball_height):
                    crash()
                    sleep(3)
                    crashed = True

        drawObject(aircraft, x, y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotBat:
            drawObject(bat, bat_x, bat_y)
        else:
            drawObject(boom, bat_x, bat_y)
            boom_count += 1
            if boom_count > 5:
                bat_x = screen_width
                bat_y = random.randrange(0, screen_height - 67)
                isShotBat = False

        if fire[1] != None:
            drawObject(fire[1], fire_x, fire_y)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    
    
    return render(request, 'basic/main.html', context)

# 벽돌부수기
def bricksbreak(request):
    
    pygame.init()  # 초기화

    background = pygame.display.set_mode((1680, 960))  # 스크린 크기
    pygame.display.set_caption("벽돌 깨기")  # 타이틀 이름

    fps = pygame.time.Clock()  # fps 설정

    # 스크린 크기 변수 지정
    screen_width = background.get_size()[0]
    screen_height = background.get_size()[1]


    # 게임 텍스트
    def game_text(word):
        font = pygame.font.SysFont(None, 100)  # 폰트와 크기 지정

        text = font.render(word, True, (255, 255, 255))  # 텍스트 색깔

        text_width = text.get_rect().size[0]  # 텍스트 크기
        text_height = text.get_rect().size[1]

        text_x_pos = screen_width // 2 - text_width // 2  # 텍스트 위치
        text_y_pos = screen_height // 2 - text_height // 2

        background.blit(text, (text_x_pos, text_y_pos))  # 텍스트 그리기


    # 패들 크기, 좌표
    paddle_width = 150
    paddle_height = 30

    paddle_x_pos = screen_width // 2 - paddle_width // 2
    paddle_y_pos = screen_height - paddle_height - 100

    paddle_to_x = 0  # 패들 이동 변수
    paddle_speed = 12  # 패들 속도 변수

    # 공의 크기, 좌표, Rect
    ball_size_radius = 10  # 공의 반지름 크기

    ball_x_pos = screen_width // 2  # 공 가로 위치
    ball_y_pos = screen_height - paddle_height - ball_size_radius - 100  # 공 세로 위치
    ball_rect = pygame.Rect(ball_x_pos, ball_y_pos, ball_size_radius * 2, ball_size_radius * 2)  # rect 의 x, y 좌표는 좌상단

    # 공의 방향과 속도
    ball_to_x = 6
    ball_to_y = 6

    # 벽돌 크기, 좌표, Rect
    brick_width = 100
    brick_height = 30

    brick_x_pos = 0
    brick_y_pos = 0

    brick_rect = [[] for _ in range(14)]  # [[], [], [], [], []...] 벽돌 rect 정보를 리스트안에 리스트로 range 갯수만큼 만듬

    for column in range(14):
        for row in range(5):  # 벽돌을 배열로 배치 (x, y, 가로길이, 세로길이)
            brick_rect[column].append(pygame.Rect(70 + column * (brick_width + 10), 100 + row * (brick_height + 10), brick_width, brick_height))

    point = 0  # 점수
    start = True  # 시작 전 준비 변수
    play = True  # 게임 시작
    while play:  # 게임이 진행 중
        dt = fps.tick(45)  # fps 설정

        # 시작 전 준비
        if start:  # start 변수가 True 일때만 실행
            start = False  # while의 가장 처음 루프에서만 실행되고 start 변수가 False 로 바뀌어 다음 루프때는 if 문으로 들어오지않음
            for countdown in range(0, 0, -1):  # range 값만큼 카운트다운
                background.fill((0, 0, 35))
                game_text(str(countdown))
                pygame.display.update()
                pygame.time.delay(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 닫기 버튼을 클릭
                play = False  # 게임 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC 버튼 입력
                    play = False
                elif event.key == pygame.K_LEFT:  # 왼쪽 화살표 입력하면 패들 이동속도 만큼 왼쪽으로 이동
                    paddle_to_x -= paddle_speed
                elif event.key == pygame.K_RIGHT:  # 오른쪽 화살표 입력하면 패들 이동속도 만큼 오른쪽으로 이동
                    paddle_to_x += paddle_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # 왼쪽, 오른쪽 화살표 입력을 떼면 패들 멈춤
                    paddle_to_x = 0

        paddle_x_pos += paddle_to_x  # 화살표 입력한 만큼 패들을 움직임
        paddle_rect = pygame.Rect(paddle_x_pos, paddle_y_pos, paddle_width, paddle_height)

        # 배경 그리기
        background.fill((0, 0, 35))

        # 패들 그리기 (surface, color, (x, y, 가로길이, 세로길이))
        pygame.draw.rect(background, (0, 255, 255), paddle_rect)

        if paddle_x_pos <= 0:  # 패들이 왼쪽 벽에 부딪치면 더이상 왼쪽으로 이동 불가
            paddle_x_pos = 0
        elif paddle_x_pos + paddle_width >= screen_width:  # 패들이 오른쪽 벽에 부딪치면 더이상 오른쪽으로 이동 불가
            paddle_x_pos = screen_width - paddle_width

        # 공 이동 좌표 계산
        if ball_x_pos - ball_size_radius <= 0:  # 공이 왼쪽벽에 부딪치면 오른쪽으로 이동
            ball_to_x = -ball_to_x
        elif ball_x_pos + ball_size_radius >= screen_width:  # 공이 오른쪽 벽에 부딪치면 왼쪽으로 이동
            ball_to_x = -ball_to_x

        if ball_y_pos - ball_size_radius <= 0:  # 공이 위쪽 벽에 부딪치면 아래로 이동
            ball_to_y = -ball_to_y
        elif ball_y_pos + ball_size_radius >= screen_height:  # 공이 아래쪽 벽에 부딪치면 공이 멈추고 게임 종료
            game_text("GAME OVER")
            pygame.display.update()
            pygame.time.delay(1000)
            break


        # 공 좌표에 따라 이동
        ball_x_pos += ball_to_x
        ball_y_pos += ball_to_y

        # 공 그리기 (surface, color, center(x, y), radius)
        pygame.draw.circle(background, (0, 0, 255), (ball_x_pos, ball_y_pos), 10)
        ball_rect.center = (ball_x_pos - 10, ball_y_pos - 10)  # 변경된 좌표에 따라 공 중앙에 새로 rect 지정

        # 공이 패들과 충돌 (어떻게하면 공의 센터를 정확히 측정할 수 있을지 모르겠다. 우선 검증되지않은 센터값을 기준으로 코딩했다)
        if ball_rect.colliderect(paddle_rect):
            ball_to_y = -ball_to_y  # 공을 다시 위로 이동
            if paddle_x_pos + paddle_width // 2 - 5 <= ball_rect.center[0] <= paddle_x_pos + paddle_width // 2 + 5:
                ball_to_x = 0.1 * ball_to_x  # 패들의 정가운데 범위에 충돌하면 공 속도와 x좌표를 지정값만큼 배수
                print('real_center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
            elif paddle_x_pos + paddle_width // 2 - 10 <= ball_x_pos <= paddle_x_pos + paddle_width // 2 + 10:
                ball_to_x = 0.8 * ball_to_x  # 패들의 가운데 범위에 충돌하면 공 속도와 x좌표를 지정값만큼 배수
                print('center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
            elif paddle_x_pos + paddle_width // 2 - 30 <= ball_x_pos <= paddle_x_pos + paddle_width // 2 - 10:
                ball_to_x = max(-2 - abs(ball_to_x) * 2, -5)  # 패들의 왼쪽 가운데 범위에 충돌하면 공 속도와 x좌표가 지정값 중 큰 값만큼 왼쪽으로 이동
                print('left_center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
            elif ball_x_pos <= paddle_x_pos + paddle_width // 2 - 30:
                ball_to_x = max(-5 - abs(ball_to_x) * 5, -10)  # 패들의 왼쪽 범위에 충돌하면 공 속도와 x좌표거 지정값 중 큰 값만큼 왼쪽으로 이동
                print('left : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
            elif paddle_x_pos + paddle_width // 2 + 10 <= ball_x_pos <= paddle_x_pos + paddle_width // 2 + 30:
                ball_to_x = min(2 + abs(ball_to_x) * 2, 5)  # 패들의 오른쪽 가운데 범위에 충돌하면 공 속도와 x좌표가 지정값 중 작은 값만큼 오른쪽으로 이동
                print('right_center : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))
            elif paddle_x_pos + paddle_width // 2 + 30 <= ball_x_pos:
                ball_to_x = min(5 + abs(ball_to_x) * 5, 10)  # 패들의 오른쪽 범위에 충돌하면 공 속도와 x좌표가 지정값 중 큰 값만큼 오른쪽으로 이동
                print('right : ' + str(ball_rect.center[0]), str(paddle_x_pos + paddle_width // 2))

        # 벽돌 그리기
        for column in range(14):
            for row in range(5):
                if brick_rect[column][row]:  # 벽돌을 배열로 그리기 (surface, color, brick_rect = (x, y, 가로길이, 세로길이))
                    pygame.draw.rect(background, (127, 127, 127), brick_rect[column][row])
                    # 배열위치에 rect 값 지정
                    brick_rect[column][row].topleft = (70 + column * (brick_width + 10), 100 + row * (brick_height + 10))
                    
                    
                    # 공이 벽돌과 충돌
                    if ball_rect.colliderect(brick_rect[column][row]):
                        ball_to_y = -ball_to_y  # y축 반대로 이동
                        brick_rect[column][row] = 0  # 부딪친 벽돌은 없어짐
                        point += 1  # 벽돌없어질때마다 1점

        # 게임 클리어
        if point == 90:  # 점수가 지정값이 되면
            game_text("GAME CLEAR")  # 텍스트 함수 호출
            pygame.display.update()
            pygame.time.delay(1000)
            play = False  # 게임 종료

        pygame.display.update()  # 게임 화면 다시 그리기

    pygame.quit()  # 프로그램 종료
    
    context = {'games' : games}
    return render(request, 'basic/main.html', context)

# 공룡 달리기   
def dino(request):
    context = {'games' : games}

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Dino Game")

    game_font = pygame.font.SysFont(None, 24)

    class Cloud(pygame.sprite.Sprite):
        def __init__(self, image, x_pos, y_pos):
            super().__init__()
            self.image = image
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        def update(self):
            self.rect.x -= 1

    class Dino(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            super().__init__()
            self.running_sprites = []
            self.ducking_sprites = []

            self.running_sprites.append(pygame.transform.scale(
                pygame.image.load("./static/image/assets/Dino1.png"), (80, 100)))
            self.running_sprites.append(pygame.transform.scale(
                pygame.image.load("./static/image/assets/Dino2.png"), (80, 100)))

            self.ducking_sprites.append(pygame.transform.scale(
                pygame.image.load(f"./static/image/assets/DinoDucking1.png"), (110, 60)))
            self.ducking_sprites.append(pygame.transform.scale(
                pygame.image.load(f"./static/image/assets/DinoDucking2.png"), (110, 60)))

            self.x_pos = x_pos
            self.y_pos = y_pos
            self.current_image = 0
            self.image = self.running_sprites[self.current_image]
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.velocity = 50
            self.gravity = 4.5
            self.ducking = False

        def jump(self):
            if self.rect.centery >= 360:
                while self.rect.centery - self.velocity > 40:
                    self.rect.centery -= 1

        def duck(self):
            self.ducking = True
            self.rect.centery = 380

        def unduck(self):
            self.ducking = False
            self.rect.centery = 360

        def apply_gravity(self):
            if self.rect.centery <= 360:
                self.rect.centery += self.gravity

        def update(self):
            self.animate()
            self.apply_gravity()

        def animate(self):
            self.current_image += 0.05
            if self.current_image >= 2:
                self.current_image = 0

            if self.ducking:
                self.image = self.ducking_sprites[int(self.current_image)]
            else:
                self.image = self.running_sprites[int(self.current_image)]

    class Cactus(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            super().__init__()
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.sprites = []
            for i in range(1, 7):
                current_sprite = pygame.transform.scale(
                    pygame.image.load(f"./static/image/assets/cacti/cactus{i}.png"), (70, 70))
                self.sprites.append(current_sprite)
            self.image = random.choice(self.sprites)
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        def update(self):
            self.x_pos -= game_speed
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    class Ptero(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.x_pos = 1300
            self.y_pos = random.choice([280, 295, 350])
            self.sprites = []
            self.sprites.append(
                pygame.transform.scale(
                    pygame.image.load("./static/image/assets/Ptero1.png"), (76, 55)))
            self.sprites.append(
                pygame.transform.scale(
                    pygame.image.load("./static/image/assets/Ptero2.png"), (76, 55)))
            self.current_image = 0
            self.image = self.sprites[self.current_image]
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        def update(self):
            self.animate()
            self.x_pos -= game_speed
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        def animate(self):
            self.current_image += 0.025
            if self.current_image >= 2:
                self.current_image = 0
            self.image = self.sprites[int(self.current_image)]

    # Variables
    game_speed = 4
    jump_count = 10
    player_score = 0
    game_over = False
    obstacle_timer = 0
    obstacle_spawn = False
    obstacle_cooldown = 1000

    # Surfaces
    ground = pygame.image.load("./static/image/assets/ground.png")
    ground = pygame.transform.scale(ground, (1280, 20))
    ground_x = 0
    ground_rect = ground.get_rect(center=(640, 400))
    cloud = pygame.image.load("./static/image/assets/cloud.png")
    cloud = pygame.transform.scale(cloud, (200, 80))

    # Groups
    cloud_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    dino_group = pygame.sprite.GroupSingle()
    ptero_group = pygame.sprite.Group()

    # Objects
    dinosaur = Dino(50, 360)
    dino_group.add(dinosaur)

    # Events
    CLOUD_EVENT = pygame.USEREVENT
    pygame.time.set_timer(CLOUD_EVENT, 3000)

    # Functions
    def end_game():
        # global player_score, game_speed
        game_over_text = game_font.render("Game Over!", True, "black")
        game_over_rect = game_over_text.get_rect(center=(640, 300))
        score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
        score_rect = score_text.get_rect(center=(640, 340))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        game_speed = 4
        cloud_group.empty()
        obstacle_group.empty()

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            dinosaur.duck()
        else:
            if dinosaur.ducking:
                dinosaur.unduck()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
                return render(request, 'basic/main.html', context)
            if event.type == CLOUD_EVENT:
                current_cloud_y = random.randint(50, 300)
                current_cloud = Cloud(cloud, 1380, current_cloud_y)
                cloud_group.add(current_cloud)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dinosaur.jump()
                    if game_over:
                        game_over = False
                        game_speed = 4
                        player_score = 0

        screen.fill("white")

        # Collisions
        if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
            game_over = True
            
        if game_over:
            end_game()

        if not game_over:
            game_speed += 0.0015

            if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
                obstacle_spawn = True

            if obstacle_spawn:
                obstacle_random = random.randint(1, 50)
                if obstacle_random in range(1, 7):
                    new_obstacle = Cactus(1280, 340)
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False
                elif obstacle_random in range(7, 10):
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False

            player_score += 0.1
            player_score_surface = game_font.render(
                str(int(player_score)), True, ("black"))
            screen.blit(player_score_surface, (1150, 10))

            cloud_group.update()
            cloud_group.draw(screen)

            ptero_group.update()
            ptero_group.draw(screen)

            dino_group.update()
            dino_group.draw(screen)

            obstacle_group.update()
            obstacle_group.draw(screen)

            ground_x -= game_speed

            screen.blit(ground, (ground_x, 360))
            screen.blit(ground, (ground_x + 1280, 360))

            if ground_x <= -1280:
                ground_x = 0

        clock.tick(120)
        pygame.display.update()