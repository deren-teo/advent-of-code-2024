"""Day 5: Print Queue"""

from collections import defaultdict
from typing import List


def list_idx(l: List, o: object) -> int:
    """
    Returns the index of the given object in the given list, or None if the
    object does not occur in the list.
    """
    for i, obj in enumerate(l):
        if obj == o: return i
    return None

def correctly_ordered(constraints: List[str], pages: List[int]) -> bool:
    """
    Returns True if the set of pages conforms to all given constraints.
    """
    for i in range(1, len(pages)):
        if f'{pages[i]}|{pages[i - 1]}' in constraints:
            return False
    return True

def relevant_constraints(constraints: List[str], pages: List[int]) -> List[str]:
    """
    Returns the subset of constraints for which both pages in the constraint
    occur within the given set of page numbers.
    """
    relevant = []
    for ordered_pair in constraints:
        a, b = map(int, ordered_pair.split('|'))
        if a in pages and b in pages:
            relevant.append(ordered_pair)
    return relevant


def part1(constraints: List[str], updates: List[int]) -> int:
    """
    Evaluates each set of updates against the given set of constraints and
    returns the sum of the middle page number of each correctly ordered set.
    """
    midpage_sum = 0
    for pages in updates:
        if correctly_ordered(constraints, pages):
            midpage_sum += pages[len(pages) // 2]
    return midpage_sum


def part2(constraints: List[str], updates: List[str]) -> int:
    """
    Solves the given constraint satisfaction problem for each set of updates,
    reordering misordered sets and returning the sum of the middle page number
    of each reordered set.
    """
    # Remove the update sets which are already correctly ordered -- irrelevant
    updates = [u for u in updates if not correctly_ordered(constraints, u)]

    midpage_sum = 0
    for pages in updates:
        csp = defaultdict(list)
        queue = relevant_constraints(constraints, pages)

        while len(queue) > 0:
            ordered_pair = queue.pop(0)
            a, b = map(int, ordered_pair.split('|'))
            idx_a = list_idx(pages, a)
            idx_b = list_idx(pages, b)

            if idx_a > idx_b:
                pages.insert(idx_b, pages.pop(idx_a))
                queue = csp[a] + queue

            csp[a].append(ordered_pair)

        # NOTE: every set of updates has an odd number of pages
        midpage_sum += pages[len(pages) // 2]

    return midpage_sum


if __name__ == '__main__':
    with open('example-pt1.txt') as f:
        constraints = [c.strip() for c in f.readlines()]
    with open('example-pt2.txt') as f:
        updates = [list(map(int, u.split(','))) for u in f.readlines()]
    assert (ans := part1(constraints, updates)) == 143, ans
    assert (ans := part2(constraints, updates)) == 123, ans

    with open('input-pt1.txt') as f:
        constraints = [c.strip() for c in f.readlines()]
    with open('input-pt2.txt') as f:
        updates = [list(map(int, u.split(','))) for u in f.readlines()]
    print('Part 1:', part1(constraints, updates))
    print('Part 2:', part2(constraints, updates))
