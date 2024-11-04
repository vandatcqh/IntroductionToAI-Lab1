import pygame
from pygame.sprite import Sprite


class Number(Sprite):
    def __init__(self, *groups, x, y, index):
        super().__init__(*groups)
        index_str = f"{index:02d}"
        self.image = pygame.image.load(f'img/number-{index_str}.png')
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.x = x
        self.y = y
        self.index = index

class Stone(Sprite):
    def __init__(self, *groups, x, y, game=None, number_group=None, index=None):
        super().__init__(*groups)
        self.game = game
        self.sprite = pygame.image.load('img/stone.png')
        self.sprite = pygame.transform.scale(self.sprite, [64, 64])
        self.image = self.sprite
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.x = x
        self.y = y
        self.number = None
        self.index = index  # Weight of the stone
        if number_group is not None and index is not None:
            self.number = Number(number_group, x=x, y=y, index=index)

    def can_move(self, move):
        target_x, target_y = self.x + move[0] // 64, self.y + move[1] // 64
        target = target_y, target_x
        curr = self.y, self.x
        target_elem = self.game.puzzle[target]
        if not isinstance(target_elem.obj, Stone):
            curr_elem = self.game.puzzle[curr]
            self.rect.y, self.rect.x = target[0] * 64, target[1] * 64
            self.y, self.x = target
            if self.number:
                self.number.rect.y, self.number.rect.x = self.rect.y, self.rect.x
                self.number.y, self.number.x = self.y, self.x
            curr_elem.char = '-' if not curr_elem.ground else 'X'
            curr_elem.obj = None
            target_elem.char = '@' if not target_elem.ground else '$'
            target_elem.obj = self
            self.update_sprite()
            return self.index  # Return the weight of the stone
        return 0  # Return 0 if the stone can't move

    def update_sprite(self):
        self.image = self.sprite 

    def __del__(self):
        if self.number:
            self.number.kill()
        self.kill()


class Obstacle(Stone):
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y)
        self.image = pygame.image.load('img/wall.png')
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
