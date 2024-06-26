import pygame
import os
import numpy as np

class Maze:
    def __init__(self, screen, BlOCK_SIZE):
        self.maze = None
        self.BLOCK_SIZE = BlOCK_SIZE
        self.screen = screen
        self.points_position = []
        data_path = os.path.join('data', "maze.txt")
        with open(data_path, "r") as file:
            maze = file.read().split("\n")
            for line in range(len(maze)):
                maze[line] = maze[line].split(" ")
                for col in range(len(maze[line])):
                    try:
                        maze[line][col] = int(maze[line][col])
                        maze[line][col] = '1'
                    except:
                        if maze[line][col] == '.' or maze[line][col] == '+':
                            self.points_position.append((col, line))
            self.maze = maze

    def draw_maze(self):
        for row in range(31):
            for col in range(28):
                if self.maze[row][col] == '1':
                    pygame.draw.rect(self.screen, (0,0,255), (col * self.BLOCK_SIZE, row * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))
                if self.maze[row][col] == '.':
                    pygame.draw.circle(self.screen, (255,255,255), (col * self.BLOCK_SIZE + self.BLOCK_SIZE//2, row * self.BLOCK_SIZE + self.BLOCK_SIZE//2), 3)
                if self.maze[row][col] == '+':
                    pygame.draw.circle(self.screen, (255,255,0), (col * self.BLOCK_SIZE + self.BLOCK_SIZE//2, row * self.BLOCK_SIZE + self.BLOCK_SIZE//2), 5)
                if self.maze[row][col] == '=':
                    pygame.draw.rect(self.screen, (255,255,255), (col * self.BLOCK_SIZE, row * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE//2))

    def check_collision(self, x, y, pacman_size):
        corners = [
            (x, y),
            (x + pacman_size, y),
            (x, y + pacman_size),
            (x + pacman_size, y + pacman_size)
        ]
        for _, corner in enumerate(corners):
            corner_x, corner_y = corner
            row = int(corner_y // self.BLOCK_SIZE)
            col = int(corner_x // self.BLOCK_SIZE)
            pygame.draw.circle(self.screen, (255,0,0), (corner_x, corner_y), 1)
            if self.maze[row][col] == '1':
                return True
        return False
    
    def check_point(self, x, y, pacman_size):
        corners = [
            (x, y),
            (x + pacman_size, y),
            (x, y + pacman_size),
            (x + pacman_size, y + pacman_size)
        ]
        for _, corner in enumerate(corners):
            corner_x, corner_y = corner
            row = int(corner_y // self.BLOCK_SIZE)
            col = int(corner_x // self.BLOCK_SIZE)
            if self.maze[row][col] == '.':
                self.maze[row][col] = '0'
                return True,1
            if self.maze[row][col] == '+':
                self.maze[row][col] = '0'
                return True,10
        return False,0
    
    def get_closest_point(self, pacman_x, pacman_y):
        closest_point = None
        closest_distance = float("inf")
        for point in self.points_position:
            distance = np.sqrt((point[0] - pacman_x)**2 + (point[1] - pacman_y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_point = point
        return closest_point