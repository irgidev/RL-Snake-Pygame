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



class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("RL Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()
        
    def _create_food(self):
        while True:
            random_food = pygame.Rect(random.randrange(0,WIDTH, BLOCK_SIZE),random.randrange(0,HEIGHT, BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
            if random_food not in self.snake_body:
                return random_food

    def reset(self):
        self.snake_body = []
        self.direction = 'RIGHT'
        self.last_move_time = pygame.time.get_ticks()
        for i in range(3):
            self.snake_body.append(pygame.Rect(X_CENTER - (BLOCK_SIZE * i),Y_CENTER, BLOCK_SIZE, BLOCK_SIZE))
        self.food = self._create_food()
        self.score = 0

    def _play_step(self):
        game_over = False
        self.now = pygame.time.get_ticks()
        if self.now - self.last_move_time > MOVE_INTERVAL:
            self.last_move_time = self.now

            if self.direction == 'RIGHT':
                x_new = self.snake_body[0].x + BLOCK_SIZE
                y_new = self.snake_body[0].y
            elif self.direction == 'LEFT':
                x_new = self.snake_body[0].x - BLOCK_SIZE
                y_new = self.snake_body[0].y
            elif self.direction == 'UP':
                x_new = self.snake_body[0].x 
                y_new = self.snake_body[0].y - BLOCK_SIZE
            elif self.direction == 'DOWN':
                x_new = self.snake_body[0].x 
                y_new = self.snake_body[0].y + BLOCK_SIZE
            
            new_head = pygame.Rect(x_new, y_new, BLOCK_SIZE, BLOCK_SIZE)
            self.snake_body.insert(0, new_head)
            if self.snake_body[0].colliderect(self.food):
                self.score += 1
                self.food = self._create_food()
            else:
                self.snake_body.pop()

            for i in range(1, len(self.snake_body)):
                if self.snake_body[0].colliderect(self.snake_body[i]):
                    game_over = True
                    return game_over, self.score

            if self.snake_body[0].left < 0 or self.snake_body[0].right > WIDTH or self.snake_body[0].top < 0 or self.snake_body[0].bottom > HEIGHT:
                game_over = True
                return game_over, self.score

        self.screen.fill(BLACK)
        for i in self.snake_body:
            pygame.draw.rect(self.screen,GREEN,i)
        pygame.draw.rect(self.screen,RED,self.food)
        pygame.display.flip()
        self.clock.tick(FPS)

        return game_over, self.score

if __name__ == '__main__':
    game = SnakeGame()

    running = True
    while running:
        game_over, score = game._play_step()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RIGHT and game.direction != 'LEFT':
                    game.direction = 'RIGHT'
                elif event.key == pygame.K_LEFT and game.direction != 'RIGHT':
                    game.direction = 'LEFT'
                elif event.key == pygame.K_UP and game.direction != 'DOWN':
                    game.direction = 'UP'
                elif event.key == pygame.K_DOWN and game.direction != 'UP':
                    game.direction = 'DOWN'
        
        if game_over:
            running = False

pygame.quit()