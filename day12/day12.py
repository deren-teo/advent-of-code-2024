"""Day 12: Garden Groups"""

from collections import defaultdict
from typing import List, Set, Tuple


CoordType = Tuple[int, int]

def pad(garden: List[str], c: str = '#') -> List[str]:
    """
    Pads the outside of the garden map with the given character.
    """
    m = len(garden[0])
    return [c * (m + 2)] + [c + row + c for row in garden] + [c * (m + 2)]

def get_region(garden: List[str], start: CoordType) -> Set[CoordType]:
    """
    Performs a BFS on the garden map from the starting position and returns
    a set of all 4-connected coordinates with the same symbol as the start.
    """
    n, m = len(garden), len(garden[0])
    i, j = start

    region_symbol = garden[i][j]
    region = {(i, j)}
    queue = [(i, j)]

    while len(queue) > 0:
        _i, _j = queue.pop(0)

        if _i > 0 and (garden[_i - 1][_j] == region_symbol) and ((_i - 1, _j) not in region):
            queue.append((_i - 1, _j))
            region.add((_i - 1, _j))
        if _i < n - 1 and (garden[_i + 1][_j] == region_symbol) and ((_i + 1, _j) not in region):
            queue.append((_i + 1, _j))
            region.add((_i + 1, _j))
        if _j > 0 and (garden[_i][_j - 1] == region_symbol) and ((_i, _j - 1) not in region):
            queue.append((_i, _j - 1))
            region.add((_i, _j - 1))
        if _j < m - 1 and (garden[_i][_j + 1] == region_symbol) and ((_i, _j + 1) not in region):
            queue.append((_i, _j + 1))
            region.add((_i, _j + 1))

    return region

def get_perimeter(region: Set[CoordType]) -> List[Tuple[CoordType, CoordType]]:
    """
    Returns the perimeter of the given region.
    """
    perimeter = []
    for i, j in region:
        if (_ij := (i - 1, j)) not in region:
            perimeter.append((_ij, (i, j)))
        if (_ij := (i + 1, j)) not in region:
            perimeter.append((_ij, (i, j)))
        if (_ij := (i, j - 1)) not in region:
            perimeter.append((_ij, (i, j)))
        if (_ij := (i, j + 1)) not in region:
            perimeter.append((_ij, (i, j)))
    return perimeter

def get_sides(region: Set[CoordType]) -> List[Set[CoordType]]:
    """
    Combines colinear perimeter segments into "sides", and returns the number of
    sides of the given region.
    """
    sides = defaultdict(set)
    s_counter = 0

    for (ext_i, ext_j), (int_i, int_j) in get_perimeter(region):
        s1_idx = None; s2_idx = None

        if ext_i == int_i: # i.e. vertical side
            p1 = (ext_i - 1, ext_j), (int_i - 1, int_j)
            p2 = (ext_i + 1, ext_j), (int_i + 1, int_j)
        else: # i.e. horizontal side
            p1 = (ext_i, ext_j - 1), (int_i, int_j - 1)
            p2 = (ext_i, ext_j + 1), (int_i, int_j + 1)

        for s_idx, s in sides.items():
            if s1_idx is None and p1 in s:
                s1_idx = s_idx
            if s2_idx is None and p2 in s:
                s2_idx = s_idx
            if s1_idx is not None and s2_idx is not None:
                break

        if s1_idx is None and s2_idx is None:
            sides[s_counter].add(((ext_i, ext_j), (int_i, int_j)))
            s_counter += 1
        elif s1_idx is None:
            sides[s2_idx].add(((ext_i, ext_j), (int_i, int_j)))
        elif s2_idx is None or s1_idx == s2_idx:
            sides[s1_idx].add(((ext_i, ext_j), (int_i, int_j)))
        else: # s1_idx != s2_idx (and neither is None)
            sides[s_counter] = sides[s1_idx] | sides[s2_idx] | {((ext_i, ext_j), (int_i, int_j))}
            del sides[s1_idx]
            del sides[s2_idx]
            s_counter += 1

    return list(sides.values())


def part1(garden: List[str]) -> int:
    """
    Returns the sum of the cost of each distinct region in the given garden map,
    where the cost of a region is the product of its area and perimeter.
    """
    visited = set()
    total_cost = 0

    for i, row in enumerate(garden):
        for j in range(len(row)):
            if (i, j) not in visited:
                region = get_region(garden, (i, j))
                total_cost += len(region) * len(get_perimeter(region))
                visited |= region

    return total_cost


def part2(garden: List[str]) -> int:
    """
    Returns the sum of the cost of each distinct region in the given garden map,
    where the cost of the region is the product of its area and number of sides.
    """
    padded = pad(garden)
    visited = set()
    total_cost = 0

    for i in range(1, len(padded) - 1):
        for j in range(1, len(padded[0]) - 1):
            if (i, j) not in visited:
                region = get_region(padded, (i, j))
                total_cost += len(region) * len(get_sides(region))
                visited |= region

    return total_cost


if __name__ == '__main__':
    with open('example.txt') as f:
        map = [row.strip() for row in f.readlines()]
    assert (ans := part1(map)) == 1930, ans
    assert (ans := part2(map)) == 1206, ans

    with open('input.txt') as f:
        map = [row.strip() for row in f.readlines()]
    print('Part 1:', part1(map))
    print('Part 2:', part2(map))
