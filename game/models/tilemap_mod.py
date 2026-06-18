"""
Модель тайловой карты.
Отвечает за хранение и управление тайловой сеткой уровня.
"""

import core.settings


class Tilemap_Model:
    """
    Модель тайловой карты.
    Хранит данные о типах тайлов, размерах карты и предоставляет методы для работы с ней.
    """
    
    def __init__(self, grid_width, grid_height, tilemap_data=None):
        """
        Args:
            grid_width: ширина сетки в тайлах
            grid_height: высота сетки в тайлах
            tilemap_data: 2D список тайлов (если None, инициализируется пустой картой)
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.pixel_width = grid_width * core.settings.TILE_SIZE
        self.pixel_height = grid_height * core.settings.TILE_SIZE
        
        # Инициализируем карту
        if tilemap_data is None:
            self.tilemap = [[core.settings.TILE_EMPTY for _ in range(grid_width)] 
                           for _ in range(grid_height)]
        else:
            self.tilemap = tilemap_data
    
    def get_tile(self, tile_x, tile_y):
        """
        Получает тип тайла по координатам сетки.
        Возвращает TILE_EMPTY, если координаты вне границ.
        """
        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            return self.tilemap[tile_y][tile_x]
        return core.settings.TILE_EMPTY
    
    def set_tile(self, tile_x, tile_y, tile_type):
        """
        Устанавливает тип тайла по координатам.
        Проверяет границы.
        """
        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            self.tilemap[tile_y][tile_x] = tile_type
    
    def is_walkable(self, tile_x, tile_y):
        """Проверяет, проходимо ли на указанном тайле."""
        tile_type = self.get_tile(tile_x, tile_y)
        return tile_type in (core.settings.TILE_FLOOR, core.settings.TILE_CORRIDOR)
    
    def world_to_tile(self, world_x, world_y):
        """Преобразует мировые координаты в тайловые."""
        return int(world_x // core.settings.TILE_SIZE), int(world_y // core.settings.TILE_SIZE)
    
    def tile_to_world(self, tile_x, tile_y):
        """Преобразует тайловые координаты в центр тайла (мировые)."""
        return tile_x * core.settings.TILE_SIZE + core.settings.TILE_SIZE / 2, \
               tile_y * core.settings.TILE_SIZE + core.settings.TILE_SIZE / 2
    
    def get_walkable_neighbors(self, tile_x, tile_y):
        """Возвращает список проходимых соседних тайлов."""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = tile_x + dx, tile_y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    def update_from_tilemap_data(self, tilemap_data):
        """
        Обновляет карту новыми данными.
        Используется при переходе на новый уровень.
        """
        if len(tilemap_data) == self.grid_height and \
           len(tilemap_data[0]) == self.grid_width:
            self.tilemap = tilemap_data
