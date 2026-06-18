import core.settings
from systems.collision import AABB

class Player_Model:
    def __init__(self):
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.attack_power = 10
        self.attack_speed = 1.0
        self.X = core.settings.WIDTH / 2
        self.Y = core.settings.HEIGHT - 50
        self.width = 50
        self.height = 40

    def move(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def take_damage(self, amount):
        pass

    def drink_elixir(self, elixir):
        pass

    def update(self, dt, obstacles=None):
        self.X += self.speedx * dt
        self.Y += self.speedy * dt

        if self.X < 0:
            self.X = 0
        elif self.X > core.settings.WIDTH:
            self.X = core.settings.WIDTH

        if self.Y < 0:
            self.Y = 0
        elif self.Y > core.settings.HEIGHT:
            self.Y = core.settings.HEIGHT
            
        # Проверка и разрешение коллизий AABB (после каждого движения)
        if obstacles:
            player_rect = (self.X - self.width / 2, self.Y - self.height / 2, self.width, self.height)
            for obs in obstacles:
                dx, dy = AABB.resolve(player_rect, obs)
                if dx != 0 or dy != 0:
                    self.X += dx
                    self.Y += dy
                    # Обновляем AABB после сдвига, чтобы корректно обработать следующие препятствия
                    player_rect = (self.X - self.width / 2, self.Y - self.height / 2, self.width, self.height)

    def attack(self):
        pass