import random
from controller.bsp import BSPGenerator
import core.settings

class Level_Model:
    """
    Модель игрового уровня. Отвечает за хранение данных о комнатах и коридорах.
    """
    def __init__(self, map_width=2000, map_height=2000, min_room_size=200, iterations=4):
        self.map_width = map_width
        self.map_height = map_height
        self.rooms = []
        self.corridors = []
        
        # Сразу генерируем уровень при создании объекта
        self.generate_level(min_room_size, iterations)

    def generate_level(self, min_room_size, iterations):
        """Инициализирует BSP-генератор и создает структуру уровня."""
        generator = BSPGenerator(self.map_width, self.map_height, min_room_size, iterations)
        self.rooms, self.corridors = generator.generate()

    def get_random_room(self):
        """Возвращает случайную комнату. Удобно для спавна игрока, врагов или лута."""
        return random.choice(self.rooms) if self.rooms else None