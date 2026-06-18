import pygame
import sys
from models.level_mod import Level_Model
from views.level import Level_View
from models.player_mod import Player_Model
from views.player import Player_View
from controller.player_con import Player_Controller
from core.camera import Camera

# Пытаемся взять настройки окна, иначе задаем по умолчанию
try:
    import core.settings as settings
    WIDTH, HEIGHT = settings.WIDTH, settings.HEIGHT
except (ImportError, AttributeError):
    WIDTH, HEIGHT = 1280, 720

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wither: the potion trip")
    clock = pygame.time.Clock()

    # 1. Генерируем подземелье
    level_model = Level_Model(map_width=2000, map_height=2000)
    level_view = Level_View(level_model)

    # 2. Инициализируем игрока
    player_model = Player_Model()
    
    # Спавним игрока строго в центре первой попавшейся случайной комнаты
    start_room = level_model.get_random_room()
    if start_room:
        player_model.X, player_model.Y = start_room.center

    player_view = Player_View(player_model.X, player_model.Y)
    player_controller = Player_Controller(player_model, player_view)

    # 3. Инициализируем камеру
    camera = Camera(width=WIDTH, height=HEIGHT)
    # Перемещаем камеру на игрока сразу при спавне, чтобы не было резкого скачка в первом кадре
    camera.x = player_model.X - WIDTH / 2
    camera.y = player_model.Y - HEIGHT / 2

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Обновление логики (obstacles пока None, поэтому ходим сквозь стены)
        player_controller.handle_input(keys, dt, obstacles=None)

        # Обновление камеры (плавно догоняет игрока)
        camera.update(player_model.X, player_model.Y, level_model.map_width, level_model.map_height)

        # Отрисовка
        screen.fill((20, 20, 20)) # Темная пустота за пределами подземелья
        
        level_view.render(screen, camera)
        player_view.render(screen, camera)

        pygame.display.flip()

if __name__ == "__main__":
    main()