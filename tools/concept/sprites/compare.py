"""Vergelijkend vel: een nieuwe sprite naast Hoenn-sprites van dezelfde fase en
ongeveer dezelfde grootte, op 1x (zoals in de game) en vergroot.

  python3 tools/concept/sprites/compare.py uit.png <map> [--stage N] [--zoom 3] [--n 6] [--with soort,soort]

<map> bevat anim_front.png (+ back.png). Bovenste rij: de nieuwe sprite (frame 1,
frame 2, back) en de buren (frame 1) als GBA-origineel; tweede rij: dezelfde
buren zoals ze nu in de game staan (DPPt-stijl). Daaronder alles op 1x.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import spritelib as L
import measure as M


def tile(im, z):
    bg = L.checker_bg(64 * z, 64 * z, 4 * z)
    if im is not None:
        bg.alpha_composite(L.scaled(im, z))
    return bg


def main():
    a = sys.argv[1:]
    out, d = a.pop(0), a.pop(0)
    stage, z, n, extra = None, 3, 6, []
    while a:
        k = a.pop(0)
        if k == '--stage': stage = int(a.pop(0))
        elif k == '--zoom': z = int(a.pop(0))
        elif k == '--n': n = int(a.pop(0))
        elif k == '--with': extra = a.pop(0).split(',')
    fa, pal = L.load_png(os.path.join(d, 'anim_front.png'))
    fr = [fa[k * 64:(k + 1) * 64] for k in range(fa.shape[0] // 64)]
    bk = None
    if os.path.exists(os.path.join(d, 'back.png')):
        bk = L.load_png(os.path.join(d, 'back.png'))[0][:64]
    area = int((fr[0] > 0).sum())
    st, _, _ = M.evo_stage()
    cand = []
    for s in L.hoenn_species():
        if stage and st(s) != stage:
            continue
        f, _ = L.load_front(s, 'gba')
        cand.append((abs(int((f[0] > 0).sum()) - area), s))
    neigh = extra + [s for _, s in sorted(cand) if s not in extra][:max(0, n - len(extra))]
    own = [L.rgb_img(fr[0], pal), L.rgb_img(fr[-1], pal), L.rgb_img(bk, pal) if bk is not None else None]
    gba = [L.rgb_img(L.load_front(s, 'gba')[0][0], L.load_front(s, 'gba')[1]) for s in neigh]
    new = [L.rgb_img(L.load_front(s, 'new')[0][0], L.load_front(s, 'new')[1]) for s in neigh]
    S = 64 * z
    W = (3 + len(neigh)) * (S + 4)
    H = 2 * (S + 16) + 64 + 40
    sheet = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sheet)
    labels = ['nieuw f1', 'nieuw f2', 'nieuw back'] + neigh
    for j, lab in enumerate(labels):
        dr.text((j * (S + 4) + 2, 0), lab, fill='black')
    for j, im in enumerate(own + gba):
        sheet.paste(tile(im, z), (j * (S + 4), 12))
    dr.text((3 * (S + 4) + 2, S + 14), 'zelfde soorten zoals nu in de game (DPPt-stijl):', fill='black')
    for j, im in enumerate(new):
        sheet.paste(tile(im, z), ((3 + j) * (S + 4), S + 28))
    y = 2 * (S + 16) + 20
    dr.text((2, y - 14), '1x (echte grootte): nieuw | GBA-buren | in-game-buren', fill='black')
    x = 2
    for im in [own[0]] + gba + [None] + new:
        if im is None:
            x += 20; continue
        sheet.paste(tile(im, 1), (x, y)); x += 68
    sheet.save(out)
    print(out, 'buren:', ', '.join(neigh))


if __name__ == '__main__':
    main()
