import pygame
from models.level_mod import Level_Model
from views.level import Level_View
from models.player_mod import Player_Model
from views.player import Player_View
from controller.player_controller import PlayerController
from models.combat_state import CombatState
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

    # 1. Генерируем уровень (подземелье и тайловую карту)
    level_model = Level_Model()
    level_view = Level_View(level_model)

    # 2. Инициализируем игрока
    player_model = Player_Model()
    
    # Спавним игрока на случайной проходимой позиции
    spawn_pos = level_model.get_random_walkable_position()
    player_model.X, player_model.Y = spawn_pos

    player_view = Player_View(player_model.X, player_model.Y)
    combat_state = CombatState()
    player_controller = PlayerController(player_model, player_view, level_model.tilemap)

    # 3. Инициализируем камеру
    camera = Camera(width=WIDTH, height=HEIGHT)
    # Перемещаем камеру на игрока сразу при спавне, чтобы не было резкого скачка в первом кадре
    camera.x = player_model.X - WIDTH / 2
    camera.y = player_model.Y - HEIGHT / 2

    # 4. Опционально: включаем отрисовку сетки для отладки
    # level_view.set_show_grid(True)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # Для отладки: нажми G чтобы включить/отключить сетку
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                level_view.tilemap_view.show_grid = not level_view.tilemap_view.show_grid

        keys = pygame.key.get_pressed()

        # Обновление логики игрока через новый контроллер и ввод
        player_controller.update(dt, events, keys, combat_state)

        # Обновление камеры (плавно догоняет игрока)
        camera.update(player_model.X, player_model.Y, level_model.map_width, level_model.map_height)

        # Отрисовка
        screen.fill((20, 20, 20)) # Темная пустота за пределами подземелья
        
        level_view.render(screen, camera)
        player_view.render(screen, camera)

        pygame.display.flip()

if __name__ == "__main__":
    main()