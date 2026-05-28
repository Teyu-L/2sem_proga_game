import core.settings

class Player_Model:
    def __init__(self):
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.attack_power = 10
        self.attack_speed = 1.0
        self.X = core.settings.WIDTH / 2
        self.Y = core.settings.HEIGHT - 50

    def move(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy

    def take_damage(self, amount):
        pass

    def drink_elixir(self, elixir):
        pass

    def update(self, dt):
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

    def attack(self):
        pass