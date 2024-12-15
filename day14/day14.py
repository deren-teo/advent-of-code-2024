"""Day 14: Restroom Redoubt"""

from collections import defaultdict
from copy import deepcopy
from typing import List, Tuple


Robot = Tuple[Tuple[int, int], Tuple[int, int]]

def parse_robot(robot_str: str) -> Robot:
    """
    Parses a string representation of the position and velocity of a robot and
    returns integer values in nested tuples.
    """
    pos_str, vel_str = robot_str.split()
    x, y = pos_str[2:].split(',')
    v_x, v_y = vel_str[2:].split(',')
    return (int(x), int(y)), (int(v_x), int(v_y))

def evolve_map(robots: List[Robot], mapsize: Tuple[int, int], iters: int) -> List[Robot]:
    """
    Returns the positions of each robot in the map of given size after the
    specified number of iterations.
    """
    evolved = []

    for (x, y), (v_x, v_y) in robots:
        _x = (x + v_x * iters) % mapsize[0]
        _y = (y + v_y * iters) % mapsize[1]
        evolved.append(((_x, _y), (v_x, v_y)))

    return evolved

def coverage_ratio(robots: List[Robot], mapsize: Tuple[int, int]) -> float:
    """
    Returns the ratio of filled to unfilled positions in the map of given size.
    """
    return len(set(p for p, _ in robots)) / (mapsize[0] * mapsize[1])


def draw_map(robots: List[Robot], mapsize: Tuple[int, int]) -> None:
    """
    Prints a visual representation of the robots in a map of the given size.
    """
    positions = defaultdict(int)
    for p, _ in robots:
        positions[p] += 1

    for y in range(mapsize[1]):
        for x in range(mapsize[0]):
            print(positions.get((x, y), '.'), end=' ')
        print()


def part1(robots: List[Robot], mapsize: Tuple[int, int]) -> int:
    """
    Returns the safety factor of the map, defined as the product of the number
    of robots in each of the 4 map quadrants, after 100 iterations.
    """
    robots = evolve_map(robots, mapsize, iters=100)

    # Count the number of robots in each quadrant
    quadrant = {'UL': 0, 'UR': 0, 'BL': 0, 'BR': 0}

    for (x, y), _ in robots:
        if x < mapsize[0] // 2:
            if y < mapsize[1] // 2:
                quadrant['UL'] += 1
            elif y > mapsize[1] // 2:
                quadrant['BL'] += 1
        elif x > mapsize[0] // 2:
            if y < mapsize[1] // 2:
                quadrant['UR'] += 1
            elif y > mapsize[1] // 2:
                quadrant['BR'] += 1

    return quadrant['UL'] * quadrant['UR'] * quadrant['BL'] * quadrant['BR']


def part2(robots: List[Robot], mapsize: Tuple[int, int]) -> int:
    """
    Returns the map iteration (up to a maximum value of 10000) with the maximum
    coverage ratio, defined as the ratio of filled to total map positions.
    """
    _robots = deepcopy(robots)
    coverage_ratios = []
    for _ in range(10000):
        _robots = evolve_map(_robots, mapsize, iters=1)
        coverage_ratios.append(coverage_ratio(_robots, mapsize))

    i = 0
    while coverage_ratio(robots, mapsize) < round(max(coverage_ratios), 3):
        robots = evolve_map(robots, mapsize, iters=1)
        i += 1

    draw_map(robots, mapsize)
    return i


if __name__ == '__main__':
    with open('example.txt') as f:
        robots = [parse_robot(r) for r in f.readlines()]
    assert (ans := part1(robots, (11, 7))) == 12, ans

    with open('input.txt') as f:
        robots = [parse_robot(r) for r in f.readlines()]
    print('Part 1:', part1(robots, (101, 103)))
    print('Part 2:', part2(robots, (101, 103)))
