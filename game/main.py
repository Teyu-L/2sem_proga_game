import pygame
import core.settings
from models import player_mod
import views.player
from controller import player_con
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


player_model = player_mod.Player_Model()
player_controller = player_con.Player_Controller(player_model, player_view)

running = True
while running:
    dt = clock.tick(core.settings.FPS) / 1000.0

    keys = pygame.key.get_pressed()
    player_controller.handle_input(keys, dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    
    # Отрисовка
    screen.fill(core.settings.BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
