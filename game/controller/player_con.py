import pygame
import core.settings
import models

class Player_Controller ():
    def __init__(self, model, view):
        self.model = model
        self.view = view
    def handle_input(self, keys, mouse_buttons):
        

        if keys[pygame.K_w]:
            self.model.move(0,10)