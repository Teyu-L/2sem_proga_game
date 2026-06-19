from dataclasses import dataclass, field
from typing import List, Tuple, Any


@dataclass
class EnemyData:
    """Чистые данные врага (внутри пакета game.models).

    Без логики — только состояние.
    """

    hp: int
    max_hp: int
    damage: int
    speed: float
    vulnerability: str  # 'steel' или 'silver'
    attacks: List[str] = field(default_factory=list)
    pos: Tuple[int, int] = (0, 0)
    room_id: Any = None

