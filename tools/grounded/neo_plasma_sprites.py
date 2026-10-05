#!/usr/bin/env python3
"""Project Grounded: Neo Team Plasma (Pokémon Black 2/White 2) voor het Battle Stadium.

Bronnen (graphics/grounded/trainers/neo_plasma/):
- bw2_plasma_trainers_bron.png: BW2-trainersprites op 1x (witte achtergrond): grunt man en vrouw, Colress, Ghetsis
  (BW2), Zinzolin (paars), een sage (bruin: Rood) en een ninja van de Shadow Triad. Credits: aveontrainer, xMachaku en
  PurpleZaffre (DeviantArt); wie precies welke sprite maakte staat niet in het bestand.
- neo_plasma_grunt_overworld_purplezaffre_bron.png: Neo Plasma-grunt (vrouw), RMXP 4x4 op 2x (PurpleZaffre-stijl).
- neo_plasma_grunt_overworld_klein_bron.png: Neo Plasma-grunt (man), 4x4 op ±2x (een paar rijen/kolommen verschoven).

Trainerfoto's (64x64): de figuur uit de sheet; hoger dan 62 px -> bovenste 62 rijen, onderkant geditherd weg (zoals de
DS-foto's van N); kleinere figuren met de voeten op de onderrand. Kleuren per foto samengevoegd tot 15.
Overworlds: grunt vrouw 32x32 (figuur 17 px breed, zoals N/Ghetsis), grunt man 16x32 (figuur 14x21); 9 frames in de
Gen 3-volgorde, eigen palet. Zinzolin, Rood en de Shadow Triad hebben geen overworld-bron: zij krijgen een bestaande
sprite met een eigen palet (zie OW_RECOLOR).
Gebruik: python3 tools/grounded/neo_plasma_sprites.py [voorbeeldmap]
"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plasma_sprites import strip_bg, palette_of, index, fade_bottom, write_pal

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'graphics/grounded/trainers/neo_plasma/')

# (naam, bbox in de sheet)
FRONTS = {
    'neo_plasma_grunt_m': (13, 31, 61, 99),
    'neo_plasma_grunt_f': (87, 40, 130, 92),
    'rood': (9, 205, 64, 283),
    'zinzolin': (82, 210, 136, 288),
    'shadow_triad': (23, 307, 73, 354),
}


def front(name):
    sheet = Image.open(SRC + 'bw2_plasma_trainers_bron.png').convert('RGB')
    x0, y0, x1, y1 = FRONTS[name]
    fig = strip_bg(sheet.crop((x0 - 1, y0 - 1, x1 + 1, y1 + 1)), light=245, sat=12)
    fig = fig.crop(fig.getbbox())
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if fig.height > 62:
        fig = fig.crop((0, 0, fig.width, 62))
        out.alpha_composite(fig, ((64 - fig.width) // 2, 2))
        fade_bottom(out)
    else:
        out.alpha_composite(fig, ((64 - fig.width) // 2, 64 - fig.height))
    return out


GEN3_ORDER = [('down', 0), ('up', 0), ('left', 0), ('down', 1), ('down', 3), ('up', 1), ('up', 3), ('left', 1), ('left', 3)]
DIRS = ('down', 'left', 'right', 'up')


def grunt_f_overworld():
    im = Image.open(SRC + 'neo_plasma_grunt_overworld_purplezaffre_bron.png').convert('RGBA')
    im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)        # 128x128, cellen 32x32
    cells = {}
    for r, d in enumerate(DIRS):
        for c in range(4):
            cell = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            cell.alpha_composite(im.crop((c * 32, r * 32, c * 32 + 32, r * 32 + 30)), (0, 2))   # voeten op rij 31
            cells[(d, c)] = cell
    return [cells[k] for k in GEN3_ORDER]


def halve(cell):
    """Een (bijna) 2x-cel terug naar 1x: per cel de fase (0/1, 0/1) met de minste afwijkingen binnen de 2x2-blokken."""
    px = cell.load()
    W, H = cell.size
    best = None
    for ox in (0, 1):
        for oy in (0, 1):
            bad = sum(1 for y in range(oy, H - 1, 2) for x in range(ox, W - 1, 2)
                      if len({px[x, y], px[x + 1, y], px[x, y + 1], px[x + 1, y + 1]}) > 1)
            if best is None or bad < best[0]:
                best = (bad, ox, oy)
    _, ox, oy = best
    out = Image.new('RGBA', ((W - ox) // 2, (H - oy) // 2))
    for y in range(out.height):
        for x in range(out.width):
            blk = [px[ox + 2 * x + i, oy + 2 * y + j] for i in (0, 1) for j in (0, 1)]
            out.putpixel((x, y), max(set(blk), key=blk.count))
    return out


def grunt_m_overworld():
    im = Image.open(SRC + 'neo_plasma_grunt_overworld_klein_bron.png').convert('RGBA')
    cells = {}
    for r, d in enumerate(DIRS):
        for c in range(4):
            small = halve(im.crop((c * 32, r * 48, c * 32 + 32, r * 48 + 48)))
            bb = small.getbbox()
            fig = small.crop(bb)
            cell = Image.new('RGBA', (16, 32), (0, 0, 0, 0))
            cell.alpha_composite(fig, ((16 - fig.width) // 2, 32 - fig.height))
            cells[(d, c)] = cell
    return [cells[k] for k in GEN3_ORDER]


# Overworlds zonder bron: een bestaande Gen 3-sprite (9 frames, 16x32) met een eigen palet. {index: kleur}
OW_RECOLOR = {
    # Zinzolin: de Expert (kaal, witte baard) in een paars gewaad met rode accenten
    'zinzolin': ('expert_m', {5: (150, 110, 190), 6: (100, 70, 140), 7: (40, 24, 64),
                              8: (230, 90, 80), 9: (170, 50, 50), 10: (80, 20, 20)}),
    # Rood: dezelfde Expert in bruin met een gouden kraag
    'rood': ('expert_m', {5: (176, 136, 88), 6: (124, 92, 56), 7: (52, 36, 20),
                          8: (232, 196, 72), 9: (176, 140, 32), 10: (88, 68, 12)}),
    # Shadow Triad: de Black Belt in een donkerblauw ninjapak met zilverwit haar en een donkere hoofdband
    'shadow_triad': ('black_belt', {5: (72, 72, 112), 6: (48, 48, 84), 7: (20, 20, 40),
                                    8: (60, 60, 70), 9: (40, 40, 48), 10: (16, 16, 24),
                                    11: (232, 232, 240), 12: (184, 184, 200), 13: (112, 112, 132),
                                    14: (104, 104, 144)}),
}


def recolor_overworld(name):
    base, changes = OW_RECOLOR[name]
    im = Image.open(os.path.join(ROOT, f'graphics/object_events/pics/people/{base}.png'))
    pal = im.getpalette()[:48]
    cols = [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]
    for i, c in changes.items():
        cols[i] = tuple((v >> 3) << 3 for v in c)
    out = im.copy()
    out.putpalette([v for c in cols for v in c] + [0] * (768 - 48))
    out.save(os.path.join(ROOT, f'graphics/object_events/pics/people/{name}.png'))
    with open(os.path.join(ROOT, f'graphics/object_events/palettes/{name}.pal'), 'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            f.write(f'{c[0]} {c[1]} {c[2]}\n')


def save_overworld(name, frames):
    w = frames[0].width
    cols = palette_of(frames)
    sheet = Image.new('RGBA', (w * len(frames), 32), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.alpha_composite(f, (w * i, 0))
    index(sheet, cols).save(os.path.join(ROOT, f'graphics/object_events/pics/people/{name}.png'))
    write_pal(os.path.join(ROOT, f'graphics/object_events/palettes/{name}.pal'), cols)
    return sheet


def save_front(name, img):
    out = index(img, palette_of([img]))
    out.save(os.path.join(ROOT, f'graphics/trainers/front_pics/{name}.png'))
    out.save(SRC + f'{name}_front.png')
    return out


def main():
    fronts = {k: save_front(k, front(k)) for k in FRONTS}
    save_overworld('neo_plasma_grunt_f', grunt_f_overworld())
    save_overworld('neo_plasma_grunt_m', grunt_m_overworld())
    for k in OW_RECOLOR:
        recolor_overworld(k)
    if len(sys.argv) > 1:   # voorbeelden op 4x
        d = sys.argv[1]
        for k, im in fronts.items():
            im.convert('RGB').resize((256, 256), Image.NEAREST).save(os.path.join(d, f'{k}_front_4x.png'))
        for k in ('neo_plasma_grunt_f', 'neo_plasma_grunt_m') + tuple(OW_RECOLOR):
            im = Image.open(os.path.join(ROOT, f'graphics/object_events/pics/people/{k}.png')).convert('RGB')
            im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(os.path.join(d, f'{k}_overworld_4x.png'))
    print('Neo Plasma: trainerfoto\'s en overworlds geschreven')


if __name__ == '__main__':
    main()
