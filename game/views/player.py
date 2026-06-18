import pygame

class Player_View(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 200, 0)) # Зеленый цвет для игрока
        
        self.rect = self.image.get_rect()
        self.rect.centerx = start_x
        self.rect.centery = start_y
        
    def render(self, screen, camera):
        # Получаем экранные координаты центра
        screen_x, screen_y = camera.world_to_screen(self.rect.centerx, self.rect.centery)
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        screen.blit(self.image, draw_rect)