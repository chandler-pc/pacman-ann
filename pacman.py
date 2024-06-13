import pygame

class Pacman:
    def __init__(self, x, y, size, speed):
        self.x = x + 6
        self.y = y + 6
        self.size = size
        self.speed = speed
        self._speed = speed
        self.direction = -1
        self.last_x = x
        self.last_y = y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0),
                         (self.x, self.y, self.size, self.size))

    def set_direction(self, key):
        if key == pygame.K_LEFT:
            self.direction = 0
        if key == pygame.K_RIGHT:
            self.direction = 1
        if key == pygame.K_UP:
            self.direction = 2
        if key == pygame.K_DOWN:
            self.direction = 3
        self.speed = self._speed

    def move(self):
        self.last_x = self.x
        self.last_y = self.y
        if self.direction == 0:
            self.x -= self.speed * 1/60
        if self.direction == 1:
            self.x += self.speed * 1/60
        if self.direction == 2:
            self.y -= self.speed * 1/60
        if self.direction == 3:
            self.y += self.speed * 1/60

    def on_collision(self):
        self.speed = 0
        self.x = self.last_x
        self.y = self.last_y
