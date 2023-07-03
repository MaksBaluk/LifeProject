import pygame
from random import randint
from config import screen_resolution
import numpy as np


class Pixel(pygame.sprite.Sprite):
    def __init__(self, screen, color):
        super().__init__()
        self.screen = screen
        self.color = color
        self._x = self.random_position()
        self._y = self.random_position()
        self.mass = 1
        self.velocity_x = 0
        self.velocity_y = 0
        self.image = pygame.Surface((5, 5))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self._x
        self.rect.y = self._y

    @staticmethod
    def random_position():
        return randint(0, screen_resolution[0])

    def update(self):
        self.rect.move_ip(self.velocity_x, self.velocity_y)
        self._x = self.rect.x
        self._y = self.rect.y

    def draw_pixel(self):
        self.screen.blit(self.image, self.rect.topleft)
