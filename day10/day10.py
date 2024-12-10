"""Day 10: Hoof It"""

from typing import List, Tuple


def find_trailheads(topographic_map: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Returns a list of cells (row, column) with an value (altitude) of zero.
    """
    trailheads = []
    for i, row in enumerate(topographic_map):
        for j, cell in enumerate(row):
            if cell == 0:
                trailheads.append((i, j))
    return trailheads

def accessible_nodes(topographic_map: List[List[int]], i: int, j: int) -> List[Tuple[int, int]]:
    """
    Returns a list of cells accessible from the given (i, j) position, where an
    accessible cell is one within the map and has a value (altitude) of the
    current value + 1.
    """
    n, m = len(topographic_map), len(topographic_map[0])
    current_elevation = topographic_map[i][j]
    accessible = []

    if i > 0 and topographic_map[i - 1][j] == current_elevation + 1:
        accessible.append((i - 1, j))
    if i < n - 1 and topographic_map[i + 1][j] == current_elevation + 1:
        accessible.append((i + 1, j))
    if j > 0 and topographic_map[i][j - 1] == current_elevation + 1:
        accessible.append((i, j - 1))
    if j < m - 1 and topographic_map[i][j + 1] == current_elevation + 1:
        accessible.append((i, j + 1))

    return accessible


def part1(topographic_map: List[List[int]]) -> int:
    """
    Returns the total score of all trailheads, where the score of a trailhead
    is the number of distinct summits reachable from the trailhead.
    """
    total_score = 0
    trailhead_score = 0

    queue = find_trailheads(topographic_map)
    visited = set()

    while len(queue) > 0:
        i, j = queue.pop(0)
        visited.add((i, j))

        if topographic_map[i][j] == 0:
            total_score += trailhead_score
            trailhead_score = 0
            visited.clear()

        if topographic_map[i][j] == 9:
            trailhead_score += 1
            continue

        accessible = accessible_nodes(topographic_map, i, j)
        queue = [n for n in accessible if n not in visited] + queue

    total_score += trailhead_score

    return total_score


def part2(topographic_map: List[List[int]]) -> int:
    """
    Returns the total rating of all trailheads, where the rating of a trailhead
    is the number of distinct paths to all summits reachable from the trailhead.
    """
    total_rating = 0
    trailhead_rating = 0

    queue = [(node, None) for node in find_trailheads(topographic_map)]
    visited = set() # (node, parent)

    while len(queue) > 0:
        (i, j), parent = queue.pop(0)
        visited.add(((i, j), parent))

        if topographic_map[i][j] == 0:
            total_rating += trailhead_rating
            trailhead_rating = 0
            visited.clear()

        if topographic_map[i][j] == 9:
            trailhead_rating += 1
            continue

        accessible = accessible_nodes(topographic_map, i, j)
        queue = [(n, (i, j)) for n in accessible if n not in visited] + queue

    total_rating += trailhead_rating

    return total_rating


if __name__ == '__main__':
    with open('example.txt') as f:
        topographic_map = [list(map(int, row.strip())) for row in f.readlines()]
    assert (ans := part1(topographic_map)) == 36, ans
    assert (ans := part2(topographic_map)) == 81, ans

    with open('input.txt') as f:
        topographic_map = [list(map(int, row.strip())) for row in f.readlines()]
    print('Part 1:', part1(topographic_map))
    print('Part 2:', part2(topographic_map))
