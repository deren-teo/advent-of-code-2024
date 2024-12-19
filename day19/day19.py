"""Day 19: Linen Layout"""

from typing import Dict, List, Set, Tuple


def parse_input(input_str: str) -> Tuple[List[str], List[str]]:
    """
    Parses a contiguous input into a list of towels and a list of patterns.
    """
    towels, patterns = input_str.split('\n\n')
    return towels.split(', '), patterns.split('\n')

def recursive_search(substrings: List[str], target: str, impossible: Set[str]) -> bool:
    """
    Recursively attempts to match a substring to the start of the target string.
    Returns True if one or more substrings can be combined (with replacement)
    to produce the target; otherwise, False.
    """
    if target in substrings:
        return True

    for s in substrings:
        if target.startswith(s) and target[len(s):] not in impossible and \
                recursive_search(substrings, target[len(s):], impossible):
            return True

    impossible.add(target)
    return False

def counting_search(substrings: List[str], target: str, cache: Dict[str, int]) -> int:
    """
    Recursively attempts to match a substring to the start of the target string.
    Returns the number of substring combinations (with replacement) which can
    produce the target.
    """
    options = 0

    for s in substrings:
        if s == target:
            options += 1
            continue
        if target.startswith(s):
            if (new_target := target[len(s):]) not in cache:
                counting_search(substrings, new_target, cache)
            options += cache[new_target]

    cache[target] = options
    return options


def part1(towels: List[str], patterns: List[str]) -> int:
    """
    Returns the number of patterns which are possible to produce as combinations
    (with replacement) of the given towels.
    """
    possible = 0
    for pattern in patterns:
        relevant_towels = {t for t in towels if t in pattern}
        if len(relevant_towels) == 0:
            continue
        possible += recursive_search(relevant_towels, pattern, set())
    return possible


def part2(towels: List[str], patterns: List[str]) -> int:
    """
    Returns the sum of the number of ways each pattern can be produced as a
    combination (with replacement) of the given towels.
    """
    options = 0
    for pattern in patterns:
        relevant_towels = {t for t in towels if t in pattern}
        if len(relevant_towels) == 0:
            continue
        options += counting_search(relevant_towels, pattern, dict())
    return options


if __name__ == '__main__':
    with open('example.txt') as f:
        towels, patterns = parse_input(f.read())
    assert (ans := part1(towels, patterns)) == 6, ans
    assert (ans := part2(towels, patterns)) == 16, ans

    with open('input.txt') as f:
        towels, patterns = parse_input(f.read())
    print('Part 1:', part1(towels, patterns))
    print('Part 2:', part2(towels, patterns))
