import pygame


class Floor(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        if x <= 15:
            self.image = pygame.image.load('img/floor.png')
        else:
            self.image = pygame.image.load('img/sidefloor.png')
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def __del__(self):
        self.kill()

class Switch(Floor):
    def __init__(self, *groups, x, y):
        super().__init__(*groups, x=x, y=y)
        self.image = pygame.image.load('img/switch.png')
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
