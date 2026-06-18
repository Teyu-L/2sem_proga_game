import core.settings
import math # Для вычисления расстояния и нормализации вектора

class Enemy_Model:
    """
    Универсальный родительский класс для всех противников в игре.
    Определяет базовые характеристики и поведение, такие как здоровье, движение, атака и уязвимости.
    """

    def __init__(self, x=0, y=0, health=50, attack_power=5, attack_speed=1.0, speed=100,
                 vulnerabilities=None, immunities=None):
        """
        Инициализирует модель противника.

        Args:
            x (int/float): Начальная позиция по оси X.
            y (int/float): Начальная позиция по оси Y.
            health (int): Текущее и максимальное здоровье противника.
            attack_power (int): Сила атаки противника.
            attack_speed (float): Скорость атаки (атаки в секунду).
            speed (int): Скорость перемещения противника в пикселях в секунду.
            vulnerabilities (list): Список типов урона, к которым противник уязвим (например, ['silver', 'fire']).
            immunities (list): Список типов урона, к которым противник иммунен (например, ['poison']).
        """
        self.X = x
        self.Y = y
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.attack_speed = attack_speed
        self.speed = speed
        self.vulnerabilities = vulnerabilities if vulnerabilities is not None else []
        self.immunities = immunities if immunities is not None else []

    def move_towards(self, target_x, target_y, dt):
        """Перемещение противника в направлении заданных координат."""
        dx = target_x - self.X
        dy = target_y - self.Y
        distance = math.hypot(dx, dy)

        if distance > 0:
            # Нормализуем вектор и умножаем на скорость и dt
            self.X += (dx / distance) * self.speed * dt
            self.Y += (dy / distance) * self.speed * dt

    def take_damage(self, amount, damage_type=None):
        """Обработка получения урона с учетом иммунитетов и уязвимостей."""
        if damage_type in self.immunities:
            return  # Урон не наносится
            
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def is_alive(self):
        return self.health > 0