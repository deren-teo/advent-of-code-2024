"""Day 7: Bridge Repair"""

from typing import List

from tqdm import tqdm


def is_possible_equation(target: int, inputs: List[int], concat: bool = False) -> bool:
    """
    Returns whether all of the inputs can be combined left-to-right using only
    '+' and '*' (and '||' if concat is True) operators to achieve the target.
    Target and all inputs must be positive integers.
    """
    if len(inputs) == 1:
        return inputs[0] == target
    if inputs[0] > target:
        return False
    in0, in1 = inputs[:2]
    if concat:
        in01 = int(str(in0) + str(in1))
        return is_possible_equation(target, [in0 + in1] + inputs[2:], concat=True) or \
               is_possible_equation(target, [in0 * in1] + inputs[2:], concat=True) or \
               is_possible_equation(target, [in01] + inputs[2:], concat=True)
    else:
        return is_possible_equation(target, [in0 + in1] + inputs[2:]) or \
               is_possible_equation(target, [in0 * in1] + inputs[2:])


def part1(equations: List[str], show_progress: bool = False) -> int:
    """
    Returns the sum of the targets which can be achieved by applying only the
    "+" and "*" operators to the inputs in left-to-right order.
    """
    loop_wrapper = lambda z: tqdm(z) if show_progress else z

    target_sum = 0
    for eq in loop_wrapper(equations):
        target, inputs = eq.split(':')
        if is_possible_equation(int(target), list(map(int, inputs.split()))):
            target_sum += int(target)
    return target_sum


def part2(equations: List[str], show_progress: bool = False) -> int:
    """
    Returns the sum of the targets which can be achieved by applying the "+",
    "*" and "||" (concatenation) operators to the inputs in left-to-right order.
    """
    loop_wrapper = lambda z: tqdm(z) if show_progress else z

    target_sum = 0
    for eq in loop_wrapper(equations):
        target, inputs = eq.split(':')
        target = int(target)
        inputs = list(map(int, inputs.split()))
        if is_possible_equation(target, inputs, concat=True):
            target_sum += target

    return target_sum


if __name__ == '__main__':
    with open('example.txt') as f:
        equations = f.readlines()
    assert (ans := part1(equations)) == 3749, ans
    assert (ans := part2(equations)) == 11387, ans

    with open('input.txt') as f:
        equations = f.readlines()
    print('Part 1:', part1(equations, show_progress=True))
    print('Part 2:', part2(equations, show_progress=True))
