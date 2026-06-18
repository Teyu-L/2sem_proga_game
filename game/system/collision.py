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