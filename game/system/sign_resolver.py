from typing import Dict, Tuple, Optional, Any
from models.sign_data import SignData
from models.player_state import PlayerState


class SignStrategy:
    """Интерфейс стратегии исполнения знака.

    Метод `apply` выполняет чистую логику применения знака и возвращает
    структуру с результатами (напр., список поражённых координат и урон).
    """

    def apply(self, sign: SignData, caster: PlayerState, target_pos: Tuple[int, int], game_map: Any) -> Dict:
        raise NotImplementedError()


class FireballStrategy(SignStrategy):
    def apply(self, sign: SignData, caster: PlayerState, target_pos: Tuple[int, int], game_map: Any) -> Dict:
        # Пример: прямолинейный снаряд с взрывом в aoe_radius
        # Логика возвращает список координат попадания и базовый урон
        affected = [target_pos]
        damage = sign.base_power
        return {"affected": affected, "damage": damage, "type": sign.damage_type}


class ShieldStrategy(SignStrategy):
    def apply(self, sign: SignData, caster: PlayerState, target_pos: Tuple[int, int], game_map: Any) -> Dict:
        # Щит — не наносит урон, а даёт эффект; возвращаем мета-информацию
        return {"shield_amount": sign.base_power, "duration": 3.0}


class SignResolver:
    """Класс, реализующий чистую логику каста знаков.

    - Не зависит от движка, работает только с PlayerState, SignData и чистыми данными карты.
    - Поддерживает регистрируемые стратегии для расширяемости.

    Комментарий: SignResolver проверяет, хватает ли маны, не на кулдауне ли знак,
    резервирует ману/ставит кулдаун в `PlayerState.cooldowns`, и вызывает стратегию.
    """

    def __init__(self):
        self.strategies: Dict[str, SignStrategy] = {}
        # Регистрируем базовые стратегии
        self.register_strategy("fireball", FireballStrategy())
        self.register_strategy("shield", ShieldStrategy())

    def register_strategy(self, key: str, strategy: SignStrategy):
        self.strategies[key] = strategy

    def can_cast(self, caster: PlayerState, sign: SignData) -> Tuple[bool, str]:
        # Проверка маны
        if caster.mana < sign.mana_cost:
            return False, "not_enough_mana"
        # Проверка кулдауна
        cd = caster.cooldowns.get(f"sign_{sign.id}", 0.0)
        if cd > 0:
            return False, "on_cooldown"
        # Если уже кастуется другой знак
        if caster.casting_sign is not None and caster.casting_time_left > 0:
            return False, "already_casting"
        return True, "ok"

    def cast(self, caster: PlayerState, sign: SignData, target_pos: Tuple[int, int], game_map: Any) -> Dict:
        """Попытка кастовать знак: проверяет ресурсы, обновляет модель и вызывает стратегию.

        Возвращает словарь с результатом; не выполняет визуальных эффектов.

        Алгоритм:
        1. Проверить `can_cast`.
        2. Если у знака есть `cast_time` > 0, установить поля `casting_sign` и `casting_time_left` в `caster`.
        3. Если `cast_time` == 0, сразу применить стратегию, уменьшить ману и выставить кулдаун.
        """

        ok, reason = self.can_cast(caster, sign)
        if not ok:
            return {"success": False, "reason": reason}

        # Если есть время кастования, ставим статус кастинга и не применяем эффект сразу
        if sign.cast_time > 0:
            caster.casting_sign = sign.id
            caster.casting_time_left = sign.cast_time
            # резервируем ману сразу (чтобы предотвратить спам)
            caster.mana -= sign.mana_cost
            return {"success": True, "casting": True, "sign_id": sign.id}

        # мгновенный каст
        caster.mana -= sign.mana_cost
        caster.cooldowns[f"sign_{sign.id}"] = sign.cooldown

        strategy = self.strategies.get(sign.strategy_key)
        if not strategy:
            return {"success": False, "reason": "no_strategy"}

        result = strategy.apply(sign, caster, target_pos, game_map)

        # Если эффект наносит урон, используем CombatResolver для учёта уязвимостей
        if "damage" in result and "affected" in result:
            # Возвращаем структуру с инфо; применение урона происходит вне SignResolver
            return {"success": True, "effect": result}

        return {"success": True, "effect": result}

