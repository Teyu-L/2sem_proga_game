import pygame
import core
class Player_Model ():
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

    def update (self, dt):
        pass

    def attack(self):
        pass