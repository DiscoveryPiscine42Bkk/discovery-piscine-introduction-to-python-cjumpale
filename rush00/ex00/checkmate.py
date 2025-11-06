#!/usr/bin/env python3
"""
checkmate.py

Behavior:
 - board: multi-line string OR list/tuple of strings (each string is a row)
 - pawn_dir: None (auto), +1 (pawns capture downward), -1 (pawns capture upward)
 - visualize: if True prints attack overlays for Pawn/Bishop/Rook/Queen
 - Prints "Success" (newline) if King is in check, otherwise "Fail".
 - Returns True if king is in check, else False.

This version includes a fallback: if no opposite-case pieces are present, we treat
all pieces (except the King) as enemies so demo boards with only uppercase letters
will still show attacks.
"""
from typing import List, Tuple, Optional, Union

BoardInput = Union[str, List[str], Tuple[str, ...]]


# -------------------------
# Parsing / helpers
# -------------------------
def _parse_board(board: BoardInput) -> List[List[str]]:
    if isinstance(board, str):
        lines = [line.rstrip('\n') for line in board.splitlines() if line.strip() != '']
    else:
        lines = [str(line).rstrip('\n') for line in board]

    if not lines:
        return []

    maxw = max(len(line) for line in lines)
    grid: List[List[str]] = []
    for line in lines:
        row = list(line)
        if len(row) < maxw:
            row += ['.'] * (maxw - len(row))
        grid.append(row)
    return grid


def _in_bounds(grid: List[List[str]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < (len(grid[0]) if grid else 0)


def _find_king(grid: List[List[str]]) -> Optional[Tuple[int, int, str]]:
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch in ('K', 'k'):
                return (i, j, ch)
    return None


def _is_enemy_by_case(ch: str, king_char: str) -> bool:
    """Original behavior: enemy if alphabetical and case differs from king."""
    if not ch or ch == '.' or ch == ' ':
        return False
    if not ch.isalpha():
        return False
    return ch.isupper() != king_char.isupper()


def _pawn_attacks(pos: Tuple[int, int], pawn_dir: int) -> List[Tuple[int, int]]:
    r, c = pos
    return [(r + pawn_dir, c - 1), (r + pawn_dir, c + 1)]


def _knight_attacks(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    r, c = pos
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    return [(r + dr, c + dc) for dr, dc in offsets]


def _linear_attacks(grid: List[List[str]], pos: Tuple[int, int], directions: List[Tuple[int, int]]):
    attacked: List[Tuple[int, int]] = []
    for dr, dc in directions:
        r, c = pos[0] + dr, pos[1] + dc
        while _in_bounds(grid, r, c):
            attacked.append((r, c))
            if grid[r][c] != '.' and grid[r][c] != ' ':
                break
            r += dr
            c += dc
    return attacked


def _compute_pawn_dir_auto(king_r: int, pawn_positions: List[Tuple[int, int]]) -> Optional[int]:
    if not pawn_positions:
        return None
    avg_row = sum(r for r, _ in pawn_positions) / len(pawn_positions)
    return 1 if avg_row < king_r else -1


# -------------------------
# Overlay builder
# -------------------------
def _build_overlay(grid: List[List[str]],
                   king_char: str,
                   target_kinds: Tuple[str, ...],
                   pawn_dir_override: Optional[int],
                   consider_all_enemies: bool = False) -> List[List[str]]:
    """
    Build overlay where X marks attacked squares by enemy pieces of types in target_kinds.
    If consider_all_enemies=True then every alphabetic piece that is not the king_char is
    considered an enemy (fallback mode).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    overlay = [['.' for _ in range(cols)] for _ in range(rows)]

    # copy original pieces into overlay
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != '.' and ch != ' ':
                overlay[r][c] = ch

    enemy_positions: List[Tuple[Tuple[int, int], str]] = []
    pawn_positions: List[Tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if not ch or not ch.isalpha():
                continue
            # determine if ch is enemy either by case or by fallback
            is_enemy = False
            if consider_all_enemies:
                # treat any piece except the king itself as enemy
                if ch != king_char:
                    is_enemy = True
            else:
                is_enemy = _is_enemy_by_case(ch, king_char)

            if is_enemy and ch.lower() in target_kinds:
                enemy_positions.append(((r, c), ch))
                if ch.lower() == 'p':
                    pawn_positions.append((r, c))

    pawn_dir = pawn_dir_override
    if pawn_dir is None and pawn_positions:
        king_pos = _find_king(grid)
        if king_pos:
            pawn_dir = _compute_pawn_dir_auto(king_pos[0], pawn_positions)

    for (r, c), ch in enemy_positions:
        kind = ch.lower()
        if kind == 'p':
            if pawn_dir is None:
                continue
            for ar, ac in _pawn_attacks((r, c), pawn_dir):
                if _in_bounds(grid, ar, ac):
                    if overlay[ar][ac] == '.':
                        overlay[ar][ac] = 'X'
                    elif overlay[ar][ac] in ('K', 'k'):
                        overlay[ar][ac] = 'X'
        elif kind == 'n':
            for ar, ac in _knight_attacks((r, c)):
                if _in_bounds(grid, ar, ac):
                    if overlay[ar][ac] == '.':
                        overlay[ar][ac] = 'X'
                    elif overlay[ar][ac] in ('K', 'k'):
                        overlay[ar][ac] = 'X'
        # rook-like (r and q)
        if kind in ('r', 'q'):
            straights = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for ar, ac in _linear_attacks(grid, (r, c), straights):
                if overlay[ar][ac] == '.':
                    overlay[ar][ac] = 'X'
                elif overlay[ar][ac] in ('K', 'k'):
                    overlay[ar][ac] = 'X'
        # bishop-like (b and q)
        if kind in ('b', 'q'):
            diags = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for ar, ac in _linear_attacks(grid, (r, c), diags):
                if overlay[ar][ac] == '.':
                    overlay[ar][ac] = 'X'
                elif overlay[ar][ac] in ('K', 'k'):
                    overlay[ar][ac] = 'X'

    return overlay


def _print_overlay(label: str, overlay: List[List[str]], left_indent: int = 4, col_sep: str = '  ') -> None:
    """
    Print a label (e.g. 'Pawn (P):') then the overlay grid indented.
    Columns are separated by `col_sep` (default two spaces) to match the image style.
    """
    print(label)
    indent = ' ' * left_indent
    for row in overlay:
        # use '.' for empty, preserve piece letters and 'X'
        print(indent + col_sep.join(ch if ch != ' ' else '.' for ch in row))
    print()


# -------------------------
# Public function
# -------------------------
def checkmate(board: BoardInput, pawn_dir: Optional[int] = None, visualize: bool = True) -> bool:
    """
    Return True if King is in check, else False.
    Also prints "Success"/"Fail" (with newline). If visualize=True prints overlays.
    Default visualize=True for interactive usage.
    """
    grid = _parse_board(board)
    king_info = _find_king(grid)
    if not king_info:
        # undefined in spec -> treat as not in check and print Fail
        print("Fail")
        return False

    kr, kc, kch = king_info

    # Determine if there exist opposite-case enemy pieces. If none, enable fallback.
    has_opposite_case = False
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            ch = grid[r][c]
            if ch and ch.isalpha() and _is_enemy_by_case(ch, kch):
                has_opposite_case = True
                break
        if has_opposite_case:
            break
    consider_all_enemies = not has_opposite_case

    # build overlays for pawn/bishop/rook/queen (pass fallback flag)
    pawn_overlay = _build_overlay(grid, kch, ('p',), pawn_dir, consider_all_enemies)
    bishop_overlay = _build_overlay(grid, kch, ('b',), pawn_dir, consider_all_enemies)
    rook_overlay = _build_overlay(grid, kch, ('r',), pawn_dir, consider_all_enemies)
    queen_overlay = _build_overlay(grid, kch, ('q',), pawn_dir, consider_all_enemies)

    attacked = False
    for ov in (pawn_overlay, bishop_overlay, rook_overlay, queen_overlay):
        if _in_bounds(ov, kr, kc) and ov[kr][kc] == 'X':
            attacked = True
            break

    # explicitly check knights; use fallback if enabled
    if not attacked:
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                ch = grid[r][c]
                if not ch or not ch.isalpha():
                    continue
                is_enemy = consider_all_enemies and (ch != kch) or (not consider_all_enemies and _is_enemy_by_case(ch, kch))
                if ch.lower() == 'n' and is_enemy:
                    for ar, ac in _knight_attacks((r, c)):
                        if (ar, ac) == (kr, kc):
                            attacked = True
                            break
                if attacked:
                    break
            if attacked:
                break

    # print result for backward compatibility
    print("Success" if attacked else "Fail")

    if visualize:
        # two blank lines to create top margin like in screenshot
        print()
        print()
        _print_overlay("Pawn (P):", pawn_overlay, left_indent=4, col_sep='  ')
        _print_overlay("Bishop (B):", bishop_overlay, left_indent=4, col_sep='  ')
        _print_overlay("Rook (R):", rook_overlay, left_indent=4, col_sep='  ')
        _print_overlay("Queen (Q):", queen_overlay, left_indent=4, col_sep='  ')

    return attacked


__all__ = ["checkmate"]


if __name__ == "__main__":
    demo = [
        "R...",
        ".K..",
        "..P.",
        "....",
    ]
    res = checkmate(demo, pawn_dir=None, visualize=True)
    print("Returned value:", res)
