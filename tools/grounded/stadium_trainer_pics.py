"""Project Grounded: trainerfoto's voor het Battle Stadium.

Bronnen (eenmalig gedownload, staan in graphics/grounded/trainers/stadium_bron/):
- frlg/      : pret/pokefirered graphics/trainers/front_pics/*_front_pic.png (al 64x64, 16 kleuren) -> 1-op-1 gekopieerd.
- platinum/  : pret/pokeplatinum res/trainers/classes/<klasse>/front.png (80x80-frames onder elkaar, stap 81 px).
               Eén frame wordt bijgesneden (niet verkleind: verkleinen maakt gezichten kapot, zie Colress/Zinnia):
               hoger dan 64 px -> bovenste 64 rijen (afgesneden onder de knieën); lager -> onderaan uitgelijnd.
               De DS-sprites hebben al 15 kleuren + transparant (index 0), dus de indices blijven behouden.
Gebruik: python3 tools/grounded/stadium_trainer_pics.py
"""
import shutil
from PIL import Image

SRC = 'graphics/grounded/trainers/stadium_bron/'
OUT = 'graphics/trainers/front_pics/'

FRLG = {
    'leader_misty': 'leader_misty',
    'leader_lt_surge': 'leader_lt_surge',
    'leader_erika': 'leader_erika',
    'leader_koga': 'leader_koga',
    'leader_sabrina': 'leader_sabrina',
    'leader_blaine': 'leader_blaine',
    'leader_giovanni': 'boss_giovanni',
    'elite_four_lorelei': 'elite_four_lorelei',
    'elite_four_bruno': 'elite_four_bruno',
    'elite_four_agatha': 'elite_four_agatha',
    'elite_four_lance': 'elite_four_lance',
    'champion_rival': 'champion_blue',
}

# bron: (uitvoernaam, frame)
PLATINUM = {
    'leader_roark': ('leader_roark', 0),
    'leader_gardenia': ('leader_gardenia', 0),
    'leader_maylene': ('leader_maylene', 0),
    'leader_wake': ('leader_wake', 2),  # frame 0 heeft de armen te wijd (73 px)
    'leader_fantina': ('leader_fantina', 6),  # frame 0 staat met de rug naar ons; 6 = gezicht, arm naar de speler
    'leader_byron': ('leader_byron', 0),
    'leader_candice': ('leader_candice', 0),
    'leader_volkner': ('leader_volkner', 0),
    'elite_four_aaron': ('elite_four_aaron', 8),  # frame 0 springt weg (achterhoofd); 8 = gezicht, armen gespreid
    'elite_four_bertha': ('elite_four_bertha', 0),
    'elite_four_flint': ('elite_four_flint', 0),
    'elite_four_lucian': ('elite_four_lucian', 0),
    'champion_cynthia': ('champion_cynthia', 0),
    'galactic_boss': ('boss_cyrus', 0),
    'commander_mars': ('commander_mars', 0),
    'commander_jupiter': ('commander_jupiter', 0),
    'commander_saturn': ('commander_saturn', 0),
    'rival': ('rival_barry', 0),
    'tower_tycoon': ('tower_tycoon_palmer', 0),
    'factory_head': ('factory_head_thorton', 0),
    'hall_matron': ('hall_matron_argenta', 0),
    'arcade_star': ('arcade_star_dahlia', 0),
    'trainer_riley': ('riley', 0),
}


# Geordende dither (Bayer 4x4): onderaan afgesneden plaatjes lossen geleidelijk op i.p.v. een harde snede
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def fade_bottom(out, rows=8):
    for i in range(rows):
        y = 63 - i
        t = (rows - i) / (rows + 1)
        for x in range(64):
            if out.getpixel((x, y)) and BAYER[y % 4][x % 4] < t * 16:
                out.putpixel((x, y), 0)


def convert_ds(src, frame):
    im = Image.open(src)
    pal = im.getpalette()
    fr = im.crop((0, frame * 81, 80, frame * 81 + 80))
    x0, y0, x1, y1 = fr.point(lambda v: 255 if v else 0).getbbox()
    w, h = x1 - x0, y1 - y0
    if w > 64:  # midden houden
        x0 += (w - 64) // 2
        w = 64
    part = fr.crop((x0, y0, x0 + w, y0 + min(h, 64)))
    used = sorted(set(part.getdata()) - {0})
    assert len(used) <= 15, (src, len(used))
    remap = {0: 0}
    for i, v in enumerate(used):
        remap[v] = i + 1
    out = Image.new('P', (64, 64), 0)
    px = (64 - part.width) // 2
    py = 0 if h >= 64 else 64 - part.height
    for y in range(part.height):
        for x in range(part.width):
            out.putpixel((px + x, py + y), remap[part.getpixel((x, y))])
    newpal = []
    for v in [0] + used:
        newpal += [(c >> 3) << 3 for c in pal[v * 3:v * 3 + 3]]
    newpal += [0] * (48 - len(newpal))
    out.putpalette(newpal + [0] * (768 - len(newpal)))
    if h > 64:  # onder de knieën afgesneden: laten oplossen (Jordi: 'slim verbergen')
        fade_bottom(out)
    return out


for s, d in FRLG.items():
    shutil.copy(SRC + 'frlg/' + s + '.png', OUT + d + '.png')
for s, (d, frame) in PLATINUM.items():
    convert_ds(SRC + 'platinum/' + s + '.png', frame).save(OUT + d + '.png')
print(len(FRLG) + len(PLATINUM), 'trainerfoto\'s geschreven')
