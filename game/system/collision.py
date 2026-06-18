import core.settings


class AABB:
    """
    Реализация алгоритма AABB (Axis-Aligned Bounding Box) для проверки 
    и разрешения коллизий между объектами игры.
    """
    
    @staticmethod
    def check(rect1, rect2):
        """
        Проверяет столкновение двух прямоугольников.
        Входные данные:
        rect1, rect2: кортежи или списки вида (x, y, width, height)
        
        Выходные данные:
        True — столкновение есть
        False — столкновения нет
        """
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2

        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)

    @staticmethod
    def resolve(rect, obstacle):
        """Возвращает вектор (dx, dy) для выталкивания объекта rect из obstacle."""
        if not AABB.check(rect, obstacle):
            return 0, 0

        x1, y1, w1, h1 = rect
        x2, y2, w2, h2 = obstacle

        overlap_left = (x1 + w1) - x2
        overlap_right = (x2 + w2) - x1
        overlap_top = (y1 + h1) - y2
        overlap_bottom = (y2 + h2) - y1

        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left:
            return -overlap_left, 0
        elif min_overlap == overlap_right:
            return overlap_right, 0
        elif min_overlap == overlap_top:
            return 0, -overlap_top
        else:
            return 0, overlap_bottom


class TilemapCollision:
    """
    Система коллизий на основе тайловой карты.
    Проверяет, может ли объект занимать определённую позицию.
    """
    
    @staticmethod
    def check_rect_collision(tilemap, rect):
        """
        Проверяет, пересекается ли прямоугольник со стенами на тайловой карте.
        
        Args:
            tilemap: объект Tilemap_Model
            rect: кортеж (x, y, width, height) в мировых координатах
        
        Returns:
            True если есть столкновение со стеной, False если свободно
        """
        x, y, w, h = rect
        tile_size = core.settings.TILE_SIZE
        
        # Получаем координаты тайлов, которые занимает объект
        min_tile_x = int(x // tile_size)
        min_tile_y = int(y // tile_size)
        max_tile_x = int((x + w - 1) // tile_size)
        max_tile_y = int((y + h - 1) // tile_size)
        
        # Проверяем каждый тайл, который занимает объект
        for tile_y in range(min_tile_y, max_tile_y + 1):
            for tile_x in range(min_tile_x, max_tile_x + 1):
                if not tilemap.is_walkable(tile_x, tile_y):
                    return True  # Есть столкновение
        
        return False  # Столкновений нет
    
    @staticmethod
    def resolve_collision(tilemap, rect, dx, dy):
        """
        Разрешает коллизию путём перемещения объекта.
        Проверяет движение по X и Y отдельно.
        
        Args:
            tilemap: объект Tilemap_Model
            rect: кортеж (x, y, width, height) в мировых координатах
            dx, dy: смещение, которое нужно применить
        
        Returns:
            кортеж (new_dx, new_dy) - реально применённое смещение
        """
        x, y, w, h = rect
        
        # Пробуем движение только по X
        new_rect_x = (x + dx, y, w, h)
        if TilemapCollision.check_rect_collision(tilemap, new_rect_x):
            dx = 0
        
        # Пробуем движение только по Y
        new_rect_y = (x + dx, y + dy, w, h)
        if TilemapCollision.check_rect_collision(tilemap, new_rect_y):
            dy = 0
        
        return dx, dy
