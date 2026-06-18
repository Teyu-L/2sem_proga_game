"""
Визуализация тайловой карты.
Отвечает за отрисовку тайлов на экран.
"""

import pygame
import core.settings


class Tilemap_View:
    """
    Представление (View) тайловой карты.
    Отрисовывает тайлы разных типов с использованием камеры.
    """
    
    def __init__(self, tilemap_model):
        """
        Args:
            tilemap_model: объект Tilemap_Model для получения данных
        """
        self.model = tilemap_model
        
        # Цвета для разных типов тайлов
        self.tile_colors = {
            core.settings.TILE_EMPTY: (30, 30, 30),      # Темно-серый - стены
            core.settings.TILE_FLOOR: (60, 60, 60),      # Серый - пол комнаты
            core.settings.TILE_CORRIDOR: (50, 50, 50),   # Темно-серый - коридор
        }
        
        # Цвет границ тайлов (для отладки, можно отключить)
        self.show_grid = False
        self.grid_color = (40, 40, 40)
    
    def render(self, screen, camera):
        """
        Отрисовывает видимую часть тайловой карты.
        
        Args:
            screen: pygame Surface для отрисовки
            camera: объект Camera для трансформации координат
        """
        # Получаем границы видимой области в тайловых координатах
        tile_size = core.settings.TILE_SIZE
        
        # Определяем видимые тайлы (с небольшим запасом для скорости)
        start_x = max(0, int(camera.x // tile_size) - 1)
        start_y = max(0, int(camera.y // tile_size) - 1)
        end_x = min(self.model.grid_width, 
                   int((camera.x + screen.get_width()) // tile_size) + 2)
        end_y = min(self.model.grid_height, 
                   int((camera.y + screen.get_height()) // tile_size) + 2)
        
        # Отрисовываем видимые тайлы
        for tile_y in range(start_y, end_y):
            for tile_x in range(start_x, end_x):
                tile_type = self.model.get_tile(tile_x, tile_y)
                self._render_tile(screen, camera, tile_x, tile_y, tile_type)
    
    def _render_tile(self, screen, camera, tile_x, tile_y, tile_type):
        """
        Отрисовывает один тайл.
        
        Args:
            screen: pygame Surface
            camera: объект Camera
            tile_x, tile_y: координаты тайла в сетке
            tile_type: тип тайла
        """
        tile_size = core.settings.TILE_SIZE
        
        # Преобразуем координаты тайла в мировые
        world_x = tile_x * tile_size
        world_y = tile_y * tile_size
        
        # Преобразуем в экранные координаты
        screen_x, screen_y = camera.world_to_screen(world_x, world_y)
        
        # Получаем цвет для типа тайла
        color = self.tile_colors.get(tile_type, (255, 0, 255))  # Magenta для неизвестных типов
        
        # Рисуем квадрат тайла
        rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
        pygame.draw.rect(screen, color, rect)
        
        # Рисуем сетку, если включено (для отладки)
        if self.show_grid:
            pygame.draw.rect(screen, self.grid_color, rect, 1)
    
    def set_show_grid(self, show):
        """Включает/отключает отрисовку сетки тайлов."""
        self.show_grid = show
