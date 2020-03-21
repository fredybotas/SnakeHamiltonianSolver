from enum import Enum, auto

MOVEMENT_DELTA = 1


class Direction(Enum):
    LEFT = (0, -MOVEMENT_DELTA)
    RIGHT = (0, MOVEMENT_DELTA)
    UP = (-MOVEMENT_DELTA, 0)
    DOWN = (MOVEMENT_DELTA, 0)


class NodeType(Enum):
    SNAKE = auto()
    GRASS = auto()
    FOOD = auto()


class Node:
    def __init__(self, x, y, node_type: NodeType):
        self.x = x
        self.y = y
        self.node_type = node_type

    def move(self, direction: Direction):
        d_x, d_y = direction.value
        self.x += d_x
        self.y += d_y

    def copy(self):
        return Node(self.x, self.y, self.node_type)


class Snake:
    tiles = []
    direction: Direction
    changing_direction = False

    def __init__(self, x, y, direction: Direction):
        self.direction = direction
        self.tiles = [Node(x, y, NodeType.SNAKE)]
        self.should_enlarge = False
        self.changing_direction = False

    def set_direction(self, direction: Direction):
        print(direction)
        if self.changing_direction is True:
            return
        if self.direction == Direction.UP and direction == Direction.DOWN:
            return
        if self.direction == Direction.DOWN and direction == Direction.UP:
            return
        if self.direction == Direction.LEFT and direction == Direction.RIGHT:
            return
        if self.direction == Direction.RIGHT and direction == Direction.LEFT:
            return
        self.changing_direction = True
        self.direction = direction

    def enlarge_in_next_move(self):
        self.should_enlarge = True

    def move(self):
        new_node = self.tiles[-1].copy()
        new_node.move(self.direction)
        self.changing_direction = False
        self.tiles += [new_node]

        if self.should_enlarge is True:
            self.should_enlarge = False
        else:
            self.tiles = self.tiles[1:]

    def get_head(self):
        return self.tiles[-1]
