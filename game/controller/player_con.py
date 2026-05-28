import pygame
import core.settings

class Player_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_input(self, keys, dt):
        speed = 200
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= speed
        if keys[pygame.K_s]:
            dy += speed
        if keys[pygame.K_a]:
            dx -= speed
        if keys[pygame.K_d]:
            dx += speed

        self.model.move(dx, dy)
        self.model.update(dt)

        self.view.rect.centerx = self.model.X
        self.view.rect.centery = self.model.Y