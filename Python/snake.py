import pygame
import random
pygame.init()
width = 440
height = 440
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Змейка")
color_snake = (0, 255, 0)
black = (0,0,0)
blok_size = 10
kolvo_blokX = width/blok_size
kolvo_blokY = height/blok_size
score = 0
score_font = pygame.font.SysFont("comicsansms", 20)
game_over_font = pygame.font.SysFont("comicsansms", 35)
game_over_font2 = pygame.font.SysFont("comicsansms", 20)

speed = 0

class Control:
    def __init__(self):
        self.flag_game = True
        self.flag_dir = "RIGHT"
        self.flag_pause = True

    def control(self):
        """Управление в зависимостри от флага"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.flag_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT  and self.flag_dir != "LEFT":
                    self.flag_dir = "RIGHT"
                elif event.key == pygame.K_LEFT and self.flag_dir != "RIGHT":
                    self.flag_dir = "LEFT"
                elif event.key == pygame.K_DOWN and self.flag_dir != "UP":
                    self.flag_dir = "DOWN"
                elif event.key == pygame.K_UP and self.flag_dir != "DOWN":
                    self.flag_dir = "UP"
                elif event.key == pygame.K_ESCAPE:
                    self.flag_game = False
                elif event.key == pygame.K_SPACE:
                    if self.flag_pause == True:
                        self.flag_pause = False
                    elif self.flag_pause == False:
                        self.flag_pause = True

    def Your_score(self,screen):
        # loc_score = score
        value = score_font.render("Your Score: " + str(score), True, pygame.Color("Yellow"))
        screen.blit(value, [0, 0])


class Snake:
    def __init__(self):
        self.head = [40,40]
        self.body = [[40,40],[30,45],[20,45]]

    def move(self,control):
        """Движение змейки"""
        if control.flag_dir == "RIGHT":
            self.head[0]+=10
        elif control.flag_dir == "LEFT":
            self.head[0]-=10
        elif control.flag_dir == "UP":
            self.head[1]-= 10
        elif control.flag_dir == "DOWN":
            self.head[1]+=10

    def chec_end(self,):
        """Конец экрана и появление с обратной стороны"""
        if self.head[0] < 0 :
            self.head[0] = 440
        elif self.head[0] > 440:
            self.head[0] = 0
        elif self.head[1] > 440:
            self.head[1] = 0
        elif self.head[1] < 0:
            self.head[1] = 440

    def chec_end_body(self):
        if self.head in self.body[1:]:
            print("Проиграл!")
            return True



    def animation(self):
        """Прибавляем в начало списка голову, а хвост удаляем"""
        self.body.insert(0,list(self.head))
        self.body.pop()

    def draw_snake(self,screen):
        for i in self.body:
            pygame.draw.rect(screen,pygame.Color("Green"),pygame.Rect(i[0],i[1],blok_size,blok_size))

    def eat_food(self,food):
        if self.head == food.food_positions:
            self.body.append([food.food_positions])
            global score
            score += 1
            food.get_food_positions()




class Food:
    def __init__(self):
        self.food_positions = [100,100]

    def get_food_positions(self):
        """Рандомное значение еды"""

        self.food_positions[0] = round(random.randrange(0, kolvo_blokX) * blok_size)
        self.food_positions[1] = round(random.randrange(0, kolvo_blokY) * blok_size)


    def draw_food(self,screen):
        pygame.draw.rect(screen,pygame.Color("Red"),pygame.Rect(self.food_positions[0],self.food_positions[1],blok_size,blok_size))


def start_game():
    global score
    game_over = False
    score =0
    snake = Snake()
    control = Control()
    food = Food()
    global speed

    while control.flag_game:

        while game_over == True:
            screen.fill(pygame.Color("Blue"))
            mesg = game_over_font.render("Ты проиграл!", True, pygame.Color("Red"))
            screen.blit(mesg, [width/5, height/3])
            mesg = game_over_font2.render("Нажми С для повтора либо Q для выхода", True, pygame.Color("Red"))
            screen.blit(mesg, [30, height / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    control.flag_game = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        control.flag_game = False
                        game_over = False
                    if event.key == pygame.K_c:
                        start_game()


        control.control()
        screen.fill(pygame.Color("White"))
        snake.draw_snake(screen)
        food.draw_food(screen)
        control.Your_score(screen)
        if speed % 500 == 0 and control.flag_pause:
            snake.move(control)
            # print(snake.head)
            snake.eat_food(food)
            snake.animation()
            game_over = snake.chec_end_body()
            snake.chec_end()
        speed +=1
        pygame.display.flip()
    pygame.quit()
    quit()

start_game()