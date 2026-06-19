from typing import List, Tuple, Optional
import heapq


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int], room_mask: List[List[int]]) -> Optional[List[Tuple[int, int]]]:
    """
    A* для тайловой сетки с учётом принадлежности к комнате.

    grid: 0 = проходимо, 1 = стена
    room_mask: id комнаты для каждой клетки
    Враги не могут переходить в клетки с другим room_id.
    """

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    start_room = room_mask[start[1]][start[0]]

    def neighbors(node):
        x, y = node
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if grid[ny][nx] == 0 and room_mask[ny][nx] == start_room:
                    yield (nx, ny)

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    gscore = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for nb in neighbors(current):
            tentative_g = gscore[current] + 1
            if tentative_g < gscore.get(nb, 1e9):
                came_from[nb] = current
                gscore[nb] = tentative_g
                f = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_set, (f, tentative_g, nb))

    return None


"""
Комментарий: ограничение по room_mask не даёт врагам выходить в другие комнаты
или по коридорам, если коридоры отнесены к другим id.
"""

