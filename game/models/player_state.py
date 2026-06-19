from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


@dataclass
class PlayerState:
    """Чистые данные состояния игрока. Без логики.

    Поля:
    - hp, max_hp: здоровье
    - mana, max_mana: мана
    - weapon: текущее оружие (1,2 - мечи; 3 - арбалет)
    - active_sign: номер активного знака (1..5)
    - cooldowns: словарь кулдаунов по ключам (в секундах)
    - parry_active / parry_time_left: состояние парирования
    - pos: позиция в мире (x, y)
    - velocity: текущая скорость (vx, vy)
    - casting: информация о текущем касте (sign_id и оставшееся время)
    """

    hp: int = 100
    max_hp: int = 100
    mana: int = 50
    max_mana: int = 50
    weapon: int = 1
    active_sign: int = 1
    cooldowns: Dict[str, float] = field(default_factory=dict)
    parry_active: bool = False
    parry_time_left: float = 0.0
    pos: Tuple[float, float] = (0.0, 0.0)
    velocity: Tuple[float, float] = (0.0, 0.0)
    casting_sign: Optional[int] = None
    casting_time_left: float = 0.0

