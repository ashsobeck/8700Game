import pygame
from blocker import Blocker


# makes a row of Blockers for random levels
def make_row(x: int, y: int, len: int, block: Blocker):
    blockers = [block.clone(x+i, y) for i in range(len)]
    return blockers


# makes a column of Blockers for random levels
def make_col(x: int, y: int, len: int, block: Blocker):
    blockers = [block.clone(x, y+i) for i in range(len)]
    return blockers


# makes a corner of shape:
# ------
# |
# |
def make_corner(x: int, y: int, len: int, block: Blocker):
    x_blockers = [block.clone(x+i, y) for i in range(len)]
    y_blockers = [block.clone(x, y+i) for i in range(len)]
    return x_blockers + y_blockers


# makes a diagonal line 
def make_diagonal(x: int, y: int, len: int, block: Blocker):
    blockers = [block.clone(x+i, y+i) for i in range(len)]
