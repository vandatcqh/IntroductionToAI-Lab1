import numpy as np
import pygame

from .stone import Stone, Obstacle
from .floor import Floor, Switch
from .ares import Ares


class PuzzleElement:
    def __init__(self, char, obj=None, ground=None):
        self.char = char
        self.ground = ground
        self.obj = obj

    def __str__(self):
        return self.char


class Game:
    def __init__(self, window=None, width=1216, height=640, level=None, path=None):
        self.window = window
        self.level = level
        self.width = width
        self.height = height
        self.puzzle = np.empty((height // 64, width // 64), dtype=PuzzleElement)
        self.floor_group = pygame.sprite.Group()
        self.object_group = pygame.sprite.Group()
        self.ares_group = pygame.sprite.Group()
        self.switch_group = pygame.sprite.Group()
        self.number_group = pygame.sprite.Group()
        self.ares = None
        self.puzzle_size = None
        self.pad_x = 0
        self.pad_y = 0
        self.path = path or f'input/input-{level:02d}.txt'
        self.load_floor()
        self.load_puzzle()

    def __del__(self):
        self.clear_objects()

    def print_puzzle(self):
        for h in range(self.height // 64):
            for w in range(self.width // 64):
                if self.puzzle[h, w]:
                    print(self.puzzle[h, w].char, end=' ')
                else:
                    print(' ', end=' ')
            print(' ')

    def is_level_complete(self):
        stones_left = 0
        for h in range(self.height // 64):
            for w in range(self.width // 64):
                if self.puzzle[h, w] and self.puzzle[h, w].char == '@':
                    stones_left += 1
        return stones_left == 0

    def clear_objects(self):
        for sprite in self.object_group:
            del sprite
        for sprite in self.floor_group:
            del sprite
        for sprite in self.number_group:
            del sprite

    def load_floor(self):
        for i in range(self.width // 64):
            for j in range(self.height // 64):
                Floor(self.floor_group, x=i, y=j)

    def load_puzzle(self):
        try:
            with open(self.path) as f:
                lines = f.readlines()
                weights = list(map(int, lines[0].strip().split()))
                print(weights)
                grid_lines = lines[1:]
                self.puzzle_size = (len(grid_lines), len(grid_lines[0].rstrip('\n')))
                pad_x = (self.width // 64 - self.puzzle_size[1] - 2) // 2
                pad_y = (self.height // 64 - self.puzzle_size[0]) // 2
                self.pad_x, self.pad_y = pad_x, pad_y

            stone_index = 1  

            with open(self.path) as f:
                next(f)  
                for i, line in enumerate(f):
                    line = line.rstrip('\n')
                    for j, c in enumerate(line):
                        new_elem = PuzzleElement(c)
                        self.puzzle[i + pad_y, j + pad_x] = new_elem
                        if c == '#':  # tường
                            new_elem.obj = Obstacle(self.object_group, x=j + pad_x, y=i + pad_y)
                        elif c == '$':  # hộp
                            new_elem.obj = Stone(
                                self.object_group,
                                x=j + pad_x,
                                y=i + pad_y,
                                game=self,
                                number_group=self.number_group,
                                index=weights[stone_index-1]  
                            )
                            stone_index += 1  
                        elif c == '@':  
                            new_elem.obj = Ares(
                                self.object_group, self.ares_group,
                                x=j + pad_x, y=i + pad_y, game=self
                            )
                            self.ares = new_elem.obj
                        elif c == '.': 
                            new_elem.ground = Switch(self.switch_group, x=j + pad_x, y=i + pad_y)
                        elif c == '*':  
                            new_elem.ground = Switch(self.switch_group, x=j + pad_x, y=i + pad_y)
                            new_elem.obj = Stone(
                                self.object_group,
                                x=j + pad_x,
                                y=i + pad_y,
                                game=self,
                                number_group=self.number_group,
                                index=weights[stone_index-1]  
                            )
                            stone_index += 1  
                        elif c == '%':  
                            new_elem.obj = Ares(
                                self.object_group, self.ares_group,
                                x=j + pad_x, y=i + pad_y, game=self
                            )
                            new_elem.ground = Switch(self.switch_group, x=j + pad_x, y=i + pad_y)
                            self.ares = new_elem.obj
                        elif c not in ' -':
                            raise ValueError(
                                f'Invalid character on file {self.path}: {c}'
                            )
        except (OSError, ValueError) as e:
            print(f'{e}')
            self.clear_objects()
            return
