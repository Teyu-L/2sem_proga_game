import pygame
import core.settings

class Enemy_View(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        # Задаем размер и цвет (красный для противников)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0)) 
        
        self.rect = self.image.get_rect()
        self.rect.centerx = start_x
        self.rect.centery = start_y
    
    def render(self, screen):
        """Отрисовка спрайта противника."""
        screen.blit(self.image, self.rect)

    def update_position(self, x, y):
        """Синхронизация позиции view с координатами модели."""
        self.rect.centerx = x
        self.rect.centery = y