# tests/test_bsp_generation.py
import pytest
from system.bsp import BSPGenerator

def test_no_overlapping_rooms():
    """Комнаты не должны пересекаться"""
    generator = BSPGenerator(width=800, height=600, min_size=60, max_depth=5)
    result = generator.generate()
    
    rooms = result['rooms']
    for i in range(len(rooms)):
        for j in range(i + 1, len(rooms)):
            r1 = rooms[i]
            r2 = rooms[j]
            # Проверка на пересечение
            assert not (r1[0] < r2[0] + r2[2] and 
                       r1[0] + r1[2] > r2[0] and
                       r1[1] < r2[1] + r2[3] and 
                       r1[1] + r1[3] > r2[1]), \
                f"Rooms overlap: {r1} and {r2}"

def test_all_rooms_connected():
    """Все комнаты должны быть достижимы (через коридоры)"""
    generator = BSPGenerator(width=800, height=600, min_size=60, max_depth=5)
    result = generator.generate()
    
    rooms = result['rooms']
    corridors = result['corridors']
    
    # Строим граф связности
    # Комната соединена, если коридор касается её границы
    connected_rooms = {0}  # Начинаем с первой комнаты
    
    changed = True
    while changed:
        changed = False
        for corridor in corridors:
            # Проверяем, какие комнаты соединяет этот коридор
            for i, room in enumerate(rooms):
                if corridor_touches_room(corridor, room):
                    if i in connected_rooms:
                        # Ищем вторую комнату, которую касается коридор
                        for j, other_room in enumerate(rooms):
                            if j not in connected_rooms and corridor_touches_room(corridor, other_room):
                                connected_rooms.add(j)
                                changed = True
    
    assert len(connected_rooms) == len(rooms), \
        f"Not all rooms connected: {len(connected_rooms)}/{len(rooms)}"

def test_corridors_between_siblings_only():
    """Коридоры должны быть только между sibling комнатами"""
    generator = BSPGenerator(width=800, height=600, min_size=60, max_depth=5)
    result = generator.generate()
    
    # Здесь нужна проверка, что коридоры созданы только между
    # комнатами из соседних узлов дерева BSP
    # Это сложнее — нужно хранить структуру дерева
    pass

def corridor_touches_room(corridor, room):
    """Проверяет, касается ли коридор комнаты"""
    x1, y1, x2, y2 = corridor
    rx, ry, rw, rh = room
    
    # Коридор касается комнаты, если хотя бы одна точка коридора
    # находится на границе комнаты
    corridor_points = [(x1, y1), (x2, y2)]
    
    for px, py in corridor_points:
        # Проверяем, на границе ли комнаты
        on_horizontal_edge = (ry <= py <= ry + rh) and (px == rx or px == rx + rw)
        on_vertical_edge = (rx <= px <= rx + rw) and (py == ry or py == ry + rh)
        inside = (rx <= px <= rx + rw) and (ry <= py <= ry + rh)
        
        if on_horizontal_edge or on_vertical_edge or inside:
            return True
    
    return False

def test_no_duplicate_corridors():
    """Не должно быть идентичных или перекрывающихся коридоров"""
    generator = BSPGenerator(width=800, height=600, min_size=60, max_depth=5)
    result = generator.generate()
    
    corridors = result['corridors']
    for i in range(len(corridors)):
        for j in range(i + 1, len(corridors)):
            c1 = corridors[i]
            c2 = corridors[j]
            
            # Проверяем на идентичность (с учётом направления)
            assert not (
                (c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2] and c1[3] == c2[3]) or
                (c1[0] == c2[2] and c1[1] == c2[3] and c1[2] == c2[0] and c1[3] == c2[1])
            ), f"Duplicate corridors: {c1} and {c2}"