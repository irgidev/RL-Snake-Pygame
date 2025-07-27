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
HUD_HEIGHT = 60


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("RL Snake Game")
        self.clock = pygame.time.Clock()
        self.games_played = 0
        self.reset()
        
    def _create_food(self):
        while True:
            random_food = pygame.Rect(random.randrange(0,WIDTH, BLOCK_SIZE),random.randrange(HUD_HEIGHT,HEIGHT, BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
            if random_food not in self.snake_body:
                return random_food

    def reset(self):
        self.games_played += 1
        self.snake_body = []
        self.direction = 'RIGHT'
        self.last_move_time = pygame.time.get_ticks()
        for i in range(3):
            self.snake_body.append(pygame.Rect(X_CENTER - (BLOCK_SIZE * i),Y_CENTER, BLOCK_SIZE, BLOCK_SIZE))
        self.food = self._create_food()
        self.score = 0

    def _play_step(self, action):
        self.reward = 0
        game_over = False
        self.now = pygame.time.get_ticks()
        if self.now - self.last_move_time > MOVE_INTERVAL:
            self.last_move_time = self.now
            
            directions_clockwise = ['RIGHT', 'DOWN', 'LEFT', 'UP']
            idx = directions_clockwise.index(self.direction)

            if action[1] == 1:
                new_idx = (idx + 1) % 4
                self.direction = directions_clockwise[new_idx]
            elif action[2] == 1:
                new_idx = (idx - 1) % 4
                self.direction = directions_clockwise[new_idx]

            head = self.snake_body[0]
            x_new, y_new = head.x, head.y
            if self.direction == 'RIGHT':
                x_new += BLOCK_SIZE
            elif self.direction == 'LEFT':
                x_new -= BLOCK_SIZE
            elif self.direction == 'UP':
                y_new -= BLOCK_SIZE
            elif self.direction == 'DOWN':
                y_new += BLOCK_SIZE

            new_head = pygame.Rect(x_new, y_new, BLOCK_SIZE, BLOCK_SIZE)
            self.snake_body.insert(0, new_head)
            if self.snake_body[0].colliderect(self.food):
                self.reward = 10
                self.score += 1
                self.food = self._create_food()
            else:
                self.snake_body.pop()

            for i in range(1, len(self.snake_body)):
                if self.snake_body[0].colliderect(self.snake_body[i]):
                    self.reward = -10
                    game_over = True
                    return game_over, self.score, self.reward

            if self.snake_body[0].left < 0 or self.snake_body[0].right > WIDTH or self.snake_body[0].top < HUD_HEIGHT or self.snake_body[0].bottom > HEIGHT:
                self.reward = -10
                game_over = True
                return game_over, self.score, self.reward

        self.screen.fill(BLACK)
        for i in self.snake_body:
            pygame.draw.rect(self.screen,GREEN,i)
        pygame.draw.rect(self.screen,RED,self.food)

        text_surface = self.font.render(f"Score: {self.score}", True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)
        self.screen.blit(text_surface, text_rect)

        games_text_surface = self.font.render(f"Games: {self.games_played}", True, (255, 255, 255))
        games_text_rect = games_text_surface.get_rect()
        games_text_rect.topleft = (10, 30)

        pygame.draw.line(self.screen, (255,255,255), (0,HUD_HEIGHT-2), (WIDTH, HUD_HEIGHT-2), 2)

        self.screen.blit(games_text_surface, games_text_rect)

        pygame.display.flip()
        self.clock.tick(FPS)

        return game_over, self.score, self.reward

if __name__ == '__main__':
    game = SnakeGame()

    running = True
    while running:
        game_over, score, reward = game._play_step([1,0,0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if game_over:
            game.reset()

pygame.quit()