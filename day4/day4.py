"""Day 4: Ceres Search"""

from typing import List


def cross_search(puzzle: List[str], i: int, j: int, dir: str, target: str = 'MAS') -> bool:
    """
    Returns True if the letters starting from but not including the given
    puzzle coordinates and in the given direction spell out the target word.
    """
    inc_i = {'U': -1, 'UL': -1, 'L':  0, 'DL':  1, 'D': 1, 'DR': 1, 'R': 0, 'UR': -1}[dir]
    inc_j = {'U':  0, 'UL': -1, 'L': -1, 'DL': -1, 'D': 0, 'DR': 1, 'R': 1, 'UR':  1}[dir]
    for letter in target:
        i += inc_i
        j += inc_j
        if puzzle[i][j] != letter:
            return False
    return True


def part1(puzzle: List[str]) -> int:
    """
    Returns the number of "XMAS" strings in the puzzle, where the string may be
    oriented in any of the 8 cardinal and diagonal directions.
    """
    n = len(puzzle)
    m = len(puzzle[0])

    matches = 0
    for i, row in enumerate(puzzle):
        for j, letter in enumerate(row):
            if letter == 'X':
                if i >= 3:
                    matches += cross_search(puzzle, i, j, 'U')
                    if j >= 3:
                        matches += cross_search(puzzle, i, j, 'UL')
                if j >= 3:
                    matches += cross_search(puzzle, i, j, 'L')
                    if i <= n - 4:
                        matches += cross_search(puzzle, i, j, 'DL')
                if i <= n - 4:
                    matches += cross_search(puzzle, i, j, 'D')
                    if j <= m - 4:
                        matches += cross_search(puzzle, i, j, 'DR')
                if j <= m - 4:
                    matches += cross_search(puzzle, i, j, 'R')
                    if i >= 3:
                        matches += cross_search(puzzle, i, j, 'UR')
    return matches


def part2(puzzle: List[str]) -> int:
    """
    Returns the number of crossed "MAS" or "SAM" strings, where two diagonal
    instances of the string intersect at the letter "A".
    """
    n = len(puzzle)
    m = len(puzzle[0])

    matches = 0
    for i in range(n - 2):
        row = puzzle[i].strip()
        for j in range(m - 2):
            letter = row[j]
            if letter == 'M':
                if not cross_search(puzzle, i, j, 'DR', target='AS'):
                    continue
                if row[j + 2] == 'M':
                    matches += cross_search(puzzle, i, j + 2, 'DL', target='AS')
                elif row[j + 2] == 'S':
                    matches += cross_search(puzzle, i, j + 2, 'DL', target='AM')
            elif letter == 'S':
                if not cross_search(puzzle, i, j, 'DR', target='AM'):
                    continue
                if row[j + 2] == 'M':
                    matches += cross_search(puzzle, i, j + 2, 'DL', target='AS')
                elif row[j + 2] == 'S':
                    matches += cross_search(puzzle, i, j + 2, 'DL', target='AM')
    return matches


if __name__ == '__main__':
    with open('example.txt') as f:
        puzzle = f.readlines()
    assert (ans := part1(puzzle)) == 18, ans
    assert (ans := part2(puzzle)) == 9, ans

    with open('input.txt') as f:
        puzzle = f.readlines()
    print('Part 1:', part1(puzzle))
    print('Part 2:', part2(puzzle))
