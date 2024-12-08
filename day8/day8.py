"""Day 8: Resonant Collinearity"""

from collections import defaultdict
from itertools import combinations
from typing import Iterable, List, Tuple, Set

CoordXY = Tuple[int, int]


def get_frequencies(map: List[str]) -> Iterable[str]:
    """
    Returns an iterable over the set of all distinct frequencies in the map.
    """
    frequencies = defaultdict(list)
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell != '.':
                frequencies[cell].append((i, j))
    return frequencies.values()

def get_antinodes(l1: CoordXY, l2: CoordXY, n: int, m: int, resonance: bool = False) -> Set[CoordXY]:
    """
    Returns the positions of all antinodes within bounds of the map that are
    formed by the given pair of antennas, with or without considering resonance.
    """
    delta_i = l1[0] - l2[0]
    delta_j = l1[1] - l2[1]

    antinodes = {l1, l2} if resonance else set()

    i, j = l1
    while True:
        i += delta_i
        j += delta_j
        if not (0 <= i < n and 0 <= j < m):
            break
        antinodes.add((i, j))
        if not resonance:
            break

    i, j = l2
    while True:
        i -= delta_i
        j -= delta_j
        if not (0 <= i < n and 0 <= j < m):
            break
        antinodes.add((i, j))
        if not resonance:
            break

    return antinodes


def part1(map: List[str]) -> int:
    """
    Returns the number of antinodes in the given map, where an antinode is
    defined as a point twice in line with two antennas of the same frequency,
    twice as far from one as from the other (two per combination of antennas).
    """
    n, m = len(map), len(map[0])
    antinodes = set()
    for antennas in get_frequencies(map):
        for l1, l2 in combinations(antennas, r=2):
            for i, j in get_antinodes(l1, l2, n, m):
                if 0 <= i < n and 0 <= j < m:
                    antinodes.add((i, j))
    return len(antinodes)


def part2(map: List[str]) -> int:
    """
    Returns the number of antinodes in the given map, where an antinode is
    defined as a point in line with at least two antennas of the same frequency.
    Unlike in Part 1, a pair of antennas may have more than two antinodes.
    """
    n, m = len(map), len(map[0])
    antinodes = set()
    for antennas in get_frequencies(map):
        for l1, l2 in combinations(antennas, r=2):
            for i, j in get_antinodes(l1, l2, n, m, resonance=True):
                if 0 <= i < n and 0 <= j < m:
                    antinodes.add((i, j))
    return len(antinodes)


if __name__ == '__main__':
    with open('example.txt') as f:
        map = [line.strip() for line in f.readlines()]
    assert (ans := part1(map)) == 14, ans
    assert (ans := part2(map)) == 34, ans

    with open('input.txt') as f:
        map = [line.strip() for line in f.readlines()]
    print('Part 1:', part1(map))
    print('Part 2:', part2(map))
