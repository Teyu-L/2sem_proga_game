from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CombatState:
    """Состояние боя — кулдауны, парирование и здоровье игрока.

    Это чистые данные; алгоритмы читают и обновляют их.
    """

    player_hp: int = 100
    player_max_hp: int = 100
    cooldowns: Dict[str, float] = field(default_factory=dict)
    parry_active: bool = False
    parry_time_left: float = 0.0

