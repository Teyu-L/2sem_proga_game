import core.settings
from system.collision import TilemapCollision as TilemapCollisionClass

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
        # Вычисляем новую позицию
        new_x = self.X + self.speedx * dt
        new_y = self.Y + self.speedy * dt

        # Проверяем коллизии с тайловой картой, если она передана
        if tilemap:
            player_rect = (new_x - self.width / 2, new_y - self.height / 2, self.width, self.height)
            dx, dy = TilemapCollisionClass.resolve_collision(
                tilemap,
                (self.X - self.width / 2, self.Y - self.height / 2, self.width, self.height),
                self.speedx * dt,
                self.speedy * dt
            )
            self.X += dx
            self.Y += dy
        else:
            # Если тайловая карта не передана, просто обновляем позицию
            self.X = new_x
            self.Y = new_y

    def attack(self):
        pass