#!/usr/bin/env python3
"""Project Grounded: N en Ghetsis (Pokémon Black/White) voor het Battle Stadium.

Bronnen (graphics/grounded/trainers/):
- n/n_sheet_delgatron_bron.jpg: N-sheet van Delgatron (DeviantArt). Op 1x, maar JPEG: achtergrond via flood fill
  vanaf de rand weg, kleuren samengevoegd tot 15. Trainerfoto = de derde staande pose (armen open), bovenste 62
  rijen (onderkant geditherd weg, zoals de DS-trainerfoto's). Overworld = de HGSS-achtige loopframes (32x32-cellen).
- ghetsis/ghetsis_schreeuw_bron.jpg: schreeuwende Ghetsis (pixel-art op ±5,5x, JPEG). Eerst terug naar het
  pixelraster (132x66; per cel de mediaan), dan een uitsnede van 64x64 rond het hoofd; de hand schuift 14 px naar
  rechts zodat hij in beeld komt.
- ghetsis/ghetsis_overworld_purplezaffre_bron.png: Ghetsis-overworld van PurpleZaffre (DeviantArt), RMXP 4x4, 2x.

De figuren zijn breder dan 16 px (hoed, gewaad), dus de overworlds zijn 32x32 (9 frames, Gen 3-volgorde, eigen
palet); zo hoog als een gewone Gen 3-NPC.
Gebruik: python3 tools/grounded/plasma_sprites.py [voorbeeldmap]
"""
import os, sys
from collections import deque
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'graphics/grounded/trainers/')
BG = (115, 197, 164)
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def gba(c):
    return tuple((v >> 3) << 3 for v in c[:3])


def strip_bg(cell, light=185, sat=40):
    """Witte (JPEG-)achtergrond die met de rand verbonden is transparant maken; wit binnen de omlijning blijft."""
    cell = cell.convert('RGBA')
    px = cell.load()
    W, H = cell.size
    isbg = lambda c: min(c[:3]) >= light and max(c[:3]) - min(c[:3]) < sat
    seen = set()
    q = deque([(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] + [(0, y) for y in range(H)] + [(W - 1, y) for y in range(H)])
    while q:
        x, y = q.popleft()
        if (x, y) in seen or not (0 <= x < W and 0 <= y < H) or not isbg(px[x, y]):
            continue
        seen.add((x, y))
        q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    for x, y in seen:
        px[x, y] = (0, 0, 0, 0)
    # losse JPEG-spikkels (stukjes van max. 3 pixels) weg
    done = set()
    for y0 in range(H):
        for x0 in range(W):
            if (x0, y0) in done or not px[x0, y0][3]:
                continue
            comp, q = [], deque([(x0, y0)])
            while q:
                x, y = q.popleft()
                if (x, y) in done or not (0 <= x < W and 0 <= y < H) or not px[x, y][3]:
                    continue
                done.add((x, y))
                comp.append((x, y))
                q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
            if len(comp) <= 3:
                for p in comp:
                    px[p] = (0, 0, 0, 0)
    return cell


def palette_of(imgs, n=15):
    """Alle zichtbare pixels samen naar n kleuren: eerst k-means naar 40 (JPEG-ruis weg), dan steeds de twee
    dichtstbijzijnde samenvoegen (de meest gebruikte blijft), zodat kleine maar felle kleuren (rode ogen) blijven."""
    pix = [p[:3] for im in imgs for p in im.get_flattened_data() if p[3]]
    strip = Image.new('RGB', (len(pix), 1))
    strip.putdata(pix)
    q = strip.quantize(colors=40, method=Image.Quantize.MEDIANCUT, kmeans=4)
    pal = q.getpalette()
    cnt = {}
    for i in q.get_flattened_data():
        c = gba(pal[i * 3:i * 3 + 3])
        cnt[c] = cnt.get(c, 0) + 1
    dist = lambda a, b: sum(w * (x - y) ** 2 for w, x, y in zip((3, 6, 1), a, b))
    while len(cnt) > n:
        live = list(cnt)
        _, a, b = min((dist(a, b) * min(cnt[a], cnt[b]) ** 0.5, a, b) for i, a in enumerate(live) for b in live[i + 1:])
        keep, drop = (a, b) if cnt[a] >= cnt[b] else (b, a)
        cnt[keep] += cnt.pop(drop)
    return sorted(cnt, key=sum)


def nearest(c, cols):
    return min(range(len(cols)), key=lambda i: sum(w * (a - b) ** 2 for w, a, b in zip((3, 6, 1), c[:3], cols[i])))


def index(img, cols):
    out = Image.new('P', img.size, 0)
    px = img.load()
    cache = {}
    for y in range(img.height):
        for x in range(img.width):
            p = px[x, y]
            if p[3]:
                if p[:3] not in cache:
                    cache[p[:3]] = nearest(p, cols) + 1
                out.putpixel((x, y), cache[p[:3]])
    flat = list(BG)
    for c in cols:
        flat += c
    flat += [0] * (768 - len(flat))
    out.putpalette(flat)
    return out


def fade_bottom(out, rows=8):
    for i in range(rows):
        y = out.height - 1 - i
        t = (rows - i) / (rows + 1)
        for x in range(out.width):
            if out.getpixel((x, y))[3] and BAYER[y % 4][x % 4] < t * 16:
                out.putpixel((x, y), (0, 0, 0, 0))


def write_pal(path, cols):
    flat = [BG] + list(cols) + [(0, 0, 0)] * (15 - len(cols))
    with open(path, 'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in flat:
            f.write(f'{c[0]} {c[1]} {c[2]}\n')


# --- N ---------------------------------------------------------------------------------------------------------
N_SHEET = SRC + 'n/n_sheet_delgatron_bron.jpg'


def n_front():
    im = Image.open(N_SHEET).convert('RGB')
    fig = strip_bg(im.crop((176, 92, 246, 182)))
    x0, y0, x1, y1 = fig.getbbox()
    fig = fig.crop((x0, y0, x1, y0 + 62))
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    out.alpha_composite(fig, ((64 - fig.width) // 2, 2))
    fade_bottom(out)
    return out


# loopframes in de sheet: (rij, kolom) van de 32x32-cellen vanaf (243, 7)
N_FRAMES = [(3, 2), (0, 0), (5, 0), (4, 0), (4, 1), (3, 0), (3, 1), (5, 1), (6, 0)]   # Gen 3-volgorde


def n_overworld():
    im = Image.open(N_SHEET).convert('RGB')
    return [strip_bg(im.crop((243 + 32 * c, 7 + 32 * r, 275 + 32 * c, 39 + 32 * r))) for r, c in N_FRAMES]


# --- Ghetsis ---------------------------------------------------------------------------------------------------
def ghetsis_native():
    """De schreeuwende Ghetsis terug naar zijn pixelraster: cellen van 5,495 px (gemeten met de randen)."""
    im = Image.open(SRC + 'ghetsis/ghetsis_schreeuw_bron.jpg').convert('RGB')
    px = im.load()
    P = 5.495
    xs = [x for x in (k * P + 4.545 for k in range(140)) if 12 < x < 738]
    ys = [y for y in (325.5 + k * P + 3.245 for k in range(-1, 70)) if 322 < y < 682]
    out = Image.new('RGB', (len(xs), len(ys)))
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            blk = [px[int(round(x)) + dx, int(round(y)) + dy] for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
            out.putpixel((i, j), tuple(sorted(c[k] for c in blk)[4] for k in range(3)))
    return out


def ghetsis_front():
    nat = strip_bg(ghetsis_native(), light=230, sat=25)
    hand = nat.crop((0, 34, 38, nat.height))
    nat.alpha_composite(hand, (14, 34))          # hand dichter bij het gezicht
    return nat.crop((36, 1, 100, 65))


def ghetsis_overworld():
    im = Image.open(SRC + 'ghetsis/ghetsis_overworld_purplezaffre_bron.png').convert('RGBA')
    im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)        # 128x128, cellen 32x32
    cells = {}
    for r, d in enumerate(('down', 'left', 'right', 'up')):
        for c in range(4):
            cell = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            cell.alpha_composite(im.crop((c * 32, r * 32, c * 32 + 32, r * 32 + 30)), (0, 2))   # voeten op rij 31
            cells[(d, c)] = cell
    order = [('down', 0), ('up', 0), ('left', 0), ('down', 1), ('down', 3), ('up', 1), ('up', 3), ('left', 1), ('left', 3)]
    return [cells[k] for k in order]


def save_overworld(name, frames):
    cols = palette_of(frames)
    sheet = Image.new('RGBA', (32 * len(frames), 32), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.alpha_composite(f, (32 * i, 0))
    index(sheet, cols).save(os.path.join(ROOT, f'graphics/object_events/pics/people/{name}.png'))
    write_pal(os.path.join(ROOT, f'graphics/object_events/palettes/{name}.pal'), cols)
    return sheet


def save_front(name, img):
    out = index(img, palette_of([img]))
    out.save(os.path.join(ROOT, f'graphics/trainers/front_pics/{name}.png'))
    out.save(SRC + f'{name}/{name}_front.png')
    return out


def main():
    fronts = {'n': save_front('n', n_front()), 'ghetsis': save_front('ghetsis', ghetsis_front())}
    ows = {'n': save_overworld('n', n_overworld()), 'ghetsis': save_overworld('ghetsis', ghetsis_overworld())}
    if len(sys.argv) > 1:   # voorbeelden op 4x
        d = sys.argv[1]
        for k, im in fronts.items():
            im.convert('RGB').resize((256, 256), Image.NEAREST).save(os.path.join(d, f'{k}_front_4x.png'))
        for k in ows:
            im = Image.open(os.path.join(ROOT, f'graphics/object_events/pics/people/{k}.png')).convert('RGB')
            im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(os.path.join(d, f'{k}_overworld_4x.png'))
    print('N en Ghetsis: trainerfoto\'s en overworlds geschreven')


if __name__ == '__main__':
    main()
