"""Day 15: Warehouse Woes"""

from typing import Dict, List, Set, Tuple


CoordType = Tuple[int, int]

def parse_warehouse(warehouse_map: str, double_width: bool = False
        ) -> Tuple[Set[CoordType], Dict[int, List[CoordType]], CoordType]:
    """
    Parses a string representation of a warehouse map into a set of positions
    representing walls, boxes and the robot. Each box has a unique ID number.
    """
    walls = set()
    boxes = dict()
    robot = None, None
    box_id = 0

    for i, row in enumerate(warehouse_map.split('\n')):
        for j, cell in enumerate(row):
            if cell == '#':
                walls |= {(i, 2 * j), (i, 2 * j + 1)} if double_width else {(i, j)}
            elif cell == 'O':
                boxes[box_id] = [(i, 2 * j), (i, 2 * j + 1)] if double_width else [(i, j)]
                box_id += 1
            elif cell == '@':
                robot = (i, 2 * j) if double_width else (i, j)

    return walls, boxes, robot

def print_warehouse(walls: Set[CoordType], boxes: Dict[int, CoordType],
        robot: CoordType, warehouse_size: Tuple[int, int]) -> None:
    """
    Prints a string representation of the warehouse map, for debugging.
    """
    for i in range(warehouse_size[0]):
        for j in range(warehouse_size[1]):
            if (i, j) in walls:
                print('#', end='')
            elif (i, j) in {p for ps in boxes.values() for p in ps}:
                print('O', end='')
            elif (i, j) == robot:
                print('@', end='')
            else:
                print('.', end='')
        print()
    print()

def get_next_position(current_position: CoordType, direction: str) -> CoordType:
    """
    Returns the next position in the given direction from the current position.
    """
    i, j = current_position
    next_i = {'^': i - 1, 'v': i + 1}.get(direction, i)
    next_j = {'<': j - 1, '>': j + 1}.get(direction, j)
    return next_i, next_j

def move_robot(walls: Set[CoordType], boxes: Dict[int, List[CoordType]],
        box_lookup: Dict[CoordType, int], robot: CoordType, direction: str) -> None:
    """
    Updates the positions of the robot and boxes due to the given movement.
    """
    # Use a queue to keep track of boxes affected by the move
    check_queue = [get_next_position(robot, direction)]
    box_queue = []
    while len(check_queue) > 0:
        check_p = check_queue.pop(0)
        # If we run into a wall, the robot does not move
        if check_p in walls:
            return robot
        if check_p in box_lookup:
            if (box_id := box_lookup[check_p]) in box_queue:
                continue
            box_queue.append(box_id)
            for box_p in boxes[box_id][::-1]:
                check_queue.append(get_next_position(box_p, direction))

    # Update the position of all the boxes affected by the move
    for box_id in box_queue[::-1]:
        # NOTE: delete all existing positions before writing any, else a newly
        #  written position may be accidentally deleted
        for box_p in boxes[box_id]:
            del box_lookup[box_p]

        new_positions = []
        for box_p in boxes[box_id]:
            new_positions.append(new_p := get_next_position(box_p, direction))
            box_lookup[new_p] = box_id
        boxes[box_id] = new_positions

    return get_next_position(robot, direction)


def part1(walls: Set[CoordType], boxes: Dict[int, CoordType], robot: CoordType,
        moves: str) -> int:
    """
    Simulates the movements of the robot in a warehouse represented by the given
    walls and boxes. Returns a value representing the sum of the positions of
    the boxes after the robot has finished moving.
    """
    box_lookup = {v[0]: k for k, v in boxes.items()}
    for move in moves:
        robot = move_robot(walls, boxes, box_lookup, robot, move)
    return sum(100 * i + j for i, j in [p[0] for p in boxes.values()])


def part2(walls: Set[CoordType], boxes: Dict[int, CoordType], robot: CoordType,
        moves: str) -> int:
    """
    Simulates the movements of a robot in a warehouse represented by the given
    walls and boxes. Compared to Part 1, boxes can now be half-aligned with
    other boxes, allowing one box to push two side-by-side boxes.

    Returns a value representing the sum of the positions of the the boxes after
    the robot has finished moving.
    """
    box_lookup = dict()
    for box_id, (p1, p2) in boxes.items():
        box_lookup[p1] = box_id
        box_lookup[p2] = box_id

    for move in moves:
        robot = move_robot(walls, boxes, box_lookup, robot, move)

    return sum(100 * i + j for i, j in [p[0] for p in boxes.values()])


if __name__ == '__main__':
    with open('example-part1-only.txt') as f:
        warehouse_map, moves = f.read().split('\n\n')
        walls, boxes, robot = parse_warehouse(warehouse_map)
    assert (ans := part1(walls, boxes, robot, moves)) == 2028, ans

    with open('example-part2-only.txt') as f:
        warehouse_map, moves = f.read().split('\n\n')
        walls, boxes, robot = parse_warehouse(warehouse_map, double_width=True)
    assert (ans := part2(walls, boxes, robot, moves)) == 618, ans

    with open('example.txt') as f:
        warehouse_map, moves = f.read().split('\n\n')
        walls, boxes, robot = parse_warehouse(warehouse_map)
        assert (ans := part1(walls, boxes, robot, moves)) == 10092, ans
        walls, boxes, robot = parse_warehouse(warehouse_map, double_width=True)
        assert (ans := part2(walls, boxes, robot, moves)) == 9021, ans

    with open('input.txt') as f:
        warehouse_map, moves = f.read().split('\n\n')
        walls, boxes, robot = parse_warehouse(warehouse_map)
        print('Part 1:', part1(walls, boxes, robot, moves))
        walls, boxes, robot = parse_warehouse(warehouse_map, double_width=True)
        print('Part 2:', part2(walls, boxes, robot, moves))
