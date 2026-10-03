"""Project Grounded: kleurt de Burglar uit Red/Blue (Game Boy, 4 grijstinten) in Gen 3-stijl in.
Bron: graphics/grounded/trainers/burglar/burglar_redblue_bron.png (56x56, ~5,7x vergroot).
Vorm blijft pixel voor pixel gelijk; per gebied krijgt elke grijstint een kleur uit een eigen ramp.
Uit: graphics/grounded/trainers/burglar/burglar_gen3.png (64x64, 15 kleuren + transparant).
Gebruik: python3 tools/grounded/burglar_sprite.py"""
from PIL import Image, ImageDraw

SRC = 'graphics/grounded/trainers/burglar/burglar_redblue_bron.png'
OUT = 'graphics/grounded/trainers/burglar/burglar_gen3.png'
N = 56
LEVELS = [0, 96, 168, 255]

im = Image.open(SRC).convert('L')
s = 320 / N
g = [[min(range(4), key=lambda i: abs(LEVELS[i] - im.getpixel((int((x + 0.5) * s), int((y + 0.5) * s))))) for x in range(N)] for y in range(N)]

# achtergrond: wit dat via wit aan de rand vastzit
bg = [[False] * N for _ in range(N)]
stack = [(x, y) for x in range(N) for y in (0, N - 1)] + [(x, y) for y in range(N) for x in (0, N - 1)]
while stack:
    x, y = stack.pop()
    if 0 <= x < N and 0 <= y < N and not bg[y][x] and g[y][x] == 3:
        bg[y][x] = True
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

OUTLINE = (40, 32, 48)
# ramps per materiaal: [donker, midden, licht] voor de grijstinten 96, 168, 255; zwart = omlijning
RAMP = {
    'cap':   [(48, 64, 112), (88, 112, 168), (160, 184, 224)],
    'skin':  [(168, 104, 72), (224, 152, 112), (248, 208, 168)],
    'sack':  [(120, 80, 40), (176, 128, 72), (216, 176, 112)],
    'cloth': [(96, 104, 128), (176, 184, 200), (240, 240, 248)],
}
SHOE = (72, 56, 48)

# gezicht per rij (x van-tot); links ervan zit de opgeheven hand, die hoort bij de kleren
FACE = {17: (18, 33), 18: (18, 33), 19: (18, 33), 20: (18, 33), 21: (18, 33), 22: (18, 33), 23: (18, 33),
        24: (19, 33), 25: (19, 33), 26: (20, 33), 27: (20, 32), 28: (21, 31), 29: (22, 30), 30: (23, 29)}


def material(x, y):
    lvl = g[y][x]
    if y <= 16 or (29 <= x <= 41 and y <= 19):
        return 'cap'
    if y in FACE and FACE[y][0] <= x <= FACE[y][1]:
        return 'skin'
    if 33 <= x <= 50 and 23 <= y <= 41 and (lvl in (1, 2) or x >= 42):
        return 'sack'
    return 'cloth'


def is_shoe(x, y):
    return (y >= 40 and x <= 13) or (y >= 47 and 35 <= x <= 45)


def outline(x, y):
    return 0 <= x < N and 0 <= y < N and not bg[y][x] and g[y][x] == 0


out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
for y in range(N):
    for x in range(N):
        if bg[y][x]:
            continue
        lvl = g[y][x]
        if lvl == 0:
            c = SHOE if is_shoe(x, y) else OUTLINE
        else:
            tone = lvl - 1   # 0 donker, 1 midden, 2 licht
            # Gen 3-schaduw: licht van linksboven, dus een tint donkerder tegen de lijn rechts en onder
            if tone > 0 and (outline(x + 1, y) or outline(x, y + 1)):
                tone -= 1
            c = RAMP[material(x, y)][tone]
        out.putpixel((x + 4, y + 8), c + (255,))

# naar 15 kleuren + transparant (index 0)
cols = sorted({out.getpixel((x, y))[:3] for y in range(64) for x in range(64) if out.getpixel((x, y))[3]})
assert len(cols) <= 15, len(cols)
pal = [(115, 197, 164)] + cols
idx = Image.new('P', (64, 64), 0)
idx.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
for y in range(64):
    for x in range(64):
        p = out.getpixel((x, y))
        if p[3]:
            idx.putpixel((x, y), pal.index(p[:3]))
idx.save(OUT)
print(OUT, len(cols), 'kleuren')
