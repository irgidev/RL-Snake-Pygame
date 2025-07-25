import pygame

WIDTH = 640
HEIGHT = 480
BLACK = (0,0,0)
GREEN = (0,255,0)
FPS = 60
BLOCK_SIZE = 20
X_CENTER = WIDTH / 2
Y_CENTER = HEIGHT / 2
MOVE_INTERVAL = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RL Snake Game")
clock = pygame.time.Clock()

snake_head = pygame.Rect(X_CENTER,Y_CENTER, BLOCK_SIZE, BLOCK_SIZE)
direction = 'RIGHT'

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
            snake_head.x += BLOCK_SIZE
        elif direction == 'LEFT':
            snake_head.x -= BLOCK_SIZE
        elif direction == 'UP':
            snake_head.y -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_head.y += BLOCK_SIZE

    if snake_head.left < 0 or snake_head.right > WIDTH or snake_head.top < 0 or snake_head.bottom > HEIGHT:
            running = False

    screen.fill(BLACK)
    pygame.draw.rect(screen,GREEN,snake_head)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()