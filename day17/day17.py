"""Day 17: Chronospatial Computer"""

from typing import List, Tuple


def parse_input(raw_input: str) -> Tuple[List[int], List[int]]:
    """
    Parses a string representation of the three registers and instructions into
    lists of integers.
    """
    raw_lines = raw_input.split('\n')
    registers = map(int, [regstr.split(':')[1] for regstr in raw_lines[:3]])
    inputs = map(int, raw_lines[4].split(':')[1].split(','))
    return list(registers), list(inputs)


def cmb(regs: List[int], opr: int) -> int:
    """
    Evaluates a combo operand; returns a register value for opr in (4, 5, 6).
    """
    return {4: regs[0], 5: regs[1], 6: regs[2]}.get(opr, opr)


def adv(regs: List[int], opr: int):
    opr = cmb(regs, opr)
    regs[0] = int(regs[0] / (2 ** (opr)))

def bdv(regs: List[int], opr: int):
    opr = cmb(regs, opr)
    regs[1] = int(regs[0] / (2 ** (opr)))

def cdv(regs: List[int], opr: int):
    opr = cmb(regs, opr)
    regs[2] = int(regs[0] / (2 ** (opr)))

def bxl(regs: List[int], opr: int):
    regs[1] ^= opr

def bxc(regs: List[int], opr: int):
    regs[1] ^= regs[2]

def bst(regs: List[int], opr: int):
    opr = cmb(regs, opr)
    regs[1] = (opr) & 0b111

def jnz(regs: List[int], opr: int):
    global ptr
    ptr = opr if regs[0] != 0 else ptr + 2

def out(regs: List[int], opr: int):
    global ret
    opr = cmb(regs, opr)
    ret += [opr & 0b111]

OPCODES = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


def part1(registers: List[int], inputs: List[int]) -> str:
    """
    Returns the comma-separated output produced by running the given inputs with
    the given initial register configuration.
    """
    global ptr; ptr = 0
    global ret; ret = []

    while ptr < len(inputs):
        OPCODES[(opcode := inputs[ptr])](registers, inputs[ptr + 1])
        ptr += 2 if opcode != 3 else 0

    return ','.join(map(str, ret))


def part2(inputs: List[int]) -> int:
    """TODO"""


if __name__ == '__main__':
    with open('example-part1-only.txt') as f:
        registers, inputs = parse_input(f.read())
    assert (ans := part1(registers, inputs)) == '4,6,3,5,6,3,5,2,1,0', ans

    with open('input.txt') as f:
        registers, inputs = parse_input(f.read())
    print('Part 1:', part1(registers, inputs))
