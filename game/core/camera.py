import core.settings

class Camera:
    """
    Камера, привязана к игроку.
    """
    def __init__(self, width, height):
        """
        Инициализирует камеру.

        Args:
            width (int): Ширина видимой области (экрана).
            height (int): Высота видимой области (экрана).
        """
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target_x, target_y, map_width, map_height):
        """
        Обновляет положение камеры, чтобы она была сфокусирована на цели,
        но не выходила за пределы карты.

        Args:
            target_x (float): X-координата цели в мире.
            target_y (float): Y-координата цели в мире.
            map_width (int): Общая ширина карты.
            map_height (int): Общая высота карты.
        """
        # Плавно двигаем камеру к цели
        desired_x = target_x - self.width / 2
        desired_y = target_y - self.height / 2
        
        self.x += (desired_x - self.x) * 0.1
        self.y += (desired_y - self.y) * 0.1

        # Ограничиваем движение камеры границами карты
        self.x = max(0, self.x)
        self.y = max(0, self.y)
        self.x = min(self.x, map_width - self.width)
        self.y = min(self.y, map_height - self.height)

    def world_to_screen(self, wx, wy):
        """Преобразует мировые координаты в координаты на экране."""
        return wx - self.x, wy - self.y
