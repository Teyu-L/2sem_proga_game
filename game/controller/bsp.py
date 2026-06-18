import random
import pygame

class BSPNode:
    """Узел дерева разбиения."""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.left = None
        self.right = None
        self.room = None

class BSPGenerator:
    """
    Генератор подземелий с использованием алгоритма Binary Space Partitioning (BSP).
    """
    def __init__(self, map_width, map_height, min_room_size, iterations):
        self.map_width = map_width
        self.map_height = map_height
        self.min_room_size = min_room_size
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
            for leaf in leaves:
                if leaf.left is None and leaf.right is None:
                    # Пытаемся разбить узел на два
                    if self._split_node(leaf):
                        new_leaves.append(leaf.left)
                        new_leaves.append(leaf.right)
                    else:
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

        max_size = (node.rect.height if split_horizontally else node.rect.width) - self.min_room_size
        
        if max_size <= self.min_room_size:
            return False  # Узел слишком мал для дальнейшего разбиения

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
            # Узел является "листом" - создаем в нем комнату с небольшими отступами от границ (стен)
            w = random.randint(max(3, int(node.rect.width * 0.6)), max(3, node.rect.width - 2))
            h = random.randint(max(3, int(node.rect.height * 0.6)), max(3, node.rect.height - 2))
            
            x = node.rect.x + random.randint(1, max(1, node.rect.width - w - 1))
            y = node.rect.y + random.randint(1, max(1, node.rect.height - h - 1))
            
            room = pygame.Rect(x, y, w, h)
            self.rooms.append(room)
            return room

    def _create_corridor(self, room1, room2):
        """Создает Г-образные коридоры, соединяющие центры двух комнат."""
        x1, y1 = room1.center
        x2, y2 = room2.center
        corridor_width = 30 # Ширина коридора (можно настроить в зависимости от размера спрайта игрока)

        if random.choice([True, False]):
            self.corridors.append(pygame.Rect(min(x1, x2), y1, abs(x1 - x2) + corridor_width, corridor_width))
            self.corridors.append(pygame.Rect(x2, min(y1, y2), corridor_width, abs(y1 - y2) + corridor_width))
        else:
            self.corridors.append(pygame.Rect(x1, min(y1, y2), corridor_width, abs(y1 - y2) + corridor_width))
            self.corridors.append(pygame.Rect(min(x1, x2), y2, abs(x1 - x2) + corridor_width, corridor_width))