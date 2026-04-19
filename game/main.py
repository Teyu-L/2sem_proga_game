import pygame
import core.settings
import models
import views.player
pygame.init()
pygame.mixer.init()

# инициализация дисплея
screen = pygame.display.set_mode((core.settings.WIDTH, core.settings.HEIGHT))
pygame.display.set_caption("Wither Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

player_view = views.player.Player_view()
all_sprites = pygame.sprite.Group()


running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(core.settings.FPS)
    # Ввод процесса (события)

    all_sprites.update()

    
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


screen.fill(core.settings.BLACK)

pygame.display.flip()
pygame.quit()
