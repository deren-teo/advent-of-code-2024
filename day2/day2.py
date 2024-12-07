"""Day 2: Red-Nosed Reports"""

from math import copysign
from typing import List


def is_safe(report: List[int], dampener: bool = False) -> bool:
    """
    Returns True if the numbers in the report are either strictly increasing or
    strictly decreasing, with a maximum step change of 3 in either case.

    If dampener is True, up to one unsafe value may be discarded.
    """
    sgn = copysign(1, report[1] - report[0])
    for i in range(1, len(report)):
        diff = report[i] - report[i - 1]
        if not (1 <= abs(diff) <= 3) or diff * sgn < 0:
            if dampener:
                if i == len(report) - 1:
                    return True
                return is_safe([report[i - 1]] + report[i + 1:], dampener=False) or \
                       is_safe([report[i - 2]] + report[i:],     dampener=False)
            return False
    return True


def part1(reports: List[List[int]]) -> int:
    """
    Returns the number of "safe" reports, defined as all numbers in the report
    being either strictly increasing or decreasing, and with a maximum step
    change of 3 in either case.
    """
    return sum(is_safe(report) for report in reports)


def part2(reports: List[List[int]]) -> int:
    """
    Returns the number of "safe" reports, defined the same way as in Part 1,
    except up to one unsafe value may be discarded and the report remains safe.
    """
    return sum(is_safe(report, dampener=True) for report in reports)


if __name__ == '__main__':
    with open('example.txt') as f:
        reports = [list(map(int, report.split())) for report in f.readlines()]
    assert (ans := part1(reports)) == 2, ans
    assert (ans := part2(reports)) == 4, ans

    with open('input.txt') as f:
        reports = [list(map(int, report.split())) for report in f.readlines()]
    print('Part 1:', part1(reports))
    print('Part 2:', part2(reports))
