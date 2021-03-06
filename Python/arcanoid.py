import pygame
from random import randrange as rnd

pygame.init()

width, height = 1000, 600
fps = 60
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
img = pygame.image.load("image.jpg").convert()

#Платформа
paddle_w = 200
paddle_h = 30
paddle_speed = 23
paddle = pygame.Rect(width//2 - paddle_w // 2, height - paddle_h, paddle_w, paddle_h)

#Мячик
ball_radius, ball_speed = 20, 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, width - ball_rect),height//2, ball_rect, ball_rect)
dx, dy = 1, -1

#Блоки
block_list = []

def movepaddle():
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and  paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and  paddle.right < width:
        paddle.right += paddle_speed

def rebount():
    global dx, dy
    if ball.x > width - ball_radius or ball.x < 0 + ball_radius:
        dx = -dx
    if ball.y < 0 + ball_radius - 5:
        dy = -dy
    if ball.colliderect(paddle):
        dx, dy = collision(dx, dy, ball, paddle)

def craft_block():
    for i in range(9):
        for j in range(4):
            block_list.append(pygame.Rect(10 + 110 * i, 10 + 60 * j, 100, 50))


def draw_block():
    for i in block_list:
        pygame.draw.rect(screen, pygame.Color("red"), i)


def collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
        # print(ball.right)
        # print(rect.left)
        # print(delta_x)
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
        # print(ball.bottom)
        # print(rect.top)
        # print(delta_y)
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x>delta_y:
        dy = -dy
    elif delta_x<delta_y:
        dx = -dx
    return dx, dy

def collision_block():
    global dx, dy
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        dx, dy = collision(dx, dy, ball, hit_rect)

craft_block()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(img, (0,0))
    pygame.draw.rect(screen, pygame.Color("blue"), paddle)
    pygame.draw.circle(screen, pygame.Color("White"), ball.center, ball_radius)
    # craft_block()
    draw_block()
    collision_block()
    movepaddle()
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    rebount()


    pygame.display.flip()
    clock.tick(fps)