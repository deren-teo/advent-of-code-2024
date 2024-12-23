"""Day 23: LAN Party"""

from collections import defaultdict
from copy import deepcopy
from itertools import permutations
from typing import Dict, List, Set, Tuple


def create_adjacency_list(connections: List[Tuple[str]]) -> Dict[str, Set[str]]:
    """"""
    adj_list = defaultdict(set)
    for c1, c2 in connections:
        adj_list[c1].add(c2)
        adj_list[c2].add(c1)
    return adj_list

def find_triads(connections: List[Tuple[str]]) -> Set[Tuple[str, str, str]]:
    """"""
    adj_list = create_adjacency_list(connections)
    triads = set()
    for c1, c1_linked in adj_list.items():
        for c2 in c1_linked:
            for c3 in (c1_linked & adj_list[c2]):
                if not any(p for p in permutations([c1, c2, c3]) if p in triads):
                    triads.add((c1, c2, c3))

    return triads

def find_maximal_cliques(adj_list: Dict[str, Set[str]]) -> List[Set]:
    """
    Returns a list of all maximal cliques in the given connections, found using
    the Bron-Kerbosch algorithm.
    """
    maximal_cliques = []

    def bron_kerbosch(R: Set, P: Set, X: Set):
        """
        https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
        """
        if len(P) == 0 and len(X) == 0:
            maximal_cliques.append(R)
        else:
            for v in deepcopy(P):
                bron_kerbosch(R | {v}, P & adj_list[v], X & adj_list[v])
                P.remove(v)
                X.add(v)

    bron_kerbosch(set(), set(adj_list.keys()), set())
    return maximal_cliques


def part1(connections: List[Tuple[str]]) -> int:
    """
    Returns the number of cliques of size 3 containing at least one computer
    with a name starting with the letter "t".
    """
    triads = find_triads(connections)
    possible_targets = set()
    for c1, c2 in connections:
        if c1.startswith('t'):
            possible_targets.add(c1)
        if c2.startswith('t'):
            possible_targets.add(c2)
    return len([t for t in triads if any(c for c in possible_targets if c in t)])


def part2(connections: List[Tuple[str]]) -> str:
    """
    Finds the largest clique in the given connections. Returns the names of the
    computers in the clique, sorted alphabetically and joined by commas.
    """
    maximal_cliques = find_maximal_cliques(create_adjacency_list(connections))
    maximum_clique = sorted(maximal_cliques, key=lambda c: len(c))[-1]
    return ','.join(sorted(maximum_clique))


if __name__ == '__main__':
    with open('example.txt') as f:
        connections = [tuple(line.strip().split('-')) for line in f.readlines()]
    assert (ans := part1(connections)) == 7, ans
    assert (ans := part2(connections)) == 'co,de,ka,ta', ans

    with open('input.txt') as f:
        connections = [tuple(line.strip().split('-')) for line in f.readlines()]
    print('Part 1:', part1(connections))
    print('Part 2:', part2(connections))
