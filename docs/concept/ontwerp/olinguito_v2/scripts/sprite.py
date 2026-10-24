"""Olinguito v2 sprite (64x64, Gen 3). Basis: pixel-over van het 3D-poppetje (52°, ±850 px) als letterraster,
daarna handwerk als overlay-rijen in docs/concept/sprites/olinguito_v2/hand.txt (`y x pixels`, '.' = laat staan,
'_' = transparant). Controleert: kleuren <= 15, oppervlak, open randen, rechte randstukken, zwart-aandeel.
Draaien vanuit de repo-root: python3 docs/concept/ontwerp/olinguito_v2/scripts/sprite.py"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d

DIR = os.path.join(HERE, '..', '..', '..', 'sprites', 'olinguito_v2')
TARGET = 850
pop3d.LEG_K = 1.3
R = pop3d.R

PAL = {  # letter -> kleur (15 + transparant)
    'K': '#160D09',  # zwart: omlijning schaduwkant, masker, pupil
    'B': '#3E2618',  # omlijningsbasis vacht/kop, oorrand
    's': '#5C3B26',  # vacht schaduw / verre poten
    'b': '#7A5236',  # vacht basis
    'h': '#97693F',  # vacht hooglicht
    'g': '#5A4839',  # kop schaduw
    'f': '#78624E',  # kop basis
    'l': '#9A8670',  # kop hooglicht, oor binnen
    'm': '#4B3C34',  # snoet
    'n': '#8E4F58',  # neus, voet schaduw
    'p': '#D09A8E',  # voet
    'c': '#F2EAD6',  # klauw licht
    'r': '#B8572C',  # oog onder (lichter roodbruin)
    'e': '#A8401A',  # oog (roodbruin)
    'w': '#FFFFFF',  # glans
}
OUTLINE = {'h': 'B', 'b': 'B', 's': 'B', 'l': 'B', 'f': 'B', 'g': 'B', 'm': 'K', 'n': 'K', 'p': 'n', 'c': 'd', 'd': 'K',
           'e': 'K', 'w': 'K', 'K': 'K', 'B': 'K'}
GROUP_TONES = {  # groep -> (hooglicht, basis, schaduw)
    'fur': 'hbs', 'crown': 'hbs', 'far': 'ssB', 'head': 'lfg', 'muzzle': 'mmm', 'mask': 'KKK', 'eye': 'eee',
    'pupil': 'KKK', 'glint': 'www', 'nose': 'nnn', 'paw': 'ppn', 'farpaw': 'nnn', 'claw': 'ccd', 'ear': 'BBB',
    'earin': 'lll'}
PRIO = ['glint', 'pupil', 'eye', 'nose', 'claw']


def hires():
    m = pop3d.olinguito()
    x0, x1, y0, y1 = pop3d.bbox(m, 52, 8)
    scale = R * (250 / 256) / max(x1 - x0, y1 - y0)
    zbuf, gid, nrm, groups = pop3d.render(m, 52, 8, scale, ((x0 + x1) / 2, (y0 + y1) / 2))
    L = np.array((-0.45, 0.65, 0.62)); L /= np.linalg.norm(L)
    return gid, nrm @ L, zbuf, groups


def best_size(a):
    im = Image.fromarray((a * 255).astype(np.uint8))
    return min(range(30, 64), key=lambda s: abs((np.array(im.resize((s, s), Image.BOX)) > 127).sum() - TARGET))


def base_grid():
    gid, light, z, groups = hires()
    s = best_size(gid >= 0)
    G = [['_'] * s for _ in range(s)]
    Z = np.full((s, s), -1e9)
    for i in range(s):
        for j in range(s):
            y0, y1, x0, x1 = i * R // s, (i + 1) * R // s, j * R // s, (j + 1) * R // s
            g = gid[y0:y1, x0:x1].ravel()
            fig = g >= 0
            if fig.sum() < g.size * 0.5:
                continue
            cnt = np.bincount(g[fig], minlength=len(groups))
            pick = cnt.argmax()
            for pg in PRIO:
                if cnt[groups.index(pg)] >= g.size * (0.22 if pg != 'claw' else 0.3):
                    pick = groups.index(pg); break
            sel = gid[y0:y1, x0:x1] == pick
            lv = light[y0:y1, x0:x1][sel].mean()
            tones = GROUP_TONES[groups[pick]]
            G[i][j] = tones[0] if lv > 0.62 else tones[1] if lv > -0.15 else tones[2]
            Z[i, j] = z[y0:y1, x0:x1][sel].mean()
    G = np.array(G)
    # binnenlijnen: pixel van het voorste deel naast een veel verder deel
    s = G.shape[0]
    out = G.copy()
    for i in range(s):
        for j in range(s):
            if G[i, j] == '_':
                continue
            for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                y, x = i + di, j + dj
                if 0 <= y < s and 0 <= x < s and G[y, x] != '_' and Z[y, x] < Z[i, j] - 9:
                    out[i, j] = 'K' if (di > 0 or dj > 0) else OUTLINE.get(G[i, j], 'K')
    return out


def place(G):
    ys, xs = np.nonzero(G != '_')
    G = G[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = G.shape
    out = np.full((64, 64), '_')
    y0, x0 = 64 - h - 3, (64 - w) // 2
    out[y0:y0 + h, x0:x0 + w] = G
    return out


def silhouette_outline(G):
    """Omtrek: zwart aan de schaduwkant (rechts/onder), omlijningsbasis aan de lichte kant."""
    out = G.copy()
    for i in range(64):
        for j in range(64):
            c = G[i, j]
            if c == '_':
                continue
            nb = {(di, dj): (G[i + di, j + dj] if 0 <= i + di < 64 and 0 <= j + dj < 64 else '_')
                  for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0))}
            outs = [k for k, v in nb.items() if v == '_']
            if not outs or c in 'KBw':
                continue
            shadow = any(di > 0 or dj > 0 for di, dj in outs)
            out[i, j] = 'K' if shadow else OUTLINE.get(c, 'K')
    return out


def apply_hand(G, path):
    if not os.path.exists(path):
        return G
    for ln in open(path):
        ln = ln.split('#')[0].rstrip()
        if not ln.strip():
            continue
        y, x, px = ln.split(None, 2)
        y, x = int(y), int(x)
        for k, ch in enumerate(px):
            if ch != '.':
                G[y, x + k] = ch
    return G


def checks(G):
    fig = G != '_'
    rep = []
    cols = set(G[fig])
    rep.append(f'kleuren {len(cols)} (max 15), oppervlak {fig.sum()} px')
    # open randen: randpixel die geen omlijningskleur heeft
    openr = []
    for i in range(64):
        for j in range(64):
            if fig[i, j] and G[i, j] not in 'KBncl':
                for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    y, x = i + di, j + dj
                    if not (0 <= y < 64 and 0 <= x < 64) or not fig[y, x]:
                        openr.append((j, i)); break
    rep.append(f'open randen: {openr[:20]}{"..." if len(openr) > 20 else ""}')
    # zwart-aandeel van de omtrek
    edge = [(i, j) for i in range(64) for j in range(64) if fig[i, j] and any(
        not (0 <= i + a < 64 and 0 <= j + b < 64) or not fig[i + a, j + b] for a, b in ((0, 1), (1, 0), (0, -1), (-1, 0)))]
    k = sum(G[i, j] == 'K' for i, j in edge)
    rep.append(f'zwart in de omtrek {k / max(1, len(edge)):.2f} (Gen 3 ±0,35–0,6)')
    return rep


def to_rgba(G):
    out = np.zeros((64, 64, 4), np.uint8)
    for k, v in PAL.items():
        m = G == k
        out[m, :3] = [int(v[i:i + 2], 16) for i in (1, 3, 5)]
        out[m, 3] = 255
    return out


def save_indexed(G, path):
    keys = list(PAL)
    idx = np.zeros((64, 64), np.uint8)
    for n, k in enumerate(keys):
        idx[G == k] = n + 1
    im = Image.fromarray(idx, 'P')
    pal = [0, 0, 0]  # index 0 transparant
    for k in keys:
        pal += [int(PAL[k][i:i + 2], 16) for i in (1, 3, 5)]
    im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(path, transparency=0)


def dump(G, path):
    ys, xs = np.nonzero(G != '_')
    x0 = xs.min()
    lines = ['    ' + ''.join(str((x // 10) % 10) for x in range(x0, xs.max() + 1)),
             '    ' + ''.join(str(x % 10) for x in range(x0, xs.max() + 1))]
    for y in range(ys.min(), ys.max() + 1):
        lines.append(f'{y:2d}  ' + ''.join(G[y, x0:xs.max() + 1]).replace('_', '.'))
    open(path, 'w').write('\n'.join(lines) + '\n')


def sheet(G, path):
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    refs = ['linoone', 'zigzagoon', 'poochyena', 'sentret', 'rattata', 'growlithe']
    def ref(n):
        im = Image.open(os.path.join('graphics/pokemon', n, 'anim_front.png'))
        a = np.array(im)[:64, :64]
        rgb = np.array(im.convert('RGB'))[:64, :64]
        o = np.zeros((64, 64, 4), np.uint8); o[..., :3] = rgb; o[..., 3] = (a != 0) * 255
        return Image.fromarray(o, 'RGBA')
    tiles = [('olinguito', Image.fromarray(to_rgba(G), 'RGBA'))] + [(n, ref(n)) for n in refs]
    im = Image.new('RGB', (12 + len(tiles) * 72, 100 + 6 * 64 + 10), 'white')
    d = ImageDraw.Draw(im)
    for i, (n, t) in enumerate(tiles):
        im.paste(t, (12 + i * 72, 8), t)
        d.text((12 + i * 72, 76), n, font=F, fill=(80, 80, 80))
    for k, (n, t) in enumerate(tiles[:3]):
        b = t.resize((64 * 6 if k == 0 else 64 * 3, 64 * 6 if k == 0 else 64 * 3), Image.NEAREST)
        im.paste(b, (12 if k == 0 else 12 + 400, 96 if k <= 1 else 96 + 200), b)
    im.save(path)


def main():
    os.makedirs(DIR, exist_ok=True)
    G = place(base_grid())
    G = apply_hand(G, os.path.join(DIR, 'hand.txt'))
    G = silhouette_outline(G)
    G = apply_hand(G, os.path.join(DIR, 'hand_na.txt'))   # na de automatische omlijning (definitief)
    for r in checks(G):
        print(r)
    dump(G, os.path.join(DIR, 'raster.txt'))
    save_indexed(G, os.path.join(DIR, 'front.png'))
    sheet(G, os.path.join(DIR, 'vel.png'))


if __name__ == '__main__':
    main()
