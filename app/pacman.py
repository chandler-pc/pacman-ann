import pygame
import time

class Pacman:
    def __init__(self, x, y, size, speed, maze):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self._speed = speed
        self.direction = -1
        self.next_direction = -1
        self.last_x = x
        self.last_y = y
        self.maze = maze
        self.direction_timer = 0
        self.direction_attempt_time = 1  # tiempo en segundos para intentar cambiar de dirección

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.size, self.size))

    def set_direction(self, key):
        if key == pygame.K_LEFT:
            self.next_direction = 0
        elif key == pygame.K_RIGHT:
            self.next_direction = 1
        elif key == pygame.K_UP:
            self.next_direction = 2
        elif key == pygame.K_DOWN:
            self.next_direction = 3
        self.direction_timer = time.time()

    def move(self):
        self.last_x = self.x
        self.last_y = self.y

        # Intentar cambiar a la siguiente dirección durante un tiempo específico
        if self.next_direction != -1 and time.time() - self.direction_timer <= self.direction_attempt_time:
            if self.next_direction == 0 and not self.will_collide(-self.speed * 1 / 60, 0):
                self.direction = 0
                self.next_direction = -1
            elif self.next_direction == 1 and not self.will_collide(self.speed * 1 / 60, 0):
                self.direction = 1
                self.next_direction = -1
            elif self.next_direction == 2 and not self.will_collide(0, -self.speed * 1 / 60):
                self.direction = 2
                self.next_direction = -1
            elif self.next_direction == 3 and not self.will_collide(0, self.speed * 1 / 60):
                self.direction = 3
                self.next_direction = -1

        # Mover en la dirección actual
        if self.direction == 0 and not self.will_collide(-self.speed * 1 / 60, 0):
            self.x -= self.speed * 1 / 60
        elif self.direction == 1 and not self.will_collide(self.speed * 1 / 60, 0):
            self.x += self.speed * 1 / 60
        elif self.direction == 2 and not self.will_collide(0, -self.speed * 1 / 60):
            self.y -= self.speed * 1 / 60
        elif self.direction == 3 and not self.will_collide(0, self.speed * 1 / 60):
            self.y += self.speed * 1 / 60

    def on_collision(self):
        self.x = self.last_x
        self.y = self.last_y

    def will_collide(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy
        return self.maze.check_collision(next_x, next_y, self.size)