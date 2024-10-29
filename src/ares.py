import pygame
from pygame.sprite import Sprite

from .stone import Stone, Obstacle


class Ares(Sprite):
    def __init__(self, *groups, x, y, game):
        super().__init__(*groups)
        self.game = game
        self.up = pygame.image.load('img/aresU.png')
        self.up = pygame.transform.scale(self.up, [64, 64])
        self.down = pygame.image.load('img/aresD.png')
        self.down = pygame.transform.scale(self.down, [64, 64])
        self.left = pygame.image.load('img/aresL.png')
        self.left = pygame.transform.scale(self.left, [64, 64])
        self.right = pygame.image.load('img/aresR.png')
        self.right = pygame.transform.scale(self.right, [64, 64])
        self.image = self.down
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.x = x
        self.y = y

    def update(self, key=None):
        move = None
        if key:
            key = key.upper()
            if key == 'R':
                self.image = self.right
                move = (64, 0)
            elif key == 'L':
                self.image = self.left
                move = (-64, 0)
            elif key == 'U':
                self.image = self.up
                move = (0, -64)
            elif key == 'D':
                self.image = self.down
                move = (0, 64)
        if move:
            curr = self.y, self.x
            target = self.y + move[1] // 64, self.x + move[0] // 64
            target_elem = self.game.puzzle[target]
            if not (target_elem and target_elem.obj and isinstance(target_elem.obj, Obstacle)):
                is_box = isinstance(target_elem.obj, Stone)
                if not is_box or (is_box and target_elem.obj.can_move(move)):
                    curr_elem = self.game.puzzle[curr]
                    self.rect.y, self.rect.x = target[0] * 64, target[1] * 64
                    self.y, self.x = target
                    curr_elem.char = '-' if not curr_elem.ground else 'X'
                    curr_elem.obj = None
                    target_elem.char = '*' if not target_elem.ground else '%'
                    target_elem.obj = self
                    return 1
        return 0

    def __del__(self):
        self.kill()
