import pygame
import config
import numpy as np
from Game import Pixel

pygame.init()

screen = pygame.display.set_mode(config.screen_resolution)
clock = pygame.time.Clock()


def apply_gravitational_force(pixels):
    num_pixels = len(pixels)
    dx = np.subtract.outer(pixels[:, 0], pixels[:, 0])
    dy = np.subtract.outer(pixels[:, 1], pixels[:, 1])
    distance = np.maximum(np.hypot(dx, dy), 1)
    force = config.G * np.outer(pixels[:, 2], pixels[:, 2]) / (distance ** 2)
    angle = np.arctan2(dy, dx)
    force_x = np.sum(force * np.cos(angle), axis=1)
    force_y = np.sum(force * np.sin(angle), axis=1)
    pixels[:, 3] += force_x / pixels[:, 2]
    pixels[:, 4] += force_y / pixels[:, 2]


def make_pixels(amount: int, create_pixel_func: callable, pixels: pygame.sprite.Group):
    for _ in range(amount):
        pixels.add(create_pixel_func())


def draw_pixels(pixels: list):
    for pixel in pixels:
        pixel.draw_pixel()


def update(pixels: list):
    for pixel in pixels:
        pixel.update()


def main():
    all_pixels = pygame.sprite.Group()
    make_pixels(2, lambda: Pixel(screen, pygame.Color('red')), all_pixels)
    make_pixels(2, lambda: Pixel(screen, pygame.Color('green')), all_pixels)

    while True:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pixels_array = np.array(
            [[pixel._x, pixel._y, pixel.mass, pixel.velocity_x, pixel.velocity_y] for pixel in all_pixels],
            dtype=np.float64)
        apply_gravitational_force(pixels_array)
        pixels_array[:, 0:2] += pixels_array[:, 3:5]
        for i, pixel in enumerate(all_pixels):
            pixel._x = pixels_array[i, 0]
            pixel._y = pixels_array[i, 1]
        all_pixels.update()

        all_pixels.draw(screen)

        pygame.display.set_caption("FPS :" + str(int(clock.get_fps())))
        pygame.display.flip()
        clock.tick(config.FPS)


if __name__ == '__main__':
    main()
