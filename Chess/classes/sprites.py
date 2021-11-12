import pygame


class Piece_Sprite(pygame.sprite.Sprite):
    def __init__(self, picture, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y