# Ronde 8 nachtaap (Psychic-starter fase 1), van nul af aan.
# Alles met de hand per lichaamsdeel als tekstraster. Rijen staan in run-length-vorm
# ("3.2V" = 3 transparant, 2 schaduwviolet) zodat de breedte gecontroleerd kan worden;
# elke pixel is met de hand gekozen. Geen vormfuncties, geen automatische schaduw/omlijning.
# Lagen (achter naar voor): staart, lijf (armen, handen, benen), kop.
import re
import sys
from PIL import Image

# Palet (index 0 = transparant). Volgorde = index in normal.pal.
PAL = [
    ('.', (152, 208, 160)),  # 0 transparant
    ('K', (40, 24, 56)),     # 1 bijna-zwart (omlijning schaduwkant, pupil)
    ('O', (88, 56, 120)),    # 2 omlijningsbasis violet
    ('V', (124, 92, 164)),   # 3 schaduw violet
    ('v', (160, 128, 200)),  # 4 basis violet
    ('h', (198, 174, 232)),  # 5 hooglicht violet
    ('D', (206, 172, 140)),  # 6 schaduw crème
    ('C', (240, 220, 182)),  # 7 basis crème
    ('c', (255, 248, 226)),  # 8 hooglicht crème
    ('m', (176, 96, 32)),    # 9 donker amber (iris boven)
    ('a', (232, 160, 48)),   # 10 amber
    ('A', (255, 214, 110)),  # 11 licht amber (gekleurde reflectie, gloed)
    ('w', (255, 255, 255)),  # 12 glans
]
IDX = {ch: i for i, (ch, _) in enumerate(PAL)}


def rle(s):
    out = ''
    for n, ch in re.findall(r'(\d+)(\D)', s):
        out += ch * int(n)
    return out


def rows(spec, width):
    res = []
    for line in spec.strip().split('\n'):
        r = rle(line.split('#')[0].strip())
        assert len(r) == width, (line, len(r), width)
        res.append(r)
    return res


def segs(spec, x0, width):
    """Rijen als 'x:pixels x:pixels' (absolute canvas-x), voor delen met veel losse stukken."""
    res = []
    for line in spec.strip().split('\n'):
        r = ['.'] * width
        for part in line.split('#')[0].split():
            x, px = part.split(':')
            for i, ch in enumerate(px):
                assert r[int(x) - x0 + i] == '.', (line, part)
                r[int(x) - x0 + i] = ch
        res.append(''.join(r))
    return res


# ---------- KOP (26 x 21) ----------
# Ronde gezichtsschijf, 3/4 naar links: achterhoofd (rechts) voller. Twee grote amberogen
# (verre oog smaller), crème halvemaanvlekken boven de ogen, donkere streep ertussen,
# kleine crème snuit met een klein glimlachje. Licht linksboven.
HEAD = rows("""
9. 4V 4O 9.
6. 3V 4h 4v 3O 6.
4. 2V 1v 6h 7v 2O 4.
3. 1V 2v 5h 1v 2V 7v 1V 1O 3.
2. 1V 1v 2c 3C 3v 2V 2v 4C 1D 1v 1V 1O 2.
1. 1O 1v 1c 6C 1D 1v 2V 1v 5C 2D 1v 1V 1O 1.
1. 1O 1v 6C 2D 1v 2V 1v 5C 2D 1v 1V 1O 1.
1. 1O 1v 1C 1D 4K 1C 1D 1v 2V 1v 1D 4K 1C 1D 2v 1V 1O
1O 3v 1K 4m 1K 1D 1v 2V 1v 1K 4m 1K 1D 1v 2V 1K
1O 2v 1K 6m 1K 1v 2V 1K 6m 1K 1v 2V 1K
1O 1v 1K 1m 2w 2K 3m 1K 2V 1K 1m 2w 1K 2m 1K 1v 2V 1K
1O 1v 1K 1a 2w 3K 2a 1K 2V 1K 1a 2w 2K 1a 1K 1v 2V 1K
1O 1v 1K 1a 5K 2a 1K 2V 1K 1a 4K 1a 1K 1v 2V 1K
1O 1v 1K 1a 5K 1a 1A 1K 2V 1K 1a 4K 1A 1K 1v 2V 1K
1O 1v 1K 2a 3K 3A 1K 2V 1K 1a 3K 2A 1K 1v 2V 1K
1O 2v 1K 1a 5A 1K 1c 2C 1K 1a 5A 1K 1v 1V 1K 1.
1. 1O 2v 1K 4A 1K 1c 4C 1K 4A 1K 1v 2V 1K 1.
2. 1O 2v 4K 1c 1O 3C 1O 1D 4K 3V 1K 2.
3. 2O 2v 4C 3O 1C 3D 4V 1K 3.
5. 1O 3K 1V 2C 5D 2V 3K 4.
9. 10K 7.
""", 26)

# ---------- STAART (19 x 31, eerste 5 kolommen = ruimte voor de aanhechting) ----------
# Nazca-spiraal: lint (2 px) loopt rechts omhoog, over de top naar links, onderlangs terug en
# krult in het midden omhoog tot een ronde punt; een open spleet maakt de krul leesbaar.
# Daaronder de steel die schuin naar de rug loopt en achter het lijf verdwijnt.
TAIL = rows("""
10. 4O 5.
8. 2O 2h 2v 1O 1K 3.
7. 1O 3h 4v 1V 1K 2.
6. 1O 1h 2v 4K 1v 2V 1K 1.
5. 1O 1h 2v 1K 4. 1O 1v 2V 1K
5. 1O 1h 1v 1K 1. 2O 3. 1O 1v 1V 1K
5. 1O 2v 1K 1h 1v 1K 3. 1O 1v 1V 1K
5. 1O 2v 1K 2v 1K 3. 1O 1v 1V 1K
5. 1O 2v 1K 2v 1V 1K 2. 1O 1v 1V 1K
5. 1O 5v 2V 1K 1. 1O 1v 1V 1K
6. 1K 3v 5V 1K 1v 1V 1K
7. 1K 7V 1K 1v 1V 1K
8. 2K 4V 2K 1v 1V 1K
10. 4K 1. 1K 1v 1V 1K
15. 1O 1v 1V 1K
15. 1O 1v 1V 1K
14. 1O 1v 1V 1K 1.
13. 1O 1v 1V 1K 2.
12. 1O 1v 1V 1K 3.
11. 1O 1v 1V 1K 4.
10. 1O 1v 1V 1K 5.
9. 1O 1v 1V 1K 6.
8. 1O 1v 1V 1K 7.
7. 1O 1v 1V 1K 8.
6. 1O 1v 1V 1K 9.
5. 1O 1v 1V 1K 10.
4. 1O 1v 1V 1K 11.
3. 1O 1v 1V 1K 12.
2. 1O 1v 1V 1K 13.
1. 1O 1v 1V 1K 14.
1O 1v 1V 1K 15.
""", 19)

# ---------- LIJF (venster x 12..39; rijen y 32..47) ----------
# Zittend, 3/4 naar links. Slanke armen in een V: bovenarm schuin naar de elleboog, onderarm
# terug omhoog naar de handen, die samen onder de kin liggen (zorgzaam gebaar); in de naad
# tussen de handpalmen een amber lichtje. Bolle crème buik, rond knietje met een voetje
# ervoor. De kop werpt slagschaduw op de borst. Rechterkant (rug) rond, niet recht.
BODY = segs("""
20:Ohv 33:VK
19:Ohv 22:O 23:V 24:DDDDDDDDD 33:VV 35:K
18:Ohv 21:O 22:vCC 25:OOOOO 30:CCD 33:OVVK
17:Ohv 20:O 21:vcC 24:OhhvOVO 31:CD 33:OvVVK
17:Ohv 20:O 21:vC 23:OhhvvOVO 31:CD 33:OvVVK
17:Ovvv 21:OOhhvvvOVO 31:DD 33:OvVVK
17:Ovvvvvvv 25:vvVAVK 31:DD 33:OVVVVK
17:KVVVVVV 24:KKKKKK 30:DDD 33:OVVVVK
18:KKKKKK 24:DDDDDDDDD 33:KKKKVK
17:OVVVVVVK 25:CCCCCCDD 33:vVVVVK
16:OhhhvvvvVK 26:cCCCCDD 33:vVVVVK
16:OhvvvvvVVK 26:CCCCDDD 33:vVVVK
14:OOOvvvvVVVVK 26:CCCDDDD 33:VVVVK
13:OhvOvvvVVVVK 25:DDDDDDD 32:VVVVK
13:OvVOVVVVVVK 24:VVVVVVVVVV 34:KK
14:KKKKKKKKKKKKKKKKKKKK
""", 12, 28)
BODY_X, BODY_Y = 12, 32
HEAD_X, HEAD_Y = 14, 12
TAIL_X, TAIL_Y = 37, 14
SHIFT_X, SHIFT_Y = -2, 8


def blit(canvas, grid, ox, oy):
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            if ch != '.':
                canvas[oy + y][ox + x] = ch


def frame(f):
    c = [['.'] * 64 for _ in range(64)]
    hy = HEAD_Y + (1 if f else 0)       # frame 2: kop zakt 1 px (ademhaling)
    ty = TAIL_Y - (1 if f else 0)       # frame 2: spiraal veert 1 px op
    blit(c, TAIL, TAIL_X, ty)
    blit(c, BODY, BODY_X, BODY_Y)
    if f:
        c[BODY_Y + 5][28] = 'a'         # gloed tussen de handen pulseert
    blit(c, HEAD, HEAD_X, hy)
    out = [['.'] * 64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            sx, sy = x - SHIFT_X, y - SHIFT_Y
            if 0 <= sx < 64 and 0 <= sy < 64:
                out[y][x] = c[sy][sx]
    return out


def to_image(fr):
    im = Image.new('P', (64, 64 * len(fr)), 0)
    flat = []
    for (_, rgb) in PAL:
        flat += list(rgb)
    flat += [0, 0, 0] * (16 - len(PAL))
    im.putpalette(flat)
    for i, g in enumerate(fr):
        for y in range(64):
            for x in range(64):
                im.putpixel((x, y + 64 * i), IDX[g[y][x]])
    return im


def write_pal(path):
    cols = [rgb for _, rgb in PAL] + [(0, 0, 0)] * (16 - len(PAL))
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for r, g, b in cols:
            f.write(f'{r} {g} {b}\n')


if __name__ == '__main__':
    outdir = sys.argv[1]
    frames = [frame(0), frame(1)]
    to_image(frames).save(outdir + '/anim_front.png')
    write_pal(outdir + '/normal.pal')
    with open(outdir + '/bron/frame1.txt', 'w') as f:
        f.write('\n'.join(''.join(r) for r in frames[0]) + '\n')
    n = sum(ch != '.' for r in frames[0] for ch in r)
    k = sum(ch == 'K' for r in frames[0] for ch in r)
    print('oppervlak', n, 'px; K', k)
