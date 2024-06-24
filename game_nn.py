import random
import pygame
import numpy as np
from maze import Maze
from pacman import Pacman

class Game_NN:
    def __init__(self, nn, time_simulation=30, infinite_time=False):
        pygame.init()

        self.PACMAN_SIZE = 20
        self.BlOCK_SIZE = 32
        self.WIDTH, self.HEIGHT = 28*self.BlOCK_SIZE, 31*self.BlOCK_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pacman con Red Neuronal")

        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        self.maze = Maze(self.screen, self.BlOCK_SIZE)
        self.initial_x, self.initial_y = 7 * self.BlOCK_SIZE, 1 * self.BlOCK_SIZE
        while self.maze.maze[int(self.initial_y/self.BlOCK_SIZE)][int(self.initial_x/self.BlOCK_SIZE)] == '1' or self.maze.maze[int(self.initial_y/self.BlOCK_SIZE)][int(self.initial_x/self.BlOCK_SIZE)] == '=' or self.maze.maze[int(self.initial_y/self.BlOCK_SIZE)][int(self.initial_x/self.BlOCK_SIZE)] == 'X':
            self.initial_x, self.initial_y = random.randint(0,27) *self.BlOCK_SIZE, random.randint(0,30)*self.BlOCK_SIZE
        self.pacman = Pacman(self.initial_x, self.initial_y, self.PACMAN_SIZE, 100)
        self.pacman_speed = 100

        self.running = True

        self.clock = pygame.time.Clock()

        self.points = 0
        self.nn = nn

        self.time_simulation = time_simulation
        self.infinite_time = infinite_time    
        
        self.previous_direction = None
        self.change_count = 0  # Contador de cambios de dirección
        self.time_since_last_reward = 0  # Tiempo desde la última recompensa por cambio de dirección
        self.min_time_between_rewards = 1  # Tiempo mínimo entre recompensas por cambio de dirección (en segundos)

        
    def run(self):
        while self.running and self.time_simulation > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            state = self.get_state()
            action = self.nn.predict(state)

            direction = np.argmax(action)
            if direction == 0:
                self.pacman.set_direction(pygame.K_LEFT)
            elif direction == 1:
                self.pacman.set_direction(pygame.K_RIGHT)
            elif direction == 2:
                self.pacman.set_direction(pygame.K_UP)
            elif direction == 3:
                self.pacman.set_direction(pygame.K_DOWN)

            # Premio por cambio de dirección
            self.time_since_last_reward += 1 / 60  # Incrementar el tiempo desde la última recompensa
            if self.previous_direction is not None and self.previous_direction != direction:
                if self.time_since_last_reward >= self.min_time_between_rewards:
                    reward = np.clip(4 - self.change_count, 0, 4)  # Utilizar np.clip para asegurar el rango
                    self.points += reward
                    self.change_count += 1
                    self.time_since_last_reward = 0  # Reiniciar el tiempo desde la última recompensa
                    if reward > 0:
                        print(f"Change direction reward: {reward:.2f}")
            self.previous_direction = direction  # Actualizar la dirección anterior
            
            self.screen.fill(self.BLACK)
            self.pacman.move()
            check_point = self.maze.check_point(self.pacman.x, self.pacman.y, self.pacman.size)
            if check_point[0]:
                self.points += check_point[1]
            if self.maze.check_collision(self.pacman.x, self.pacman.y, self.pacman.size):
                self.pacman.on_collision()

            self.maze.draw_maze()
            self.pacman.draw(self.screen)
            pygame.display.flip()
            self.time_simulation -= 1 * 1/60
            if self.infinite_time:
                self.time_simulation = 1
                print("No time limit")
            else:
                print(f"Time remaining: {self.time_simulation:.2f}", end="\r")
            self.clock.tick(60)
        pygame.quit()

    def get_state(self):
        state = np.zeros((1, 6))
        state[0][0] = self.pacman.x
        state[0][1] = self.pacman.y
        state[0][2] = self.pacman.direction
        state[0][3] = self.points
        closest_point = self.maze.get_closest_point(self.pacman.x, self.pacman.y)
        state[0][4] = closest_point[0]
        state[0][5] = closest_point[1]
        return state.flatten()
