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

# Создание спрайтов
all_sprites = pygame.sprite.Group()
player_view = views.player.Player_view()

all_sprites.add(player_view)

running = True
while running:
    
    # Держим цикл на правильной скорости
    clock.tick(core.settings.FPS)
    # Ввод процесса (события)
    
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    
    # Отрисовка
    screen.fill(core.settings.BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
