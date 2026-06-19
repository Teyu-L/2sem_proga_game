from typing import Any, Tuple
from models.player_state import PlayerState
from models.sign_data import SignData
from models.combat_state import CombatState
from controller.input_manager import InputManager
from system.sign_resolver import SignResolver
from system.combat_resolver import resolve_damage


class PlayerController:
    """Связывает InputManager, PlayerState, SignResolver и View.

    - Получает команды от `InputManager.process`.
    - Проверяет возможность каста через `SignResolver.can_cast`.
    - Обновляет `PlayerState` (мана, кулдауны, парирование и т.д.).
    - Делегирует визуальные эффекты во View через простые вызовы.
    """

    def __init__(self, player_model, player_view, game_map):
        # player_model — существующий Player_Model (физика/коллизии)
        # player_view — объект для отрисовки игрока
        self.model = player_model
        self.view = player_view
        self.state = PlayerState(pos=(player_model.X, player_model.Y))
        self.input = InputManager()
        self.signs = {}  # id -> SignData
        self.sign_resolver = SignResolver()
        self.game_map = game_map

    def register_sign(self, sign: SignData):
        self.signs[sign.id] = sign

    def update(self, dt: float, events, key_state, combat_state: CombatState):
        cmds = self.input.process(events, key_state)

        # Механика перемещения: преобразуем в скорость и применяем через существующий модельный API
        mx, my = cmds.get("move", (0, 0))
        speed = 200
        vx = mx * speed
        vy = my * speed
        self.model.move(vx, vy)
        self.model.update(dt, self.game_map)
        # синхронизируем позицию в PlayerState
        self.state.pos = (self.model.X, self.model.Y)

        # Парирование
        if cmds.get("parry"):
            combat_state.parry_active = True
            combat_state.parry_time_left = 0.25

        # Атака (ЛКМ)
        if cmds.get("attack"):
            # Простая атака: рассчитываем урон и применяем к ближайшему врагу (логика упрощена)
            # В реальной игре здесь выбирается цель и вызывается CombatResolver
            pass

        # Каст знака (Q)
        if cmds.get("cast_sign"):
            sign_id = self.state.active_sign
            sign = self.signs.get(sign_id)
            if sign:
                can, reason = self.sign_resolver.can_cast(self.state, sign)
                if can:
                    # Целевую позицию можно получать от мыши через view/движок; здесь заглушка
                    mouse_world_pos = (int(self.state.pos[0] + 1), int(self.state.pos[1]))
                    res = self.sign_resolver.cast(self.state, sign, mouse_world_pos, self.game_map)
                    # Если эффект нанес урон — применяем его через CombatResolver на стороне контроллера
                    if res.get("success") and res.get("effect") and "affected" in res["effect"]:
                        eff = res["effect"]
                        for target in eff["affected"]:
                            # Здесь нужно найти врага по координатам — это делает архитектура выше
                            # Мы просто демонстрируем применение урона к CombatState.player_hp (для примера)
                            dmg = resolve_damage(eff["damage"], eff["type"], "silver", combat_state.parry_active)
                            combat_state.player_hp = max(0, combat_state.player_hp - dmg["effective_damage"])
                    # View должен отрисовать визуальный эффект — вызываем метод view.spawn_sign_effect
                    if hasattr(self.view, "spawn_sign_effect"):
                        self.view.spawn_sign_effect(sign_id, self.state.pos)

        # Смена оружия
        if cmds.get("change_weapon") is not None:
            self.state.weapon = cmds.get("change_weapon")

        # Смена активного знака (Tab+1..5)
        if cmds.get("select_sign") is not None:
            self.state.active_sign = cmds.get("select_sign")

        # Обновление кулдаунов и парирования
        # Уменьшаем оставшиеся кулдауны
        for k in list(self.state.cooldowns.keys()):
            self.state.cooldowns[k] = max(0.0, self.state.cooldowns[k] - dt)

        # Парирование
        if combat_state.parry_active:
            combat_state.parry_time_left -= dt
            if combat_state.parry_time_left <= 0:
                combat_state.parry_active = False
                combat_state.parry_time_left = 0.0

        # Каст
        if self.state.casting_sign is not None:
            self.state.casting_time_left -= dt
            if self.state.casting_time_left <= 0:
                # Завершаем каст — применяем эффект мгновенно
                sign_id = self.state.casting_sign
                sign = self.signs.get(sign_id)
                if sign:
                    mouse_world_pos = (int(self.state.pos[0] + 1), int(self.state.pos[1]))
                    res = self.sign_resolver.cast(self.state, sign, mouse_world_pos, self.game_map)
                    if hasattr(self.view, "spawn_sign_effect"):
                        self.view.spawn_sign_effect(sign_id, self.state.pos)
                self.state.casting_sign = None
                self.state.casting_time_left = 0.0

        # Синхронизируем позицию для View
        if hasattr(self.view, "rect"):
            self.view.rect.centerx = self.model.X
            self.view.rect.centery = self.model.Y

