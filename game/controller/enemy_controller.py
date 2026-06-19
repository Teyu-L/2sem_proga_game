from typing import Tuple, Any
from models.enemy_data import EnemyData
from models.combat_state import CombatState
from system.fsm_enemy import FSM, Patrol
from system.pathfinding import astar
from system.combat_resolver import resolve_damage


class EnemyController:
    """Контроллер врага: связывает модель, алгоритмы и вид.

    - читает `EnemyData`
    - обновляет FSM (через FSM.update)
    - вызывает `astar` для получения пути
    - вызывает `resolve_damage` при нанесении урона
    """

    def __init__(self, enemy: EnemyData, view: Any, map_grid, room_mask):
        self.enemy = enemy
        self.view = view
        # map_grid и room_mask — чистые данные сетки (0/1) и id комнат
        self.map_grid = map_grid
        self.room_mask = room_mask
        # Контекст для FSM — можно использовать сам `enemy` или оградить доп. полями
        self.fsm = FSM(Patrol(), enemy)

    def update(self, dt: float, player_pos: Tuple[int, int], combat_state: CombatState):
        # Обновляем контекстные флаги, которые FSM использует для переходов
        ex, ey = self.enemy.pos
        px, py = player_pos
        dist = abs(ex - px) + abs(ey - py)
        self.enemy.player_in_sight = dist < 8  # пример порога видимости
        self.enemy.in_attack_range = dist <= 1

        # Обновляем FSM
        self.fsm.update(dt)

        # Если FSM решила преследовать — вычисляем путь и двигаем врага по нему
        if getattr(self.enemy, "player_in_sight", False) and not getattr(self.enemy, "in_attack_range", False):
            path = astar(self.map_grid, self.enemy.pos, player_pos, self.room_mask)
            if path and len(path) > 1:
                # следующий шаг — второй элемент пути (первый = текущая позиция)
                self.enemy.pos = path[1]

        # Если в радиусе атаки и атака готова — применяем урон через CombatResolver
        if getattr(self.enemy, "in_attack_range", False):
            attack_type = self.enemy.attacks[0] if self.enemy.attacks else "physical"
            res = resolve_damage(self.enemy.damage, attack_type, "silver", combat_state.parry_active)
            combat_state.player_hp = max(0, combat_state.player_hp - res["effective_damage"])

    def handle_player_action(self, action: str, combat_state: CombatState):
        """Обработка действий игрока: 'attack' или 'parry'.

        Контроллер не реализует логику урона — он передаёт информацию в
        `CombatState` и другие алгоритмы, которые уже используют `resolve_damage`.
        """
        if action == "parry":
            combat_state.parry_active = True
            combat_state.parry_time_left = 0.3
        elif action == "attack":
            # сюда можно положить логику нанесения урона по врагу
            pass

