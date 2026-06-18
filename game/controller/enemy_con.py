class Enemy_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, player_model, dt):
        """Обновляет состояние противника: логику движения к игроку и синхронизацию с view."""
        # Перемещаем модель в сторону игрока
        self.model.move_towards(player_model.X, player_model.Y, dt)
        # Синхронизируем позицию view с новыми координатами из модели
        self.view.update_position(self.model.X, self.model.Y)