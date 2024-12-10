"""Day 9: Disk Fragmenter"""

from typing import List


def compactify(disk_map: List[int]) -> List[int]:
    """
    Returns a filesystem representation where, from the end of the disk map,
    files are fragmented and filled into the earliest available free space.
    """
    file_queue = [n for i, n in enumerate(disk_map) if i % 2 == 0]
    free_queue = [n for i, n in enumerate(disk_map) if i % 2 == 1]

    filesystem = []

    head_idx = 0
    tail_idx = len(file_queue) - 1
    while head_idx <= tail_idx:
        # Parse a file that's already in place
        filesystem += [head_idx] * file_queue[head_idx]
        head_idx += 1

        # Fill in any space after the file from the end of the queue
        if head_idx <= tail_idx:
            free_space = free_queue.pop(0)
            while free_space >= file_queue[tail_idx]:
                filesystem += [tail_idx] * file_queue[tail_idx]
                free_space -= file_queue[tail_idx]
                tail_idx -= 1

            filesystem += [tail_idx] * free_space
            file_queue[tail_idx] -= free_space

    return filesystem

def write_filesystem(filesystem: List[int], start: int, length: int, val: int) -> None:
    """
    Writes the given value into the file system over the range defined by the
    start index and length.
    """
    for i in range(start, start + length):
        filesystem[i] = val

def defragment(disk_map: List[int]) -> List[int]:
    """
    Returns a filesystem representation where, from the end of the disk map,
    files are moved as far forward as possible where there is enough space.
    """
    # Construct file and free-space queues
    file_queue = [] # (size, position)
    free_queue = [] # (size, position)
    i = 0
    position = 0
    while i < len(disk_map):
        file_queue.append([disk_map[i], position])
        position += disk_map[i]
        i += 1

        if i == len(disk_map):
            break

        free_queue.append([disk_map[i], position])
        position += disk_map[i]
        i += 1

    filesystem = [0] * sum(disk_map)

    for file_idx, (file_size, file_position) in list(enumerate(file_queue))[::-1]:
        for free_idx, (free_size, free_position) in enumerate(free_queue[:file_idx]):
            if free_size >= file_size:
                write_filesystem(filesystem, free_position, file_size, file_idx)
                free_queue[free_idx][0] -= file_size
                free_queue[free_idx][1] += file_size
                break
        else:
            write_filesystem(filesystem, file_position, file_size, file_idx)

    return filesystem

def calculate_checksum(filesystem: List[int]) -> int:
    """
    Returns the checksum of the given filesystem, which is the sum of the index
    of each slot in the filesystem multiplied by the file ID occupying the slot.
    """
    return sum(i * b for i, b in enumerate(filesystem))


def part1(disk_map: List[int]) -> int:
    """
    Returns the checksum of a filesystem constructed by compactifying the disk
    map as much as possible, including by fragmenting files.
    """
    return calculate_checksum(compactify(disk_map))


def part2(disk_map: List[int]) -> int:
    """
    Returns the checksum of a filesystem constructed by compactifying the disk
    map in terms of file blocks, without fragmenting the files.
    """
    return calculate_checksum(defragment(disk_map))


if __name__ == '__main__':
    with open('example.txt') as f:
        disk_map = [int(n) for n in f.read().strip()]
    assert (ans := part1(disk_map)) == 1928, ans
    assert (ans := part2(disk_map)) == 2858, ans

    with open('input.txt') as f:
        disk_map = [int(n) for n in f.read().strip()]
    print('Part 1:', part1(disk_map))
    print('Part 2:', part2(disk_map))
