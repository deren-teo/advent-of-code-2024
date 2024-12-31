"""Day 16: Reindeer Maze"""

import heapq

from typing import List, Set, Tuple


NEXT_I = lambda i, direction: {'^': i - 1, 'v': i + 1}.get(direction, i)
NEXT_J = lambda j, direction: {'<': j - 1, '>': j + 1}.get(direction, j)
NEXT_P = lambda p, direction: (NEXT_I(p[0], direction), NEXT_J(p[1], direction))

CW  = lambda direction: {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]
CCW = lambda direction: {'^': '<', '<': 'v', 'v': '>', '>': '^'}[direction]

CoordType = Tuple[int, int]

def parse_input(lines: List[str]) -> Tuple[Set[CoordType], CoordType, CoordType]:
    """
    Parses a string representation of a maze into a set of walls, and start and
    end coordinates.
    """
    walls = set(); start = None; end = None

    for i, row in enumerate(lines):
        for j, cell in enumerate(row):
            if cell == '#':
                walls.add((i, j))
            elif cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)

    return walls, start, end

def get_successors(walls: Set[CoordType], score: int, node: Tuple[CoordType, str]
        ) -> Set[CoordType]:
    """
    Returns a set of all (coordinate, direction) pairs which can be reached from
    the current position and direction. Does not return any pure rotations which
    cannot be immediately succeeded by a forward movement.
    """
    position, direction = node
    successors = set()

    _i, _j  = NEXT_P(position, direction)
    if (_i, _j) not in walls:
        successors.add((score + 1, ((_i, _j), direction)))

    _i, _j = NEXT_P(position, CW(direction))
    if (_i, _j) not in walls:
        successors.add((score + 1000, (position, CW(direction))))

    _i, _j = NEXT_P(position, CCW(direction))
    if (_i, _j) not in walls:
        successors.add((score + 1000, (position, CCW(direction))))

    return successors


def part1(walls: Set[CoordType], start: CoordType, end: CoordType) -> int:
    """
    Performs a BFS on the maze from the starting position using a priority queue
    and returns the minimum cost required to reach the end position.
    """
    queue = [(0, (start, '>'))]; heapq.heapify(queue)
    visited = {(start, '>')}

    while len(queue) > 0:
        score, (position, direction) = heapq.heappop(queue)
        if position == end:
            break

        for score, node in get_successors(walls, score, (position, direction)):
            if node not in visited:
                heapq.heappush(queue, (score, node))
                visited.add(node)

    return score


def part2(walls: Set[CoordType], start: CoordType, end: CoordType) -> int:
    """
    Performs Dijkstra's algorithm from the starting position to find all lowest
    cost paths to the end position. Finds unique paths using a reverse search.

    Returns the number of cells which are part of at least one lowest cost path.
    """
    best_score = part1(walls, start, end)

    # Dijkstra's algorithm from start node, terminated early when costs exceed
    # the known minimum cost to the end position. Instead of storing a single
    # best parent, the algorithm is modified to store all equal best parents.
    queue = [(0, (start, '>'))]
    distances = {(start, '>'): (0, set())}

    while len(queue) > 0:
        score, (position, direction) = heapq.heappop(queue)
        if score > best_score:
            break

        for score, node in get_successors(walls, score, (position, direction)):
            if node not in distances or distances[node][0] > score:
                heapq.heappush(queue, (score, node))
                distances[node] = (score, {(position, direction)})

            elif distances[node][0] == score:
                heapq.heappush(queue, (score, node))
                distances[node][1].add((position, direction))

    # Reverse path search from end position to start, counting distinct cells
    rp_queue = [(end, direction) for direction in ('^', '>') if distances.get((end, direction), (0, None))[0] == best_score]
    visited = set(rp_queue)

    while len(rp_queue) > 0:
        node = rp_queue.pop(0)
        new_parents = [parent for parent in distances[node][1] if parent not in visited]
        rp_queue += new_parents
        visited |= set(new_parents)

    return len({position for position, _ in visited})


if __name__ == '__main__':
    with open('example-1.txt') as f:
        walls, start, end = parse_input(f.readlines())
    assert (ans := part1(walls, start, end)) == 7036, ans
    assert (ans := part2(walls, start, end)) == 45, ans

    with open('example-2.txt') as f:
        walls, start, end = parse_input(f.readlines())
    assert (ans := part1(walls, start, end)) == 11048, ans
    assert (ans := part2(walls, start, end)) == 64, ans

    with open('input.txt') as f:
        walls, start, end = parse_input(f.readlines())
    print('Part 1:', part1(walls, start, end))
    print('Part 2:', part2(walls, start, end))
