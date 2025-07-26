import pygame
import random

WIDTH = 640
HEIGHT = 480
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
FPS = 60
BLOCK_SIZE = 20
X_CENTER = WIDTH / 2
Y_CENTER = HEIGHT / 2
MOVE_INTERVAL = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RL Snake Game")
clock = pygame.time.Clock()

snake_body = []
direction = 'RIGHT'

def create_food():
    while True:
        random_food = pygame.Rect(random.randrange(0,WIDTH, BLOCK_SIZE),random.randrange(0,HEIGHT, BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        if random_food not in snake_body:
            return random_food

food = create_food()

for i in range(3):
    snake_body.append(pygame.Rect(X_CENTER - (BLOCK_SIZE * i),Y_CENTER, BLOCK_SIZE, BLOCK_SIZE))

running = True

last_move_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'

    now = pygame.time.get_ticks()
    if now - last_move_time > MOVE_INTERVAL:
        last_move_time = now

        if direction == 'RIGHT':
            x_new = snake_body[0].x + BLOCK_SIZE
            y_new = snake_body[0].y
        elif direction == 'LEFT':
            x_new = snake_body[0].x - BLOCK_SIZE
            y_new = snake_body[0].y
        elif direction == 'UP':
            x_new = snake_body[0].x 
            y_new = snake_body[0].y - BLOCK_SIZE
        elif direction == 'DOWN':
            x_new = snake_body[0].x 
            y_new = snake_body[0].y + BLOCK_SIZE
        
        new_head = pygame.Rect(x_new, y_new, BLOCK_SIZE, BLOCK_SIZE)
        snake_body.insert(0, new_head)
        if snake_body[0].colliderect(food):
            food = create_food()
        else:
            snake_body.pop()

        for i in range(1, len(snake_body)):
            if snake_body[0].colliderect(snake_body[i]):
                running = False

        if snake_body[0].left < 0 or snake_body[0].right > WIDTH or snake_body[0].top < 0 or snake_body[0].bottom > HEIGHT:
            running = False

    screen.fill(BLACK)
    for i in snake_body:
        pygame.draw.rect(screen,GREEN,i)
    pygame.draw.rect(screen,RED,food)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()