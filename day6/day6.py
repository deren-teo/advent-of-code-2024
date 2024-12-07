"""Day 6: Guard Gallivant"""

from copy import deepcopy
from typing import List, Tuple

from tqdm import tqdm

CoordXY = Tuple[int, int]
Map = List[List[int]]

ROTATE = lambda dir: {'^': '>', '>': 'v', 'v': '<', '<': '^'}[dir]

NEXT_X = lambda x, dir: {'<': x - 1, '>': x + 1}.get(dir, x)
NEXT_Y = lambda y, dir: {'^': y - 1, 'v': y + 1}.get(dir, y)
NEXT_XY = lambda x, y, dir: (NEXT_X(x, dir), NEXT_Y(y, dir))

def locate_guard(map: Map) -> Tuple[CoordXY, str]:
    """
    Returns the (x, y) coordinate of the "^" symbol in the map.
    """
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == '^':
                return (j, i), cell
    raise ValueError('guard not found in map')

def move_guard(map: Map, x: int, y: int, direction: str) -> Tuple[CoordXY, str]:
    """
    Returns the next (x, y) coordinate and direction of the guard in the map.
    """
    n, m = len(map), len(map[0])
    _x, _y = NEXT_XY(x, y, direction)
    if not (-1 < _x < m and -1 < _y < n):
        return (_x, _y), direction
    if map[_y][_x] == '#':
        return (x, y), ROTATE(direction)
    else:
        return (_x, _y), direction

def trace_path(map: Map, x0: int, y0: int, init_dir: str) -> List[Tuple[CoordXY, str]]:
    """
    Returns the path through the map traversed by the guard from the given
    starting coordinate and direction.
    """
    n, m = len(map), len(map[0])
    path = [((x0, y0), init_dir)]
    x, y, direction = x0, y0, init_dir
    while True:
        (x, y), direction = move_guard(map, x, y, direction)
        if not (-1 < x < m and -1 < y < n):
            break
        path.append(((x, y), direction))
    return path

def has_loop(map: Map, x0: int, y0: int, init_dir: str) -> bool:
    """
    Returns True if the map has a loop from the given starting state.
    """
    n, m = len(map), len(map[0])
    path = {(x0, y0, init_dir)}
    x, y, direction = x0, y0, init_dir
    while True:
        (x, y), direction = move_guard(map, x, y, direction)
        if not (-1 < x < m and -1 < y < n):
            return False
        if (x, y, direction) in path:
            return True
        path.add((x, y, direction))


def part1(map: Map) -> int:
    """
    Returns the number of distinct coordinates traversed by the guard until
    exiting the map.
    """
    (x0, y0), init_dir = locate_guard(map)
    return len(set(t[0] for t in trace_path(map, x0, y0, init_dir)))


def part2(map: Map, show_progress: bool = False) -> int:
    """
    Returns the number of distinct coordinates where an obstacle could be
    placed to cause the guard to enter a looping path.
    """
    loop_wrapper = lambda z: tqdm(z) if show_progress else z

    (x0, y0), init_dir = locate_guard(map)
    path = trace_path(map, x0, y0, init_dir)

    obstacle_candidates = set()
    for (x, y), direction in loop_wrapper(path[:-1]):
        _x = NEXT_X(x, direction)
        _y = NEXT_Y(y, direction)
        if map[_y][_x] == '#':
            continue
        _map = deepcopy(map)
        _map[_y][_x] = '#'
        if has_loop(_map, x0, y0, init_dir):
            obstacle_candidates.add((_x, _y))

    return len(obstacle_candidates)


if __name__ == '__main__':
    with open('example.txt') as f:
        map = [[c for c in row.strip()] for row in f.readlines()]
    assert (ans := part1(map)) == 41, ans
    assert (ans := part2(map)) == 6, ans

    with open('input.txt') as f:
        map = [[c for c in row.strip()] for row in f.readlines()]
    print('Part 1:', part1(map))
    print('Part 2:', part2(map, show_progress=True))
