import torch
import random
import pygame
from collections import deque
from game import SnakeGame, BLOCK_SIZE
from model import Linear_QNet, QTrainer
from plot import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(19, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):

        head = game.snake_body[0]
        
        point_l = (head.x - BLOCK_SIZE, head.y)
        point_r = (head.x + BLOCK_SIZE, head.y)
        point_u = (head.x, head.y - BLOCK_SIZE)
        point_d = (head.x, head.y + BLOCK_SIZE)
        point_ul = (head.x - BLOCK_SIZE, head.y - BLOCK_SIZE)
        point_ur = (head.x + BLOCK_SIZE, head.y - BLOCK_SIZE)
        point_dl = (head.x - BLOCK_SIZE, head.y + BLOCK_SIZE)
        point_dr = (head.x + BLOCK_SIZE, head.y + BLOCK_SIZE)

        dir_l = game.direction == 'LEFT'
        dir_r = game.direction == 'RIGHT'
        dir_u = game.direction == 'UP'
        dir_d = game.direction == 'DOWN'

        state = [
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_d)) or 
            (dir_l and game.is_collision(point_u)),

            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            game.is_collision(point_r),
            game.is_collision(point_l),
            game.is_collision(point_u),
            game.is_collision(point_d),
            game.is_collision(point_ur),
            game.is_collision(point_ul),
            game.is_collision(point_dr),
            game.is_collision(point_dl),

            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            game.food.x < game.snake_body[0].x,
            game.food.x > game.snake_body[0].x,
            game.food.y < game.snake_body[0].y,
            game.food.y > game.snake_body[0].y
        ]

        return torch.tensor(state, dtype=torch.float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states,actions,rewards,next_states,dones)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()

    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        done, score, reward = game._play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()