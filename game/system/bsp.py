import random
import pygame

class BSPNode:
    """Узел дерева разбиения."""
    def __init__(self, x, y, width, height):
        # Rect теперь в тайловых координатах
        self.rect = pygame.Rect(x, y, width, height)
        self.left = None
        self.right = None
        self.room = None

class BSPGenerator:
    """
    Генератор подземелий с использованием алгоритма Binary Space Partitioning (BSP).
    Работает в тайловых координатах.
    """
    def __init__(self, map_width, map_height, min_room_size, corridor_width, iterations):
        self.map_width = map_width
        self.map_height = map_height
        self.min_room_size = min_room_size
        self.corridor_width = corridor_width
        self.iterations = iterations
        self.rooms = []
        self.corridors = []

    def generate(self):
        """Главный метод генерации. Возвращает (Список комнат, Список коридоров)."""
        root = BSPNode(0, 0, self.map_width, self.map_height)
        leaves = [root]

        # 1. Сплиттинг (Разбиение пространства)
        for _ in range(self.iterations):
            new_leaves = []
            # Проходимся по всем листьям и пытаемся их разбить
            for leaf in leaves:
                if leaf.left is None and leaf.right is None:
                    if self._split_node(leaf):
                        new_leaves.append(leaf.left)
                        new_leaves.append(leaf.right)
                    else:
                        # Если разбить не удалось, оставляем как есть
                        new_leaves.append(leaf)
            leaves = new_leaves

        # 2. Создание комнат и коридоров снизу вверх
        root.room = self._create_rooms(root)

        return self.rooms, self.corridors

    def _split_node(self, node):
        """Алгоритм разбиения одного узла на два дочерних."""
        if node.left or node.right:
            return False

        # Выбираем направление: горизонтально или вертикально
        split_horizontally = random.choice([True, False])
        
        # Корректируем направление, чтобы избежать слишком узких полос
        if node.rect.width > node.rect.height and node.rect.width / node.rect.height >= 1.25:
            split_horizontally = False
        elif node.rect.height > node.rect.width and node.rect.height / node.rect.width >= 1.25:
            split_horizontally = True

        # Проверяем, достаточно ли велик узел для разбиения
        dim = node.rect.height if split_horizontally else node.rect.width
        if dim < self.min_room_size * 2:
            return False # Слишком мал для создания двух дочерних узлов с min_room_size

        max_size = dim - self.min_room_size
        split_pos = random.randint(self.min_room_size, max_size)

        if split_horizontally:
            node.left = BSPNode(node.rect.x, node.rect.y, node.rect.width, split_pos)
            node.right = BSPNode(node.rect.x, node.rect.y + split_pos, node.rect.width, node.rect.height - split_pos)
        else:
            node.left = BSPNode(node.rect.x, node.rect.y, split_pos, node.rect.height)
            node.right = BSPNode(node.rect.x + split_pos, node.rect.y, node.rect.width - split_pos, node.rect.height)

        return True

    def _create_rooms(self, node):
        """Рекурсивное создание комнат в узлах-листьях и коридоров между ними."""
        if node.left or node.right:
            left_room = self._create_rooms(node.left) if node.left else None
            right_room = self._create_rooms(node.right) if node.right else None

            if left_room and right_room:
                self._create_corridor(left_room, right_room)
                return random.choice([left_room, right_room])
            return left_room or right_room
        else:
            # Узел является "листом" - создаем в нем комнату
            margin = 1  # 1-тайловый отступ от границ раздела
            min_dim = 3 # Минимальный размер комнаты в тайлах

            # Убедимся, что раздел достаточно велик для минимальной комнаты + отступов
            if node.rect.width < min_dim + 2 * margin or node.rect.height < min_dim + 2 * margin:
                return None

            # Размеры комнаты
            min_w = max(min_dim, int(node.rect.width * 0.5))
            min_h = max(min_dim, int(node.rect.height * 0.5))
            max_w = node.rect.width - 2 * margin
            max_h = node.rect.height - 2 * margin

            w = random.randint(min_w, max_w) if min_w <= max_w else max_w
            h = random.randint(min_h, max_h) if min_h <= max_h else max_h

            # Положение комнаты
            x = node.rect.x + random.randint(margin, node.rect.width - w - margin)
            y = node.rect.y + random.randint(margin, node.rect.height - h - margin)

            room = pygame.Rect(x, y, w, h)
            self.rooms.append(room)
            return room

    def _create_corridor(self, room1, room2):
        """Создает L-образные коридоры в тайловых координатах."""
        x1, y1 = room1.centerx, room1.centery
        x2, y2 = room2.centerx, room2.centery
        corridor_w = self.corridor_width

        if random.choice([True, False]):
            # Вариант 1: Горизонтальный → Вертикальный
            if x1 != x2:
                self.corridors.append(pygame.Rect(min(x1, x2), y1 - corridor_w // 2, abs(x1 - x2) + 1, corridor_w))
            if y1 != y2:
                self.corridors.append(pygame.Rect(x2 - corridor_w // 2, min(y1, y2), corridor_w, abs(y1 - y2) + 1))
        else:
            # Вариант 2: Вертикальный → Горизонтальный
            if y1 != y2:
                self.corridors.append(pygame.Rect(x1 - corridor_w // 2, min(y1, y2), corridor_w, abs(y1 - y2) + 1))
            if x1 != x2:
                self.corridors.append(pygame.Rect(min(x1, x2), y2 - corridor_w // 2, abs(x1 - x2) + 1, corridor_w))