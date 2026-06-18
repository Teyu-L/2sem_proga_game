"""
Генератор тайловой карты на основе результатов BSP алгоритма.
Алгоритм: преобразует комнаты и коридоры из BSP в тайловую сетку.
"""

import core.settings as settings


class TilemapGenerator:
    """
    Генерирует тайловую карту из комнат и коридоров, полученных от BSP.
    Работает в тайловых координатах.
    """
    
    def __init__(self, grid_width, grid_height):
        """
        Args:
            grid_width: ширина сетки в тайлах
            grid_height: высота сетки в тайлах
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        # Инициализируем карту с пустыми тайлами (стены)
        self.tilemap = [[settings.TILE_EMPTY for _ in range(grid_width)] 
                        for _ in range(grid_height)]
    
    def generate(self, rooms, corridors):
        """
        Генерирует тайловую карту на основе комнат и коридоров.
        
        Args:
            rooms: список объектов pygame.Rect (комнаты в тайловых координатах)
            corridors: список объектов pygame.Rect (коридоры в тайловых координатах)
        
        Returns:
            2D список, где каждый элемент - тип тайла
        """
        # Сначала заполняем коридоры (чтобы не перекрывались комнатами)
        for corridor in corridors:
            self._fill_rect(corridor, settings.TILE_CORRIDOR)
        
        # Затем заполняем комнаты
        for room in rooms:
            self._fill_rect(room, settings.TILE_FLOOR)
        
        return self.tilemap
    
    def _fill_rect(self, rect, tile_type):
        """
        Заполняет прямоугольник тайлами указанного типа.
        Проверяет границы сетки.
        
        Args:
            rect: pygame.Rect с координатами в тайлах (x, y, width, height)
            tile_type: тип тайла для заполнения
        """
        x, y, width, height = rect.x, rect.y, rect.width, rect.height
        
        # Убеждаемся, что не выходим за границы сетки
        x_max = min(x + width, self.grid_width)
        y_max = min(y + height, self.grid_height)
        x = max(0, x)
        y = max(0, y)
        
        for ty in range(y, y_max):
            for tx in range(x, x_max):
                self.tilemap[ty][tx] = tile_type
    
    def get_tile(self, tile_x, tile_y):
        """
        Получает тип тайла по координатам сетки.
        Возвращает TILE_EMPTY, если координаты вне границ.
        """
        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            return self.tilemap[tile_y][tile_x]
        return settings.TILE_EMPTY
    
    def is_walkable(self, tile_x, tile_y):
        """Проверяет, проходимо ли на указанном тайле."""
        tile_type = self.get_tile(tile_x, tile_y)
        return tile_type in (settings.TILE_FLOOR, settings.TILE_CORRIDOR)
    
    def world_to_tile(self, world_x, world_y):
        """Преобразует мировые координаты в тайловые."""
        return int(world_x // settings.TILE_SIZE), int(world_y // settings.TILE_SIZE)
    
    def tile_to_world(self, tile_x, tile_y):
        """Преобразует тайловые координаты в мировые."""
        return tile_x * settings.TILE_SIZE, tile_y * settings.TILE_SIZE
    
    def is_tile_walkable_at_world_pos(self, world_x, world_y):
        """Проверяет, проходима ли позиция в мировых координатах."""
        tile_x, tile_y = self.world_to_tile(world_x, world_y)
        return self.is_walkable(tile_x, tile_y)
