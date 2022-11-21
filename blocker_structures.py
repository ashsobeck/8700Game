import pygame
from blocker import Blocker


# makes a row of Blockers for random levels
def make_row(x: int, y: int, length: int, block: Blocker):
    print(x, y, length)
    blockers = [block.clone(x+i, y) for i in range(length)]
    return blockers


# makes a column of Blockers for random levels
def make_col(x: int, y: int, length: int, block: Blocker):
    blockers = [block.clone(x, y+i) for i in range(length)]
    return blockers


# makes a corner of shape:
# ------
# |
# |
def make_corner(x: int, y: int, length: int, block: Blocker):
    x_blockers = [block.clone(x+i, y) for i in range(length)]
    y_blockers = [block.clone(x, y+i) for i in range(length)]
    return x_blockers + y_blockers


# makes a diagonal line 
def make_diagonal(x: int, y: int, length: int, block: Blocker):
    blockers = [block.clone(x+i, y+i) for i in range(length)]
