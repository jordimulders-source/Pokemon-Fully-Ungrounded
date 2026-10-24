#!/usr/bin/env python3
"""Knipt de bevroren J-staart van ronde 23 uit (exact dezelfde pixels) en geeft hem terug als {(x,y): kleur}."""
import tools as T
def tail_pixels():
    g = T.read_txt(T.H + '/r23_f1.txt'); P = {}
    for y in range(34, 52):
        for x in range(44, 64):
            v = g[y][x]
            if not v: continue
            take = (y <= 39 and x >= 48) or (40 <= y <= 50 and x >= 49) or (y == 51 and x >= 47) \
                or (45 <= x <= 48 and 46 <= y <= 50) or (x == 44 and y in (48, 49))
            if take: P[(x, y)] = v
    return P
