import random
from system import bsp as system_bsp
from system import tilemap_generator as tilemap_gen
import core
from models.tilemap_mod import Tilemap_Model

class Level_Model:
    """
    Модель игрового уровня. 
    Отвечает за генерацию структуры (комнаты, коридоры) и создание тайловой карты.
    """
    def __init__(self, grid_width=core.settings.GRID_WIDTH, 
                 grid_height=core.settings.GRID_HEIGHT,
                 min_room_size=core.settings.MIN_ROOM_SIZE,
                 corridor_width=core.settings.CORRIDOR_WIDTH,
                 iterations=4):
        # Размеры в тайлах
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # Размеры в пикселях (для совместимости)
        self.map_width = grid_width * core.settings.TILE_SIZE
        self.map_height = grid_height * core.settings.TILE_SIZE
        
        # Структура подземелья (комнаты и коридоры)
        self.rooms = []
        self.corridors = []
        
        # Тайловая карта
        self.tilemap = Tilemap_Model(grid_width, grid_height)
        
        # Генерируем уровень при создании объекта
        self.generate_level(min_room_size, corridor_width, iterations)

    def generate_level(self, min_room_size, corridor_width, iterations):
        """
        Генерирует структуру уровня (комнаты, коридоры) и создает тайловую карту.
        """
        # 1. Генерируем структуру подземелья через BSP
        generator = system_bsp.BSPGenerator(
            self.grid_width, 
            self.grid_height, 
            min_room_size,
            corridor_width,
            iterations
        )
        self.rooms, self.corridors = generator.generate()
        
        # 2. Генерируем тайловую карту на основе BSP результатов
        tilemap_generator_inst = tilemap_gen.TilemapGenerator(
            self.grid_width, 
            self.grid_height
        )
        tilemap_data = tilemap_generator_inst.generate(self.rooms, self.corridors)
        self.tilemap.update_from_tilemap_data(tilemap_data)

    def get_random_room(self):
        """Возвращает случайную комнату (pygame.Rect в тайловых координатах)."""
        return random.choice(self.rooms) if self.rooms else None
    
    def get_random_walkable_position(self):
        """
        Возвращает случайную проходимую позицию в мировых координатах.
        Полезно для спавна врагов, лута и т.д.
        """
        # Выбираем случайную проходимую клетку
        attempts = 0
        max_attempts = 100
        while attempts < max_attempts:
            tile_x = random.randint(0, self.grid_width - 1)
            tile_y = random.randint(0, self.grid_height - 1)
            if self.tilemap.is_walkable(tile_x, tile_y):
                return self.tilemap.tile_to_world(tile_x, tile_y)
            attempts += 1
        
        # Если не нашли, ищем первую проходимую позицию
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.tilemap.is_walkable(x, y):
                    return self.tilemap.tile_to_world(x, y)
        
        # Последняя надежда - центр карты
        return (self.map_width / 2, self.map_height / 2)