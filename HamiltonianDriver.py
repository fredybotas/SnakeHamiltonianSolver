from Constants import *
from Snake import Direction, Node, NodeType
from HamiltonianSolver import expand_graph

import random


class HamiltonianDriver:
    delta_movement = [
        (0, 1, Direction.RIGHT),
        (0, -1, Direction.LEFT),
        (1, 0, Direction.DOWN),
        (-1, 0, Direction.UP)
    ]

    def __init__(self, game):
        self.path = expand_graph(HEIGHT, WIDTH)
        for a in self.path:
            print(a)

        self.game = game

    def length_from_node(self, start, target):
        start_x, start_y = start
        target_x, target_y = target
        num_start = self.path[start_x][start_y]
        num_target = self.path[target_x][target_y]

        if num_start > num_target:
            return (WIDTH * HEIGHT) - num_start + num_target - 1
        elif num_start < num_target:
            return num_target - num_start - 1
        else:
            return 0

    def did_shortcut(self):
        tail_x, tail_y = self.game.snake.tiles[0].x, self.game.snake.tiles[0].y
        snake_x, snake_y = self.game.snake.get_head().x, self.game.snake.get_head().y

        tail_num = self.path[tail_x][tail_y]
        head_num = self.path[snake_x][snake_y]

        if tail_num > head_num:
            distance_between_head_tail = (tail_num - head_num - 1)
        else:
            distance_between_head_tail = (WIDTH * HEIGHT) - (
                        head_num - tail_num + 1)

        return not (distance_between_head_tail + len(
            self.game.snake.tiles) == WIDTH * HEIGHT)

    def is_in_shortcut(self, x, y):
        head_x, head_y = self.game.snake.get_head().x, self.game.snake.get_head().y
        tail_x, tail_y = self.game.snake.tiles[0].x, self.game.snake.tiles[0].y

        head_num = self.path[head_x][head_y]
        tail_num = self.path[tail_x][tail_y]
        check_num = self.path[x][y]

        if head_num >= tail_num:
            return check_num >= tail_num and check_num <= head_num
        else:
            return check_num <= head_num or check_num >= tail_num

    def is_food_in_between(self, start_x, start_y, end_x, end_y):
        num_start = self.path[start_x][start_y]
        num_end = self.path[end_x][end_y]
        if self.game.food is None:
            return True
        num_food = self.path[self.game.food.x][self.game.food.y]
        if num_end > num_start:
            return num_food < num_end and num_food > num_start
        else:
            return num_food > num_start or num_food < num_end

    @staticmethod
    def is_in_graph(x, y):
        return x >= 0 and x < HEIGHT and y >= 0 and y < WIDTH

    def is_in_snake(self, x, y):
        return (x, y) in [(tile.x, tile.y) for tile in self.game.snake.tiles]

    def is_next_tile_in_path(self, x, y, next_x, next_y):
        num = self.path[x][y]
        num_next = self.path[next_x][next_y]
        return num_next == ((num % (HEIGHT * WIDTH)) + 1)

    def generate_food(self):
        free_tiles = self.game.get_free_tiles()
        nums = [self.length_from_node(
            (self.game.snake.get_head().x, self.game.snake.get_head().y),
            (x, y)) for x, y in free_tiles]
        nums, free_tiles = zip(*sorted(zip(nums, free_tiles)))
        x, y = random.choice(free_tiles[:len(free_tiles) // 2 + 1])
        return Node(x, y, NodeType.FOOD)

    def check_movement(self, x, y, move_x, move_y):
        return self.is_in_graph(move_x, move_y) and self.is_next_tile_in_path(
            x, y, move_x, move_y)

    def check_movement_shortcut(self, x, y, move_x, move_y):
        return self.is_in_graph(move_x, move_y) and not self.is_in_snake(
            move_x, move_y) and not self.is_in_shortcut(move_x, move_y)

    def on_move(self):
        curr_x, curr_y = self.game.snake.get_head().x, self.game.snake.get_head().y
        curr_x %= HEIGHT
        curr_y %= WIDTH

        min_length = 1000000
        movement = None
        for d_x, d_y, direction in self.delta_movement:
            if self.game.food is None:
                if self.check_movement(curr_x, curr_y, curr_x + d_x,
                                       curr_y + d_y) is True:
                    movement = direction
                if self.check_movement_shortcut(curr_x, curr_y, curr_x + d_x,
                                                curr_y + d_y) is True:
                    movement = direction
                continue
            if self.check_movement_shortcut(curr_x, curr_y, curr_x + d_x,
                                            curr_y + d_y) is True:
                length = self.length_from_node((curr_x + d_x, curr_y + d_y), (
                self.game.food.x, self.game.food.y))
                if length < min_length:
                    min_length = length
                    movement = direction
            if self.check_movement(curr_x, curr_y, curr_x + d_x,
                                   curr_y + d_y) is True:
                length = self.length_from_node((curr_x + d_x, curr_y + d_y), (
                self.game.food.x, self.game.food.y))
                if length < min_length:
                    min_length = length
                    movement = direction
        return movement

        if self.check_movement_shortcut(curr_x, curr_y, curr_x + 1,
                                        curr_y) is True:
            return Direction.DOWN
        elif self.check_movement_shortcut(curr_x, curr_y, curr_x - 1,
                                          curr_y) is True:
            return Direction.UP
        elif self.check_movement_shortcut(curr_x, curr_y, curr_x,
                                          curr_y + 1) is True:
            return Direction.RIGHT
        elif self.check_movement_shortcut(curr_x, curr_y, curr_x,
                                          curr_y - 1) is True:
            return Direction.LEFT
        elif self.check_movement(curr_x, curr_y, curr_x + 1, curr_y) is True:
            return Direction.DOWN
        elif self.check_movement(curr_x, curr_y, curr_x - 1, curr_y) is True:
            return Direction.UP
        elif self.check_movement(curr_x, curr_y, curr_x, curr_y + 1) is True:
            return Direction.RIGHT
        elif self.check_movement(curr_x, curr_y, curr_x, curr_y - 1) is True:
            return Direction.LEFT
