import pygame


class Spritesheet:
    def __init__(self, filename):
        self.filemane = filename
        self.sprite_sheet = pygame.image.load(filename)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        rect = pygame.Rect((x, y), (w, h))
        sprite.blit(self.sprite_sheet, (0, 0), rect)
        return sprite

    def parse_sprite(self, numberx, numbery):
        x = numberx * 16
        y = numbery * 16
        w = 16
        h = 16
        image = self.get_sprite(x, y, w, h)
        return image
