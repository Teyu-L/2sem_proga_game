from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class SignData:
    """Данные описывающие знак — только параметры, без логики.

    Поля:
    - id: числовой идентификатор знака
    - name: название
    - mana_cost: стоимость маны
    - cooldown: кулдаун в секундах
    - base_power: базовый урон или сила эффекта
    - damage_type: строка, например 'fire', 'arcane'
    - cast_time: время произнесения в секундах (0 для мгновенных)
    - aoe_radius: радиус поражения в тайлах (0 для одиночных)
    - strategy_key: ключ для выбора стратегии выполнения (расширяемость)
    """

    id: int
    name: str
    mana_cost: int
    cooldown: float
    base_power: int
    damage_type: str
    cast_time: float = 0.0
    aoe_radius: int = 0
    strategy_key: str = "default"

