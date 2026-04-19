import pygame
import core
class Player_Model ():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(core.settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = core.settings.WIDTH / 2
        self.rect.bottom = core.settings.HEIGHT - 10
        self.speedx = 0