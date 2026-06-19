from typing import Dict


def resolve_damage(base_damage: int, attack_type: str, defender_vulnerability: str, parry_active: bool) -> Dict[str, int]:
    """Чистая функция расчёта урона.

    Возвращает словарь: {damage, was_parried, effective_damage}
    """

    was_parried = False
    if parry_active:
        was_parried = True
        return {"damage": base_damage, "was_parried": was_parried, "effective_damage": 0}

    effective = base_damage
    if attack_type == defender_vulnerability:
        effective = int(base_damage * 1.5)

    return {"damage": base_damage, "was_parried": was_parried, "effective_damage": effective}

