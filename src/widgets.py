import pygame
from pygame_widgets.button import Button

from .events import *

class Label:
    def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
        self.image = self.font.render(text, 1, color)
        self.max_width = self.image.get_width()
        self.total_height = self.image.get_height()
        self.rect = pygame.Rect(x, y, self.max_width + 10, self.total_height + 10)
        self.window = window
        self.transparency = transparency

    def set_text(self, new_text, font_size, color='black'):
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
        self.image = self.font.render(new_text, 1, color)
        self.draw()

    def set_moves(self, new_text, font_size, color='black'):
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
        self.image = self.font.render(new_text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect.width = max(130, w)
        self.rect.height = max(40, h)
        self.draw()

    def draw(self):
        pygame.draw.rect(
            self.window,
            pygame.Color('blue'),
            (self.rect.x,
             self.rect.y,
             self.rect.width,
             self.rect.height)
        )
        pygame.draw.rect(
            self.window,
            (100, 100, 0),
            (self.rect.x,
             self.rect.y,
             self.rect.width,
             self.rect.height),
            width=3
        )
        text_pos_x = (self.rect.width - self.image.get_width()) // 2 + self.rect.x
        text_pos_y = (self.rect.height - self.image.get_height()) // 2 + self.rect.y
        self.window.blit(self.image, (text_pos_x, text_pos_y))


class MultilineLabel(Label):
    def __init__(self, window, text, x, y, font_size, transparency=False, color='black'):
        super().__init__(window, text, x, y, font_size, transparency, color)
        self.set_text(text, font_size, color)

    def reset(self, text=''):
        self.set_text(f'{text}', 20)
        pygame.display.update()

    def set_text(self, new_text, font_size, color='black'):
        self.font = pygame.font.SysFont('Verdana', font_size, bold=True)
       
        self.lines = new_text.split('\n')
        wrapped_lines = []

       
        max_chars_per_line = 200 
        for line in self.lines:
            if len(line) > max_chars_per_line:
                for i in range(0, len(line), max_chars_per_line):
                    wrapped_lines.append(line[i:i + max_chars_per_line])
            else:
                wrapped_lines.append(line)

        self.lines = wrapped_lines
        self.images = [self.font.render(line, 1, color) for line in self.lines]
        self.max_width = max(image.get_width() for image in self.images) if self.images else 0
        self.total_height = sum(image.get_height() for image in self.images) + (len(self.lines) - 1) * (font_size // 2)
        self.rect = pygame.Rect(self.x, self.y, self.max_width + 10, self.total_height + 10)
        self.draw()

    def draw(self):
        transparent_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )
        transparent_surface.set_alpha(110)
        transparent_surface.fill((0, 0, 200))
        if not self.transparency:
            pygame.draw.rect(
                self.window,
                (191, 236, 255),
                (self.rect.x,
                 self.rect.y,
                 self.rect.width,
                 self.rect.height),
                 border_radius=10
            )
        pygame.draw.rect(
            self.window,
            (55, 175, 225),
            (self.rect.x,
             self.rect.y,
             self.rect.width,
             self.rect.height),
            width=5,
            border_radius=10
        )
      
        total_text_height = sum(image.get_height() for image in self.images)
        total_spacing = (len(self.images) - 1) * (self.font.get_height() // 2)
        offset = self.rect.y + (self.rect.height - (total_text_height + total_spacing)) // 2

        for image in self.images:
            text_pos_x = self.rect.x + (self.rect.width - image.get_width()) // 2
            text_pos_y = offset
            self.window.blit(image, (text_pos_x, text_pos_y))
            offset += image.get_height() + (self.font.get_height() // 2)


def sidebar_widgets(window):
    prev_button = Button(
        window, 1030, 12, 22, 40, text='<', radius=2,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(PREVIOUS_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(191, 236, 255)
    )
    label = Label(window, f'Level 0', 1055, 10, 30)
    next_button = Button(
        window, 1188, 12, 22, 40, text='>', radius=2,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(NEXT_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(191, 236, 255)
    )
    restart = Button(
        window, 1055, 130, 130, 40, text='Restart', radius=5,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(RESTART_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(55, 175, 225),      
        hoverColour=(0, 255, 0),  
        pressedColour=(255, 0, 0),
        textColour=(255, 255, 255)
    )
    ucs_button = Button(
        window, 1055, 220, 130, 40, text='Run UCS', radius=5,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_UCS_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(55, 175, 225),       
        hoverColour=(0, 255, 0),   
        pressedColour=(255, 0, 0), 
        textColour=(255, 255, 255)
    )
    astarman_button = Button(
        window, 1055, 280, 130, 40, text='Run A*', radius=5,
        font=pygame.font.SysFont('Verdana', 18, bold=True),
        onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_ASTARMAN_EVENT)),
        borderColor='black', borderThickness=2,
        colour=(55, 175, 225),       
        hoverColour=(0, 255, 0),   
        pressedColour=(255, 0, 0), 
        textColour=(255, 255, 255)
    )
    moves = Label(window, f' Moves - 0 ', 1055, 75, 20)
    paths = MultilineLabel(window, f'ALG\nANS\nPath', 64, 0, 20)
    return {
        'restart': restart,
        'moves_label': moves,
        'prev_button': prev_button,
        'next_button': next_button,
        'label': label,
        'ucs': ucs_button,
        'paths': paths,
        'astarman': astarman_button,
    }
