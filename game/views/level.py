import pygame
from .tilemap import Tilemap_View as TilemapViewClass

class Level_View:
    """
    Представление (View) уровня.
    Отвечает за визуализацию уровня (тайловая карта).
    """
    def __init__(self, level_model):
        """
        Args:
            level_model: объект Level_Model
        """
        self.level_model = level_model
        # Создаем представление для тайловой карты
        self.tilemap_view = TilemapViewClass(level_model.tilemap)

    def render(self, screen, camera):
        """
        Отрисовывает уровень на экран.
        
        Args:
            screen: pygame Surface
            camera: объект Camera для трансформации координат
        """
        # Отрисовываем тайловую карту
        self.tilemap_view.render(screen, camera)
    
    def set_show_grid(self, show):
        """Включает/отключает отрисовку сетки тайлов (для отладки)."""
        self.tilemap_view.set_show_grid(show)