"""Day 11: Plutonian Pebbles"""

from collections import Counter, defaultdict
from typing import List, Tuple


def split(stone: str) -> Tuple[int, int]:
    """
    Splits a stone with a value of even length into two stones.
    E.g. 'abcxzy' -> [abc, xyz].
    """
    return (int(stone[:(len(stone) // 2)]), int(stone[(len(stone) // 2):]))

def evolve(stone: int) -> List[int]:
    """
    Evolves a stone according to the following rules (evaluated in order):
    1. If stone == 0, returns 1
    2. If stone has even length when converted to a string, splits the stone
    3. Otherwise, returns stone * 2024
    """
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        return split(str(stone))
    return [stone * 2024]

def evolve_and_count(stones: List[int], iterations: int) -> int:
    """
    Returns the final number of stones produced by evolving the given set for
    the given number of iterations.
    """
    counter = Counter(stones)

    for _ in range(iterations):
        new_counter = defaultdict(int)
        for stone, count in counter.items():
            for new_stone in evolve(stone):
                new_counter[new_stone] += count
        counter = new_counter

    return sum(count for count in counter.values())


if __name__ == '__main__':
    with open('example.txt') as f:
        stones = [int(n) for n in f.read().split(' ')]
    assert (ans := evolve_and_count(stones, 25)) == 55312, ans

    with open('input.txt') as f:
        stones = [int(n) for n in f.read().split(' ')]
    print('Part 1:', evolve_and_count(stones, 25))
    print('Part 2:', evolve_and_count(stones, 75))
