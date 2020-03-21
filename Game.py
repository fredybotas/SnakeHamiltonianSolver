import pygame as pg
import random

from Snake import Snake, Direction, Node, NodeType
from HamiltonianSolver import expand_graph, big_picture_graph
from HamiltonianDriver import HamiltonianDriver
from Constants import *


class Game:
    food = None
    snake = None
    driver = None

    def __init__(self, driver=None):
        self.driver = driver(self)
        self.restart()

    def restart(self):
        self.snake = Snake(2, 2, Direction.RIGHT)
        self.generate_food()

    def move(self):
        if self.food is not None and self.food.x == self.snake.get_head().x % HEIGHT and self.food.y == self.snake.get_head().y % WIDTH:
            self.snake.enlarge_in_next_move()
            # must be in this order
            self.snake.move()
            self.generate_food()
        else:
            self.snake.move()

        if self.driver is not None:
            self.snake.set_direction(self.driver.on_move())

        if self.check_collision():
            self.restart()

    def get_free_tiles(self):
        result = []
        for x in range(HEIGHT):
            for y in range(WIDTH):
                result.append((x, y))
        if self.snake is not None:
            snake_tiles = [(tile.x, tile.y) for tile in self.snake.tiles]
        else:
            snake_tiles = []
        return list(filter(lambda x: x not in snake_tiles, result))

    def generate_food(self):
        snake_tiles = [(node.x % HEIGHT, node.y % WIDTH) for node in
                       self.snake.tiles]

        if len(snake_tiles) == HEIGHT * WIDTH:
            self.food = None
            return

        if self.driver is not None:
            self.food = self.driver.generate_food()
        else:
            free_tiles = self.get_free_tiles()
            x, y = random.choice(free_tiles[:len(free_tiles) // 2 + 1])
            self.food = Node(x, y, NodeType.FOOD)

    def check_collision(self):
        return (self.snake.get_head().x % HEIGHT,
                self.snake.get_head().y % WIDTH) in [
                   (node.x % HEIGHT, node.y % WIDTH) for node in
                   self.snake.tiles[:-1]]


def main():
    pg.init()

    game = Game(HamiltonianDriver)
    screen = pg.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE))
    snake_surface = pg.Surface((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE),
                               pg.SRCALPHA, 32)

    while True:
        screen.fill(GRASS_COLOR)
        snake_surface.fill((0, 0, 0, 0))

        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.KEYDOWN):
                if event.key == pg.K_UP:
                    game.snake.set_direction(Direction.UP)
                if event.key == pg.K_DOWN:
                    game.snake.set_direction(Direction.DOWN)
                if event.key == pg.K_LEFT:
                    game.snake.set_direction(Direction.LEFT)
                if event.key == pg.K_RIGHT:
                    game.snake.set_direction(Direction.RIGHT)

        game.move()

        food = game.food
        if food is not None:
            rect = pg.Rect((food.y % WIDTH) * BLOCK_SIZE + 1,
                           (food.x % HEIGHT) * BLOCK_SIZE + 1, BLOCK_SIZE - 2,
                           BLOCK_SIZE - 2)
            pg.draw.rect(screen, FOOD_COLOR, rect)

        prev_tile = None
        for index, tile in enumerate(game.snake.tiles):
            if prev_tile is not None:
                rect = pg.Rect(
                    ((((prev_tile.y + tile.y) / 2) % WIDTH) * BLOCK_SIZE) + 1,
                    ((((prev_tile.x + tile.x) / 2) % HEIGHT) * BLOCK_SIZE) + 1,
                    BLOCK_SIZE - 2,
                    BLOCK_SIZE - 2)
                pg.draw.rect(screen, SNAKE_INSIDE_COLOR, rect)

            rect = pg.Rect(((tile.y % WIDTH) * BLOCK_SIZE) + 1,
                           ((tile.x % HEIGHT) * BLOCK_SIZE) + 1,
                           BLOCK_SIZE - 2,
                           BLOCK_SIZE - 2)
            pg.draw.rect(snake_surface, SNAKE_INSIDE_COLOR, rect)
            prev_tile = tile

        screen.blit(snake_surface, (0, 0))

        pg.display.update()
        pg.time.delay(20)


if __name__ == '__main__':
    main()
