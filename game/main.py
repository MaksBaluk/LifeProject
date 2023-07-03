import pygame
import config
from Game import Atom

pygame.init()

screen = pygame.display.set_mode(config.screen_resolution)
clock = pygame.time.Clock()

atoms = []


def create_atoms(number, color):
    group = []
    for _ in range(number):
        group.append(Atom(color))
        atoms.append(group[-1])
    return group


def rule(atoms1, atoms2, g):
    for a in atoms1:
        fx = 0
        fy = 0
        for b in atoms2:
            dx = a.x - b.x
            dy = a.y - b.y
            d_squared = dx * dx + dy * dy
            if 0 < d_squared < 6400:
                inv_d = 1 / d_squared ** 0.5
                fx += g * dx * inv_d
                fy += g * dy * inv_d
        a.vx = (a.vx + fx) * 0.5
        a.vy = (a.vy + fy) * 0.5
        a.move()
        a.x = max(0, min(a.x, config.Width))
        a.y = max(0, min(a.y, config.Height))
        if a.x in (0, config.Width):
            a.vx *= -1
        if a.y in (0, config.Height):
            a.vy *= -1


red = create_atoms(100, "red")
green = create_atoms(100, "green")
yellow = create_atoms(100, "yellow")


def main():
    run = True
    while run:
        screen.fill(pygame.Color('black'))
        # rule(red, red, 0.1)
        # rule(red, yellow, -0.15)
        # rule(yellow, yellow, -0.1)
        # rule(green,red,0.125)
        # rule(green,yellow,0.125)
        # rule(green,green,0.125)
        rule(green, green, -0.32)
        rule(green, red, -0.17)
        rule(green, yellow, 0.34)
        rule(red, red, -0.10)
        rule(red, green, -0.34)
        rule(yellow, yellow, 0.15)
        rule(yellow, green, -0.20)
        for a in atoms:
            a.draw(screen, 7)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
