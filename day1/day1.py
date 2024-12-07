"""Day 1: Historian Hysteria"""

from collections import Counter
from typing import Iterable


def part1(l1: Iterable[int], l2: Iterable[int]) -> int:
    """
    Returns the sum of the pairwise difference between the elements of l1 and l2
    after sorting both lists.
    """
    return sum(abs(n1 - n2) for n1, n2 in zip(sorted(l1), sorted(l2)))


def part2(l1: Iterable[int], l2: Iterable[int]) -> int:
    """
    Returns the sum of the product of each number in l1 and the number of times
    that number appears in l2.
    """
    counter = Counter(l2)
    return sum(n * counter[n] for n in l1)


if __name__ == '__main__':
    with open('example.txt') as f:
        l1, l2 = list(zip(*[map(int, l.split()) for l in f.readlines()]))
    assert (ans := part1(l1, l2)) == 11, ans
    assert (ans := part2(l1, l2)) == 31, ans

    with open('input.txt') as f:
        l1, l2 = list(zip(*[map(int, l.split()) for l in f.readlines()]))
    print('Part 1:', part1(l1, l2))
    print('Part 2:', part2(l1, l2))
