import random
from enum import Enum, auto


class NeighborPosition(Enum):
    LEFT = auto(),
    RIGHT = auto(),
    UP = auto(),
    DOWN = auto()


big_picture_graph = [
    [0, 1, 6, 7, 8],
    [19, 2, 5, 10, 9],
    [18, 3, 4, 11, 12],
    [17, 16, 15, 14, 13],
]


def get_graph_size():
    return len(big_picture_graph), len(big_picture_graph[0])


def get_starting_coords():
    height, width = get_graph_size()
    minimum = 1000000
    result = None
    for x in range(height):
        for y in range(width):
            if big_picture_graph[x][y] < minimum:
                result = (x, y)
                minimum = big_picture_graph[x][y]
    return result


def get_num(coords):
    x, y = coords
    return big_picture_graph[x][y]


def get_coords(num):
    height, width = get_graph_size()
    result = None
    for x in range(height):
        for y in range(width):
            if big_picture_graph[x][y] == num:
                result = (x, y)
    return result


def get_position(num, num_n):
    x, y = get_coords(num)
    n_x, n_y = get_coords(num_n)
    if n_x > x:
        return NeighborPosition.DOWN
    if n_x < x:
        return NeighborPosition.UP
    if n_y > y:
        return NeighborPosition.RIGHT
    if n_y < y:
        return NeighborPosition.LEFT


def get_valid_neighbors(coords):
    x, y = coords
    num = big_picture_graph[x][y]
    a, b = get_graph_size()
    size = a * b
    lower_neighbor = (num - 1) % size
    upper_neighbor = (num + 1) % size
    result = list()
    result.append(
        [get_coords(lower_neighbor), get_position(num, lower_neighbor)])
    result.append(
        [get_coords(upper_neighbor), get_position(num, upper_neighbor)])
    return result


def get_margin_points(dim_x, dim_y, side: NeighborPosition):
    x, y = None, None
    n_x, n_y = None, None
    if side == NeighborPosition.LEFT:
        x = random.randrange(dim_x)
        n_x = x
        y = 0
        n_y = dim_y - 1
    elif side == NeighborPosition.RIGHT:
        x = random.randrange(dim_x)
        n_x = x
        y = dim_y - 1
        n_y = 0
    elif side == NeighborPosition.UP:
        x = 0
        n_x = dim_x - 1
        y = random.randrange(dim_y)
        n_y = y
    elif side == NeighborPosition.DOWN:
        x = dim_x - 1
        n_x = 0
        y = random.randrange(dim_y)
        n_y = y
    return x, y, n_x, n_y


def create_result_graph(dim_x, dim_y, result):
    result_graph = [[0 for _ in range(dim_y * len(big_picture_graph[0]))] for _
                    in range(dim_x * len(big_picture_graph))]
    for index, sub_graph in enumerate(result):
        for x in range(dim_x):
            for y in range(dim_y):
                graph_x, graph_y = get_coords(index)
                result_graph[(graph_x * dim_y) + x][(graph_y * dim_x) + y] = \
                    sub_graph[x][y] + (index * dim_x * dim_y)
    return result_graph


def expand_graph(dim_x, dim_y):
    dim_x = dim_x // len(big_picture_graph)
    dim_y = dim_y // len(big_picture_graph[0])

    result = []
    start_x, start_y = get_starting_coords()

    start_neighbors = get_valid_neighbors((start_x, start_y))
    start_upper_neighbor = start_neighbors[1]
    start_lower_neighbor = start_neighbors[0]

    cycle = None
    while cycle is None:
        first_end_x, first_end_y, curr_start_x, curr_start_y = get_margin_points(
            dim_x, dim_y, start_upper_neighbor[1])
        first_start_x, first_start_y, last_end_x, last_end_y = get_margin_points(
            dim_x, dim_y, start_lower_neighbor[1])
        cycle = get_hamiltonian_cycle((first_start_x, first_start_y),
                                      (first_end_x, first_end_y), dim_y, dim_x)

    result.append(cycle)
    curr_x, curr_y = start_upper_neighbor[0]

    while True:
        curr_neighbors = get_valid_neighbors((curr_x, curr_y))
        upper_neighbor = curr_neighbors[1]

        curr_end_x, curr_end_y, next_start_x, next_start_y = get_margin_points(
            dim_x, dim_y, upper_neighbor[1])
        if upper_neighbor[0] == (start_x, start_y):
            cycle = get_hamiltonian_cycle((curr_start_x, curr_start_y),
                                          (last_end_x, last_end_y), dim_y,
                                          dim_x)
        else:
            cycle = get_hamiltonian_cycle((curr_start_x, curr_start_y),
                                          (curr_end_x, curr_end_y), dim_y,
                                          dim_x)

        if cycle is None:
            continue

        result.append(cycle)

        curr_start_x, curr_start_y = next_start_x, next_start_y
        curr_x, curr_y = upper_neighbor[0]
        if curr_x == start_x and curr_y == start_y:
            break

    return create_result_graph(dim_x, dim_y, result)


def generate_neighbors(x, y, width, height):
    result = []
    if x - 1 >= 0:
        result.append((x - 1, y))
    if x + 1 < height:
        result.append((x + 1, y))
    if y - 1 >= 0:
        result.append((x, y - 1))
    if y + 1 < width:
        result.append((x, y + 1))
    random.shuffle(result)
    return result


def get_hamiltonian_cycle(start, end, width, height):
    print('Getting hamiltonian with: {}, {}'.format(start, end))
    start_x, start_y = start
    end_x, end_y = end
    _board = [[0 for _ in range(width)] for _ in range(height)]
    _board[start_x][start_y] = 1
    stack = [(_board, 1, start_x, start_y)]
    result = None
    visited = set()

    while len(stack) > 0:
        board, num, x, y = stack[-1]
        stack = stack[:-1]

        if num == (width * height) and board[end_x][end_y] == num:
            result = board
            break

        visited.add(str(board))
        if board[end_x][end_y] != 0:
            continue

        neighbors = generate_neighbors(x, y, width, height)

        for n_x, n_y in neighbors:
            new_state = [x[:] for x in board]
            if new_state[n_x][n_y] != 0:
                continue
            new_state[n_x][n_y] = num + 1
            if str(new_state) in visited:
                continue

            stack.append((new_state, num + 1, n_x, n_y))

    return result
