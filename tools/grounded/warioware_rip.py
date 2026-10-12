#!/usr/bin/env python3
"""Project Grounded: haalt Wario-art schoon uit WarioWare, Inc. (GBA) voor de Wario-intro (tools/grounded/wario_intro.py).
Speelt de ROM met een vaste invoer (deterministisch: titel, naam invoeren, verhaal, eerste microgames), bewaart op de
gekozen frames IO-registers, palet, VRAM en OAM, en rendert daaruit de losse sprites (OAM-groepen, zonder achtergrond)
en BG-lagen (mode 0) met transparantie. Geen screenshots: zo blijven er geen achtergrondpixels of gaten in de art.
Uitvoer: graphics/grounded/trainers/guests/warioware/<naam>.png (RGBA).
Gebruik: python3.11 tools/grounded/warioware_rip.py "<pad naar WarioWare, Inc. - Mega Microgame$! (USA) (Beta).gba>"
(mgba: python3.11, zie CLAUDE.md)"""
import os, sys, struct
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maptools'))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'graphics/grounded/trainers/guests/warioware')

SHAPES = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64), (1, 0): (16, 8), (1, 1): (32, 8),
          (1, 2): (32, 16), (1, 3): (64, 32), (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}


def pal_rgb(st):
    p = np.frombuffer(st['pal'], '<u2')
    r, g, b = p & 31, (p >> 5) & 31, (p >> 10) & 31
    return np.stack([r, g, b], 1).astype(np.uint8) << 3


def io16(st, off):
    return st['io'][off] | st['io'][off + 1] << 8


def tile4(vram, base, n):
    t = np.frombuffer(vram[base + n * 32: base + n * 32 + 32], np.uint8)
    out = np.zeros(64, np.uint8)
    out[0::2] = t & 15
    out[1::2] = t >> 4
    return out.reshape(8, 8)


def tile8(vram, base, n):
    return np.frombuffer(vram[base + n * 64: base + n * 64 + 64], np.uint8).reshape(8, 8)


def render_bg(st, bg, full=False):
    """RGBA van een tekst-BG (240x160 met scroll, of de hele kaart met full=True)."""
    cnt = io16(st, 8 + 2 * bg)
    hofs, vofs = io16(st, 0x10 + 4 * bg) & 511, io16(st, 0x12 + 4 * bg) & 511
    cb, sb, c8, size = (cnt >> 2) & 3, (cnt >> 8) & 31, (cnt >> 7) & 1, cnt >> 14
    W, H = [(256, 256), (512, 256), (256, 512), (512, 512)][size]
    pal = pal_rgb(st)
    vram = st['vram']
    img = np.zeros((H, W, 4), np.uint8)
    for ty in range(H // 8):
        for tx in range(W // 8):
            blk = (tx // 32) + (ty // 32) * (2 if W == 512 else 1)
            off = sb * 0x800 + blk * 0x800 + ((ty % 32) * 32 + (tx % 32)) * 2
            v = vram[off] | vram[off + 1] << 8
            n, hf, vf, pb = v & 0x3FF, (v >> 10) & 1, (v >> 11) & 1, v >> 12
            t = tile8(vram, cb * 0x4000, n) if c8 else tile4(vram, cb * 0x4000, n)
            if hf:
                t = t[:, ::-1]
            if vf:
                t = t[::-1]
            t = t.astype(np.int32)
            idx = t if c8 else (t + pb * 16) * (t > 0)
            rgb = pal[idx]
            a = (t > 0) * 255
            img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8, :3] = rgb
            img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8, 3] = a
    if full:
        return Image.fromarray(img)
    ys = (np.arange(160) + vofs) % H
    xs = (np.arange(240) + hofs) % W
    return Image.fromarray(img[ys][:, xs])


def sprites(st):
    """Lijst van (x, y, RGBA-beeld, prioriteit, index) van de zichtbare (niet-affine of affine als gewone) sprites."""
    oam = st['oam']
    disp = io16(st, 0)
    map1d = (disp >> 6) & 1
    pal = pal_rgb(st)
    vram = st['vram']
    out = []
    for i in range(128):
        a0, a1, a2 = struct.unpack('<3H', oam[i * 8:i * 8 + 6])
        mode = (a0 >> 8) & 3
        if mode == 2:
            continue
        y, x = a0 & 255, a1 & 511
        if y >= 160:
            y -= 256
        if x >= 240:
            x -= 512
        shape, size = a0 >> 14, a1 >> 14
        if shape == 3:
            continue
        w, h = SHAPES[(shape, size)]
        c8 = (a0 >> 13) & 1
        hf = vf = 0
        if mode == 0:
            hf, vf = (a1 >> 12) & 1, (a1 >> 13) & 1
        tile, prio, pb = a2 & 0x3FF, (a2 >> 10) & 3, a2 >> 12
        img = np.zeros((h, w, 4), np.uint8)
        tw = w // 8
        for ty in range(h // 8):
            for tx in range(tw):
                if map1d:
                    n = tile + (ty * tw + tx) * (2 if c8 else 1)
                else:
                    n = tile + ty * 32 + tx * (2 if c8 else 1)
                n &= 1023
                t = (np.frombuffer(vram[0x10000 + n * 32:0x10000 + n * 32 + 64], np.uint8).reshape(8, 8) if c8
                     else tile4(vram, 0x10000, n))
                t = t.astype(np.int32)
                idx = (256 + t) if c8 else (256 + pb * 16 + t)
                img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8, :3] = pal[idx]
                img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8, 3] = (t > 0) * 255
        if hf:
            img = img[:, ::-1]
        if vf:
            img = img[::-1]
        if mode == 3:
            x, y = x + w // 2, y + h // 2   # dubbel: middenpunt corrigeren (benadering)
        out.append((x, y, Image.fromarray(img), prio, i))
    return out


def render_obj(st, filt=None):
    """Alle sprites op een doorzichtig 240x160-vel (laagste OAM-index bovenop)."""
    canvas = Image.new('RGBA', (240, 160), (0, 0, 0, 0))
    for x, y, im, prio, i in reversed(sprites(st)):
        if filt and not filt(i, x, y, im):
            continue
        canvas.alpha_composite(im, (x, y)) if 0 <= x and 0 <= y and x + im.width <= 240 and y + im.height <= 160 else canvas.paste(im, (x, y), im)
    return canvas



def keys_for(f):
    """Vaste invoer: START rond de titel, daarna om de 24 frames A (en af en toe een richting voor microgames)."""
    if f < 2300:
        return []
    k = []
    if f % 24 < 3:
        k.append('A')
    if 2300 <= f < 2700 and f % 60 < 3:
        k.append('START')
    if f % 90 < 6 and f > 4000:
        k.append(['RIGHT', 'LEFT', 'UP', 'DOWN'][(f // 90) % 4])
    return k



# naam: (frame, bbox (x0, y0, x1, y1) waarin het midden van een sprite moet liggen, of None = alles)
TARGETS = {
    'couch_a': (620, None),                                  # openingsfilm: Wario op de bank
    'idea_cash': (2100, None),                               # openingsfilm: het idee, dollartekens en de denkwolk
    'fly_a': (4955, (90, 80, 240, 180)), 'fly_b': (4970, (90, 40, 240, 160)),   # verhaal: Wario vliegt (zonder wolken)
    'boom': (7390, (0, 100, 80, 160)),                       # microgame-tussenscherm: de bom ontploft
    'bombonly': (5740, None, {112, 113}), 'fuse': (5740, None, {107}), 'spark': (5740, None, {115}),   # de timer
}

def cloudy(im):
    a = np.array(im)
    m = a[:, :, 3] > 0
    if not m.any():
        return True
    c = a[m][:, :3].astype(int)
    grey = (np.abs(c[:, 0] - c[:, 2]) < 24) & (c[:, 0] > 150)
    return grey.mean() > 0.8


def group(st, box, ids=None, nocloud=False):
    canvas = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    for x, y, im, prio, i in reversed(sprites(st)):
        cx, cy = x + im.width // 2, y + im.height // 2
        if ids is not None and i not in ids:
            continue
        if box and not (box[0] <= cx < box[2] and box[1] <= cy < box[3]):
            continue
        if nocloud and cloudy(im):
            continue
        canvas.alpha_composite(im, (x + 128, y + 128))
    bb = canvas.getbbox()
    return canvas.crop(bb) if bb else None


def main():
    from emu import Emu, KEYS
    e = Emu(sys.argv[1])
    want = {}
    for name, tg_ in TARGETS.items():
        want.setdefault(tg_[0], []).append(name)
    want.setdefault(4120, []).append('face')
    os.makedirs(OUT, exist_ok=True)
    for f in range(max(want) + 1):
        e.core.set_keys(*[KEYS[k] for k in keys_for(f)])
        e.core.run_frame()
        if f not in want:
            continue
        m = e.core.memory
        st = {'io': bytes(m.u8[0x04000000 + i] for i in range(0x60)),
              'pal': bytes(m.u8[0x05000000 + i] for i in range(0x400)),
              'vram': bytes(m.u8[0x06000000 + i] for i in range(0x18000)),
              'oam': bytes(m.u8[0x07000000 + i] for i in range(0x400))}
        for name in want[f]:
            if name == 'face':
                im = render_bg(st, 0)
            else:
                tg_ = TARGETS[name]
                im = group(st, tg_[1], tg_[2] if len(tg_) > 2 else None, nocloud=name.startswith('fly'))
            im.save(os.path.join(OUT, name + '.png'))
            print(name, f, im.size)


if __name__ == '__main__':
    main()
