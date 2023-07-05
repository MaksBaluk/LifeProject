import pygame
import config
import random


class Atom:
    """class Atom create atom in simulation"""

    def __init__(self, color: str):
        self.color = color
        self.x = self.random_position()
        self.y = self.random_position()
        self.vx = 0
        self.vy = 0

    @staticmethod
    def random_position():
        return round(random.random() * config.Width + 1)

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen: pygame.Surface, size: int | float):
        pygame.draw.rect(screen, self.color, (self.x, self.y, size, size))
