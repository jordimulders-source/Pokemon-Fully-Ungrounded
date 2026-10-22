"""Handwerk bovenop de gegenereerde basis: patches (x0, y0, rijen); '.' = laten."""
import sys
def load(p): return [list(l.rstrip('\n')[1:-1]) for l in open(p)]
def save(g,p):
    with open(p,'w') as f:
        for r in g: f.write('|'+''.join(r)+'|\n')
def patch(g,x0,y0,rows):
    for dy,r in enumerate(rows):
        for dx,c in enumerate(r):
            if c!='.': g[y0+dy][x0+dx]=c
def shift(g,dx):
    out=[[' ']*64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            if g[y][x]!=' ' and 0<=x+dx<64: out[y][x+dx]=g[y][x]
    return out
