import pygame
import config
from Game import Atom

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

atoms = []
atom_count = 200

# Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Розміри кнопок та текстового поля
button_width = 80
button_height = 30
field_width = 100
field_height = 30

# Позиція кнопок та текстового поля
button_x = screen_width // 2 - button_width // 2
button_y = screen_height - 80
field_x = screen_width // 2 - field_width // 2
field_y = screen_height - 120

# Шрифт
font = pygame.font.Font(None, 28)

# Значення для введення кількості атомів
input_value = str(atom_count)
input_active = False


class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()


class InputField:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def get_value(self):
        return self.text


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
                inv_d = 1 / (d_squared ** 0.5)
                fx += g * dx * inv_d
                fy += g * dy * inv_d
        a.vx = (a.vx + fx) * 0.5
        a.vy = (a.vy + fy) * 0.5
        a.move()
        a.x = max(0, min(a.x, screen_width))
        a.y = max(0, min(a.y, screen_height))
        if a.x == 0 or a.x == screen_width:
            a.vx *= -1
        if a.y == 0 or a.y == screen_height:
            a.vy *= -1


red = create_atoms(atom_count, "red")


def increase_atoms():
    global atom_count, red
    atom_count += 10
    red = create_atoms(atom_count, "red")


def decrease_atoms():
    global atom_count, red
    atom_count -= 10
    if atom_count < 0:
        atom_count = 0
    red = create_atoms(atom_count, "red")


def update_input_value():
    global input_value, input_active
    input_value = input_field.get_value()
    input_active = False


increase_button = Button(button_x, button_y, button_width, button_height, "+10", increase_atoms)
decrease_button = Button(button_x, button_y + 40, button_width, button_height, "-10", decrease_atoms)
input_field = InputField(field_x, field_y, field_width, field_height)
update_button = Button(field_x + field_width + 10, field_y, button_width, field_height, "Update", update_input_value)


def main():
    run = True

    while run:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_RETURN:
                    update_input_value()
                else:
                    input_field.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    input_active = input_field.rect.collidepoint(event.pos)

        rule(red, red, 0.1)

        for a in atoms:
            a.draw(screen, 7)

        pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, GRAY, (button_x, button_y + 40, button_width, button_height))
        pygame.draw.rect(screen, WHITE, (field_x, field_y, field_width, field_height))
        pygame.draw.rect(screen, GRAY, (field_x + field_width + 10, field_y, button_width, field_height))

        increase_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0)))
        decrease_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0)))
        update_button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0)))

        increase_button_text = font.render(increase_button.text, True, BLACK)
        decrease_button_text = font.render(decrease_button.text, True, BLACK)
        update_button_text = font.render(update_button.text, True, BLACK)
        input_text = font.render("Atoms:", True, WHITE)
        input_value_text = font.render(input_value, True, WHITE)

        screen.blit(increase_button_text, (button_x + button_width // 2 - increase_button_text.get_width() // 2,
                                           button_y + button_height // 2 - increase_button_text.get_height() // 2))
        screen.blit(decrease_button_text, (button_x + button_width // 2 - decrease_button_text.get_width() // 2,
                                           button_y + 40 + button_height // 2 - decrease_button_text.get_height() // 2))
        screen.blit(input_text, (field_x, field_y - input_text.get_height() - 10))
        screen.blit(input_value_text, (field_x + field_width // 2 - input_value_text.get_width() // 2,
                                        field_y + field_height // 2 - input_value_text.get_height() // 2))
        screen.blit(update_button_text, (field_x + field_width + 10 + button_width // 2 - update_button_text.get_width() // 2,
                                          field_y + field_height // 2 - update_button_text.get_height() // 2))

        pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
