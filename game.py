import pygame

from maze import Maze
from pacman import Pacman

class Game:
    def __init__(self):
        pygame.init()

        self.PACMAN_SIZE = 20
        self.BlOCK_SIZE = 32
        self.WIDTH, self.HEIGHT = 28*self.BlOCK_SIZE, 31*self.BlOCK_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pacman con Red Neuronal")

        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)

        self.pacman = Pacman(14*self.BlOCK_SIZE, 23*self.BlOCK_SIZE, self.PACMAN_SIZE, 100)
        self.pacman_speed = 100


        self.maze = Maze(self.screen,self.BlOCK_SIZE)
        self.running = True

        self.clock = pygame.time.Clock()

        self.points = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pacman.set_direction(pygame.K_LEFT)
                    if event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(pygame.K_RIGHT)
                    if event.key == pygame.K_UP:
                        self.pacman.set_direction(pygame.K_UP)
                    if event.key == pygame.K_DOWN:
                        self.pacman.set_direction(pygame.K_DOWN)

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
            self.clock.tick(60)
        
        pygame.quit()

