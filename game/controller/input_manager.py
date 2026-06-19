import pygame
from typing import List, Dict, Any, Tuple


class InputManager:
    """Считывает события и состояние клавиш, переводит в команды.

    Как InputManager передаёт команды:
    - Метод `process` принимает список событий (pygame.event.get()) и
      массив состояния клавиш (pygame.key.get_pressed()).
    - Возвращает словарь команд, который затем читает `PlayerController`.

    Карта клавиш (по ТЗ):
    WASD - перемещение
    ЛКМ - атака, ПКМ - парирование
    E - взаимодействие, Space - dash
    R/F - быстрый доступ
    Q - каст активного знака
    Tab + 1-5 - смена активного знака
    1/2/3 - смена оружия
    Esc - меню
    """

    def __init__(self):
        # внутренний статус нажатия (например, Tab держится)
        self.tab_held = False

    def process(self, events: List[pygame.event.Event], key_state) -> Dict[str, Any]:
        cmds: Dict[str, Any] = {
            "move": (0, 0),
            "attack": False,
            "parry": False,
            "interact": False,
            "dash": False,
            "use_R": False,
            "use_F": False,
            "cast_sign": False,
            "select_sign": None,
            "change_weapon": None,
            "open_menu": False,
        }

        # движение по WASD — возвращаем вектор направления
        dx = 0
        dy = 0
        if key_state[pygame.K_w]:
            dy -= 1
        if key_state[pygame.K_s]:
            dy += 1
        if key_state[pygame.K_a]:
            dx -= 1
        if key_state[pygame.K_d]:
            dx += 1
        cmds["move"] = (dx, dy)

        # Tab держится?
        self.tab_held = key_state[pygame.K_TAB]

        # Обработка событий (KEYDOWN и MOUSEBUTTONDOWN)
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    cmds["open_menu"] = True
                elif e.key == pygame.K_e:
                    cmds["interact"] = True
                elif e.key == pygame.K_SPACE:
                    cmds["dash"] = True
                elif e.key == pygame.K_r:
                    cmds["use_R"] = True
                elif e.key == pygame.K_f:
                    cmds["use_F"] = True
                elif e.key == pygame.K_q:
                    cmds["cast_sign"] = True
                elif e.key == pygame.K_1:
                    if self.tab_held:
                        cmds["select_sign"] = 1
                    else:
                        cmds["change_weapon"] = 1
                elif e.key == pygame.K_2:
                    if self.tab_held:
                        cmds["select_sign"] = 2
                    else:
                        cmds["change_weapon"] = 2
                elif e.key == pygame.K_3:
                    if self.tab_held:
                        cmds["select_sign"] = 3
                    else:
                        cmds["change_weapon"] = 3
                elif e.key == pygame.K_4 and self.tab_held:
                    cmds["select_sign"] = 4
                elif e.key == pygame.K_5 and self.tab_held:
                    cmds["select_sign"] = 5

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    cmds["attack"] = True
                elif e.button == 3:
                    cmds["parry"] = True

        # Также можно обрабатывать удержание мыши для автоповторов и т.д.

        return cmds

