from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class State(ABC):
    @abstractmethod
    def enter(self, context):
        pass

    @abstractmethod
    def exit(self, context):
        pass

    @abstractmethod
    def update(self, context, dt: float):
        pass


class FSM:
    def __init__(self, initial: State, context):
        self.current: Optional[State] = None
        self.context = context
        self.change_state(initial)

    def change_state(self, new_state: State):
        if self.current is not None:
            self.current.exit(self.context)
        self.current = new_state
        self.current.enter(self.context)

    def update(self, dt: float):
        if self.current is None:
            return
        next_state = self.current.update(self.context, dt)
        if next_state is not None:
            self.change_state(next_state)


class Patrol(State):
    def enter(self, context):
        pass

    def exit(self, context):
        pass

    def update(self, context, dt: float):
        if getattr(context, "player_in_sight", False):
            return Chase()
        return None


class Chase(State):
    def enter(self, context):
        pass

    def exit(self, context):
        pass

    def update(self, context, dt: float):
        if getattr(context, "in_attack_range", False):
            return Attack()
        if not getattr(context, "player_in_sight", False):
            return Patrol()
        return None


class Attack(State):
    def enter(self, context):
        context.attack_started = True

    def exit(self, context):
        context.attack_started = False

    def update(self, context, dt: float):
        if getattr(context, "attack_finished", False):
            if getattr(context, "player_in_sight", False):
                return Chase()
            return Patrol()
        return None


"""
FSM переключает состояния так:
- Patrol -> если игрок в поле зрения -> Chase
- Chase -> если в радиусе атаки -> Attack, если потеряли цель -> Patrol
- Attack -> по завершении переход к Chase или Patrol

Состояния используют только поля контекста (модели), поэтому FSM
независима от движка и легко тестируется.
"""

