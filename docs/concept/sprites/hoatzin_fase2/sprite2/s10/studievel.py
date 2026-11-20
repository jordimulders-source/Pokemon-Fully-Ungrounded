# studievel.py: vel.png = s10 | s9 | model (8x) + per onderdeel een uitsnede van het voorbeeld (links) naast s10 (rechts), 8x
from PIL import Image, ImageDraw
P = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
nu = Image.open('hoatzin.png').convert('RGBA'); vor = Image.open('../s9/hoatzin.png').convert('RGBA')
mod = Image.open('../../MODEL.png').convert('RGB')
def ref(n): return Image.open(P + n + '/anim_front.png').convert('RGB').crop((0, 0, 64, 64))
DELEN = [  # naam, voorbeeld, uitsnede voorbeeld, uitsnede hoatzin
    ('vleugel: Braviary (vlak + korte donkere penstreepjes, zwart alleen buiten)', 'braviary', (36, 0, 64, 28), (30, 4, 58, 32)),
    ('lijf: Honchkrow (lichte zone linksboven, donkere zone, donkere binnenlijn)', 'honchkrow', (26, 20, 54, 48), (24, 26, 52, 54)),
    ('creme: Staraptor-borst (wit, schaduw grijs rechtsonder)', 'staraptor', (10, 18, 30, 38), (8, 28, 28, 48)),
    ('kuif: Pidgeot (licht linksboven, donker onder, zwarte buitenlijn)', 'pidgeot', (30, 8, 54, 22), (0, 16, 24, 30)),
    ('poten: Honchkrow (grijs, zwarte lijn, lichte klauwpunt)', 'honchkrow', (26, 44, 46, 60), (16, 48, 46, 62)),
]
S = 8
V = Image.new('RGB', (3 * 520, 520 + len(DELEN) * 250), (255, 255, 255)); d = ImageDraw.Draw(V)
for i, im in enumerate((nu, vor)):
    b = im.resize((512, 512), Image.NEAREST); V.paste(b, (i * 520, 0), b)
V.paste(mod.resize((512, 512), Image.LANCZOS), (1040, 0))
y = 520
for naam, n, a, b in DELEN:
    d.text((4, y + 2), naam, fill=(0, 0, 0))
    r = ref(n).crop(a); r = r.resize((r.width * S, r.height * S), Image.NEAREST)
    h = nu.crop(b); h = h.resize((h.width * S, h.height * S), Image.NEAREST)
    k = 230 / max(r.height, h.height)
    r = r.resize((int(r.width * k), int(r.height * k)), Image.NEAREST); h = h.resize((int(h.width * k), int(h.height * k)), Image.NEAREST)
    V.paste(r, (4, y + 16)); V.paste(h, (r.width + 24, y + 16), h)
    y += 250
V.save('vel.png')
