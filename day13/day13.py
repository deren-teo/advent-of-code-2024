"""Day 13: Claw Contraption"""

import re

from typing import List, Tuple


def parse_machines(machine_str: str):
    """"""
    machine_str = machine_str.split('\n')
    str2int = lambda t: (int(t[0]), int(t[1]))

    p = re.compile(r'X\+(\d+), Y\+(\d+)')
    button_a = str2int(re.findall(p, machine_str[0])[0])
    button_b = str2int(re.findall(p, machine_str[1])[0])

    p = re.compile(r'X=(\d+), Y=(\d+)')
    target = str2int(re.findall(p, machine_str[2])[0])

    return button_a, button_b, target

def linsolve(a: int, b: int, z: int) -> Tuple[int, int]:
    """"""
    n_a = (z[0] - z[1] * b[0] / b[1]) / (a[0] - a[1] * b[0] / b[1])
    n_b = (z[1] - n_a * a[1]) / b[1]
    return round(n_a, 3), round(n_b, 3)


def part1(machines: List[Tuple[int, int, int]]) -> int:
    """"""
    tokens = 0
    for a, b, target in machines:
        n_a, n_b = linsolve(a, b, target)
        if n_a != int(n_a) or n_b != int(n_b):
            continue
        tokens += 3 * n_a + n_b
    return int(tokens)


def part2(machines: List[Tuple[int, int, int]]) -> int:
    """"""
    tokens = 0
    for a, b, target in machines:
        target = target[0] + 1e13, target[1] + 1e13
        n_a, n_b = linsolve(a, b, target)
        if n_a != int(n_a) or n_b != int(n_b):
            continue
        tokens += 3 * n_a + n_b
    return int(tokens)


if __name__ == '__main__':
    with open('example.txt') as f:
        machines = [parse_machines(m) for m in f.read().split('\n\n')]
    assert (ans := part1(machines)) == 480, ans

    with open('input.txt') as f:
        machines = [parse_machines(m) for m in f.read().split('\n\n')]
    print('Part 1:', part1(machines))
    print('Part 2:', part2(machines))
