"""Day 18: RAM Run"""

from typing import List, Set, Tuple


def parse_input(lines: List[str]) -> List[Tuple[int, int]]:
    """
    Parses a list of coordinates in string representation into integer tuples.
    """
    return [tuple(map(int, line.strip().split(','))) for line in lines]

def get_successors(map_size: Tuple[int, int], corrupted: Set[Tuple[int, int]],
               node: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Returns the cells which can be reached from the given node. "Corrupted"
    cells cannot be traversed and are not included.
    """
    successors = []

    if node[0] > 0 and (s := (node[0] - 1, node[1])) not in corrupted:
        successors.append(s)
    if node[1] > 0 and (s := (node[0], node[1] - 1)) not in corrupted:
        successors.append(s)
    if node[0] < map_size[0] - 1 and (s := (node[0] + 1, node[1])) not in corrupted:
        successors.append(s)
    if node[1] < map_size[1] - 1 and (s := (node[0], node[1] + 1)) not in corrupted:
        successors.append(s)

    return successors


def part1(map_size: Tuple[int, int], corrupted: Set[Tuple[int, int]]) -> int:
    """
    Returns the shortest distance from the top left to the bottom right of a map
    of the given size, where the "corrupted" cells cannot be traversed.
    """
    end = (map_size[0] - 1, map_size[1] - 1)
    queue = [((0, 0), 0)]; visited = {(0, 0)}

    while len(queue) > 0:
        node, distance = queue.pop(0)
        for s in get_successors(map_size, corrupted, node):
            if s == end:
                return distance + 1
            if s not in visited:
                queue.append((s, distance + 1))
                visited.add(s)

    return None


def part2(map_size: Tuple[int, int], corrupted: Set[Tuple[int, int]],
          incoming: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Returns the first incoming "corrupted" byte which blocks off the bottom
    right corner of the map from the top left corner.
    """
    for node in incoming:
        corrupted.add(node)
        if part1(map_size, corrupted) is None:
            return node

    raise RuntimeError('failed to converge')


if __name__ == '__main__':
    with open('example.txt') as f:
        corrupted = parse_input(f.readlines())
    assert (ans := part1((7, 7), set(corrupted[:12]))) == 22, ans
    assert (ans := part2((7, 7), set(corrupted[:12]), corrupted[12:])) == (6, 1), ans

    with open('input.txt') as f:
        corrupted = parse_input(f.readlines())
    print('Part 1:', part1((71, 71), set(corrupted[:1024])))
    print('Part 2:', part2((71, 71), set(corrupted[:1024]), corrupted[1024:]))
