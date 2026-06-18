import pygame

class Level_View:
    def __init__(self, model):
        self.model = model
        self.room_color = (60, 60, 60)       # Темно-серый пол комнат
        self.corridor_color = (80, 80, 80)   # Чуть более светлые коридоры
        self.border_color = (120, 120, 120)  # Цвет стен (обводки)

    def render(self, screen, camera):
        # Сначала рисуем коридоры
        for corridor in self.model.corridors:
            screen_x, screen_y = camera.world_to_screen(corridor.x, corridor.y)
            rect = pygame.Rect(screen_x, screen_y, corridor.width, corridor.height)
            pygame.draw.rect(screen, self.corridor_color, rect)
            pygame.draw.rect(screen, self.border_color, rect, 2) # 2 - толщина обводки
            
        # Затем рисуем комнаты (поверх коридоров)
        for room in self.model.rooms:
            screen_x, screen_y = camera.world_to_screen(room.x, room.y)
            rect = pygame.Rect(screen_x, screen_y, room.width, room.height)
            pygame.draw.rect(screen, self.room_color, rect)
            pygame.draw.rect(screen, self.border_color, rect, 2)