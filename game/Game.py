import pygame
import config
import random


class Atom:
    def __init__(self, color):
        self.color = color
        self.x = self.random_position()
        self.y = self.random_position()
        self.vx = 0
        self.vy = 0

    @staticmethod
    def random_position():
        return round(random.random() * config.screen_resolution[0] + 1)

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen, size):
        pygame.draw.line(screen, self.color, (self.x, self.y - 1), (self.x, self.y + 2), abs(size))
