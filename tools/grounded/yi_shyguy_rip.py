#!/usr/bin/env python3
"""Project Grounded: haalt de achtergrond en het hint-bord voor de Shy Guy-intro (tools/grounded/shyguy_intro.py)
schoon uit Super Mario Advance 3: Yoshi's Island (GBA), zoals warioware_rip.py dat voor Wario deed.
Speelt de ROM met een vaste invoer (deterministisch: titel, nieuw bestand, de openingsfilm, meteen level 1-1), bewaart
op vaste frames IO, palet, VRAM en OAM en rendert daaruit:
- level.png: het begin van 1-1 (bomen, het pijlbord, de gele rots, de bergen) zonder Yoshi en zonder HUD. De BG-lagen
  worden los gerenderd (de scrollregisters zijn niet leesbaar: de scroll is één keer gezocht door de volledige kaarten
  tegen een screenshot te leggen, zie SCROLL) en de lucht komt per beeldlijn uit het screenshot (een HBlank-verloop).
- board.png: het groene hint-bord (OAM) zonder tekst.
- font.png + font.txt: de letters van de hint-borden (uit drie borden met bekende tekst geknipt), voor eigen tekst.
Uitvoer: graphics/grounded/yoshis_island/shyguy_intro/.
Gebruik: python3.11 tools/grounded/yi_shyguy_rip.py "<pad naar Super Mario Advance 3 - Yoshi's Island (USA).gba>"
(de ROM staat gezipt op master; mgba: python3.11, zie CLAUDE.md)"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maptools'))
from warioware_rip import render_bg, render_obj, ROOT

OUT = os.path.join(ROOT, 'graphics/grounded/yoshis_island/shyguy_intro')
SCENE = 3620                      # 1-1, Yoshi staat bij het pijlbord
SCROLL = {1: (24, 4), 2: (12, 62), 3: (28, 274)}   # zoals de game ze op SCENE heeft (gevonden door uitlijnen)
SHIFT = 20                        # wij kijken 20 px verder naar links (meer vlakke grond); BG2 is parallax en blijft
BOARDS = {3320: ["If Baby Mario falls", "off Yoshi's back,", "the Countdown", "Timer will begin."],
          3380: ["When it reaches 0,", "Kamek's toadies", "will swoop in and", "kidnap Baby Mario!"],
          3440: ["The more Stars", "you collect, the", "safer you'll be."]}


def keys_for(f):
    """START/A door titel, bestandskeuze en film; in het level om de 30 frames A (de hint-borden)."""
    k = []
    if f < 3000:
        if f % 40 < 3 and f > 200:
            k.append('START' if (f // 40) % 2 == 0 else 'A')
    elif f % 30 < 3:
        k.append('A')
    return k


def dump(e):
    m = e.core.memory
    return {'io': bytes(m.u8[0x04000000 + i] for i in range(0x60)),
            'pal': bytes(m.u8[0x05000000 + i] for i in range(0x400)),
            'vram': bytes(m.u8[0x06000000 + i] for i in range(0x18000)),
            'oam': bytes(m.u8[0x07000000 + i] for i in range(0x400)),
            'shot': np.array(e.img.to_pil().convert('RGB'))}


def layer(st, b, hx, vy):
    F = np.array(render_bg(st, b, full=True))
    H, W = F.shape[:2]
    return F[(np.arange(160) + vy) % H][:, (np.arange(240) + hx) % W]


def level(st):
    S = st['shot']
    obj = np.array(render_obj(st))
    game = {b: layer(st, b, *SCROLL[b]) for b in SCROLL}
    # controle: de lagen verklaren het screenshot buiten de sprites precies
    out = np.zeros((160, 240, 3), np.uint8)
    none = np.ones((160, 240), bool)
    for b in (2, 1, 3):
        m = game[b][:, :, 3] > 0
        out[m] = game[b][:, :, :3][m]
        none &= ~m
    none &= obj[:, :, 3] == 0
    sky = np.zeros((160, 3), np.uint8)
    for y in range(160):
        px = S[y][none[y]]
        if len(px):
            u, c = np.unique(px, axis=0, return_counts=True)
            sky[y] = u[c.argmax()]
        else:
            sky[y] = sky[y - 1]
    out[none] = sky[np.where(none)[0]]
    bad = (np.abs(out.astype(int) - S.astype(int)).sum(2) > 24) & (obj[:, :, 3] == 0)
    assert bad.sum() < 50, bad.sum()
    # ons beeld: verder naar links
    img = np.zeros((160, 240, 3), np.uint8)
    img[:] = sky[:, None, :]
    for b in (2, 1, 3):
        hx, vy = SCROLL[b]
        L = layer(st, b, hx - (SHIFT if b != 2 else 0), vy)
        m = L[:, :, 3] > 0
        img[m] = L[:, :, :3][m]
    return img


def board_and_font(sts):
    glyphs = {}
    board = None
    for f, lines in BOARDS.items():
        o = np.array(render_obj(sts[f]))
        a = o[:, :, 3] > 0
        rgb = o[:, :, :3].astype(int)
        lum = rgb.sum(2)
        green = a & (rgb[:, :, 1] > rgb[:, :, 0] + 20) & (lum < 450)
        # alleen het bord (brede groene rijen/kolommen), niet Yoshi eronder
        ys = np.where(green.sum(1) > 60)[0]
        xs = np.where(green.sum(0) > 40)[0]
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
        green[:y0] = green[y1 + 1:] = False
        ink = (lum > 600) & a
        ink[:y0 + 2] = ink[y1 - 1:] = False
        ink[:, :x0 + 2] = ink[:, x1 - 1:] = False
        rows = np.where(ink.any(1))[0]
        groups = []
        for r in rows:
            if groups and r - groups[-1][1] <= 2:
                groups[-1][1] = r
            else:
                groups.append([r, r])
        for (gy0, gy1), s in zip(groups, lines):
            cols = np.where(ink[gy0:gy1 + 1].any(0))[0]
            segs = []
            for c in cols:
                if segs and c - segs[-1][1] <= 1:
                    segs[-1][1] = c
                else:
                    segs.append([c, c])
            chars = s.replace(' ', '')
            if len(segs) != len(chars):
                # twee letters raken elkaar ergens: alleen de eerste letter is zeker (de I van "If")
                segs, chars = segs[:1], chars[:1]
            for (c0, c1), ch in zip(segs, chars):
                if ch in glyphs:
                    continue
                # letter in een vak van de regelhoogte (11 px vanaf de bovenkant van de hoofdletters)
                g = ink[gy0 - 1:gy0 + 13, c0:c1 + 1]
                glyphs[ch] = (g, gy0 - 1 - y0)
        if board is None:
            # het bord zonder tekst: inkt en het pijltje onderin worden bordgroen
            b = o[y0 - 12:y1 + 13, x0 - 12:x1 + 13].copy()
            full = np.where((b[:, :, 3] > 0).sum(1) > 100)[0]
            fc = np.where((b[:, :, 3] > 0).sum(0) > 60)[0]
            b = b[full.min():full.max() + 1, fc.min():fc.max() + 1]   # alleen het bord (geen Yoshi of HUD)
            inner = np.zeros(b.shape[:2], bool)
            inner[10:-10, 10:-10] = True
            col = np.median(rgb[green], 0).astype(np.uint8)
            m = inner & (b[:, :, :3].astype(int).sum(2) > 450)
            m |= inner & ~((b[:, :, :3].astype(int) - col.astype(int)).__abs__().sum(2) < 30)
            b[m, :3] = col
            b[m, 3] = 255
            board = b
    return board, glyphs


def main():
    from emu import Emu, KEYS
    e = Emu(sys.argv[1])
    want = set(BOARDS) | {SCENE}
    sts = {}
    for f in range(max(want) + 1):
        e.core.set_keys(*[KEYS[k] for k in keys_for(f)])
        e.core.run_frame()
        if f in want:
            sts[f] = dump(e)
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(level(sts[SCENE])).save(os.path.join(OUT, 'level.png'))
    board, glyphs = board_and_font(sts)
    Image.fromarray(board, 'RGBA').save(os.path.join(OUT, 'board.png'))
    chars = sorted(glyphs)
    w = sum(glyphs[c][0].shape[1] + 1 for c in chars)
    font = np.zeros((14, w), np.uint8)
    x = 0
    with open(os.path.join(OUT, 'font.txt'), 'w') as fp:
        for c in chars:
            g = glyphs[c][0]
            font[:g.shape[0], x:x + g.shape[1]] = g * 255
            fp.write('%s %d %d\n' % (c, x, g.shape[1]))
            x += g.shape[1] + 1
    Image.fromarray(font).save(os.path.join(OUT, 'font.png'))
    print('level, bord %s, %d letters: %s' % (board.shape, len(chars), ''.join(chars)))


if __name__ == '__main__':
    main()
