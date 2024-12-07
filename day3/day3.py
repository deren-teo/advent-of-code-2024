"""Day 3: Mull It Over"""

import re


def part1(memstr: str) -> int:
    """
    Returns the sum of all fully-formed "mul(x,y)" statements in the string.
    """
    p = re.compile(r'mul\((\d+,\d+)\)')
    muls = re.findall(p, memstr)
    xsum = 0
    for mul in muls:
        x, y = mul.split(',')
        xsum += int(x) * int(y)
    return xsum


def part2(memstr: str) -> int:
    """
    Returns the sum of all full-formed "mul(x,y)" statements in the string,
    where they are preceded by "do()", or at least not preceded by "don't()".
    """
    p = re.compile(r"mul\((\d+,\d+)\)|(do)\(\)|(don't)\(\)")
    instructions = re.findall(p, memstr)
    xsum = 0
    cond = True
    for mul, do, dont in instructions:
        if mul and cond:
            x, y = mul.split(',')
            xsum += int(x) * int(y)
        elif do:
            cond = True
        elif dont:
            cond = False
    return xsum


if __name__ == '__main__':
    with open('example.txt') as f:
        memstr = f.readlines()
    assert (ans := part1(memstr[0])) == 161, ans
    assert (ans := part2(memstr[1])) == 48, ans

    with open('input.txt') as f:
        memstr = f.read()
    print('Part 1:', part1(memstr))
    print('Part 2:', part2(memstr))
