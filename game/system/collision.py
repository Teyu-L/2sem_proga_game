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


def get_tile_rects_for_rect(tilemap, rect):
    """
    Возвращает список прямоугольников, соответствующих непроходимым тайлам,
    которые пересекаются с областью rect.
    """
    x, y, w, h = rect
    tile_size = core.settings.TILE_SIZE

    min_tile_x = int((x - tile_size) // tile_size)
    min_tile_y = int((y - tile_size) // tile_size)
    max_tile_x = int((x + w + tile_size - 1) // tile_size)
    max_tile_y = int((y + h + tile_size - 1) // tile_size)

    obstacles = []
    for tile_y in range(min_tile_y, max_tile_y + 1):
        for tile_x in range(min_tile_x, max_tile_x + 1):
            if not tilemap.is_walkable(tile_x, tile_y):
                if 0 <= tile_x < tilemap.grid_width and 0 <= tile_y < tilemap.grid_height:
                    obstacles.append((tile_x * tile_size,
                                      tile_y * tile_size,
                                      tile_size,
                                      tile_size))
    return obstacles


def resolve_tilemap_collision(tilemap, rect, dx, dy):
    """
    Разрешает столкновение объекта с непроходимыми тайлами тайловой карты.
    Использует AABB для разрешения движения по X и Y отдельно.
    """
    x, y, w, h = rect

    if dx != 0:
        new_rect_x = (x + dx, y, w, h)
        for obstacle in get_tile_rects_for_rect(tilemap, new_rect_x):
            if AABB.check(new_rect_x, obstacle):
                dx = 0
                break

    if dy != 0:
        new_rect_y = (x + dx, y + dy, w, h)
        for obstacle in get_tile_rects_for_rect(tilemap, new_rect_y):
            if AABB.check(new_rect_y, obstacle):
                dy = 0
                break

    return dx, dy
