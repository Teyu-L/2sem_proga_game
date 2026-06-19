import core.settings 
from system.collision import AABB, resolve_tilemap_collision

class Player_Model:
    def __init__(self):
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.attack_power = 10
        self.attack_speed = 1.0
        self.X = core.settings.WIDTH / 2
        self.Y = core.settings.HEIGHT - 50
        self.width = 30
        self.height = 30

    def move(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def take_damage(self, amount):
        pass

    def drink_elixir(self, elixir):
        pass

    def update(self, dt, tilemap=None):
        """
        Обновляет позицию игрока с проверкой коллизий с тайловой картой.
        
        Args:
            dt: дельта времени (в секундах)
            tilemap: объект Tilemap_Model для проверки коллизий
        """
        # Вычисляем предложенное движение
        dx = self.speedx * dt
        dy = self.speedy * dt

        if tilemap:
            rect = (self.X - self.width / 2, self.Y - self.height / 2, self.width, self.height)
            dx, dy = resolve_tilemap_collision(tilemap, rect, dx, dy)
            self.X += dx
            self.Y += dy
        else:
            self.X += dx
            self.Y += dy

    def attack(self):
        pass