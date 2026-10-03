"""Project Grounded: zet aangeleverde trainer-art (graphics/grounded/trainers/) om naar GBA-formaat.
- Trainerfoto's: 64x64, 15 kleuren + transparant, onder de knieen afgesneden (verkleinen maakt gezichten kapot).
- Overworlds: 9 frames (zuid, noord, west, 2x zuid lopen, 2x noord lopen, 2x west lopen; oost = gespiegeld west).
Gebruik: python3 tools/grounded/trainer_sprites.py"""
from PIL import Image, ImageDraw

SRC = 'graphics/grounded/trainers/'
TRAINERS = 'graphics/trainers/front_pics/'
OW = 'graphics/object_events/pics/people/'
OWPAL = 'graphics/object_events/palettes/'
TRANSPARENT = (115, 197, 164)


def snap(c):
    return tuple((v >> 3) << 3 for v in c[:3])


def palette_of(imgs, n=15):
    """15 kleuren voor alle ondoorzichtige pixels van de plaatjes samen (exact als het past, anders median cut)."""
    px = [snap(im.getpixel((x, y))) for im in imgs for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 127]
    colors = sorted(set(px))
    if len(colors) > n:
        tmp = Image.new('RGB', (len(px), 1))
        tmp.putdata(px)
        q = tmp.quantize(n, method=Image.Quantize.MEDIANCUT).getpalette()[:n * 3]
        colors = sorted(set(snap(tuple(q[i * 3:i * 3 + 3])) for i in range(n)))
    return colors


def index(im, colors):
    out = Image.new('P', im.size, 0)
    for y in range(im.height):
        for x in range(im.width):
            c = im.getpixel((x, y))
            if c[3] > 127:
                c = snap(c)
                out.putpixel((x, y), 1 + min(range(len(colors)), key=lambda i: sum((c[k] - colors[i][k]) ** 2 for k in range(3))))
    full = list(TRANSPARENT) + [v for c in colors for v in c]
    out.putpalette(full + [0] * (768 - len(full)))
    return out


def write_pal(path, colors):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in [TRANSPARENT] + colors + [(0, 0, 0)] * (15 - len(colors)):
            fp.write('%d %d %d\n' % c)


def front_pic(src, box, name):
    im = src.crop(box)
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    part = im.crop((0, 0, im.width, min(64, im.height)))
    out.paste(part, ((64 - part.width) // 2, 0), part)
    colors = palette_of([out])
    index(out, colors).save(TRAINERS + name + '.png')
    return colors


def overworld(frames, w, h, name):
    """frames: 9 RGBA-plaatjes; elk wordt onderaan gecentreerd in een w x h vak."""
    cells = []
    for f in frames:
        c = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        c.paste(f, ((w - f.width) // 2, h - f.height - 1), f)
        cells.append(c)
    colors = palette_of(cells)
    sheet = Image.new('RGBA', (w * 9, h), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        sheet.paste(c, (i * w, 0), c)
    index(sheet, colors).save(OW + name + '.png')
    write_pal(OWPAL + name + '.pal', colors)
    print(name, len(colors), 'kleuren')


# ---------------- Colress
c = Image.open(SRC + 'colress/colress_b2w2_bron.png').convert('RGBA')
front_pic(c, (14, 1, 70, 80), 'colress')
# overworld van PizzaSun: 2x uitvergroot, 4x4 cellen (rijen: zuid, west, oost, noord; kolommen: staan, stap, staan, stap)
ow = Image.open(SRC + 'colress/colress_overworld_pizzasun.png').convert('RGBA').resize((128, 128), Image.NEAREST)
cell = lambda r, k: ow.crop((k * 32, r * 32, k * 32 + 32, r * 32 + 32)).crop(ow.crop((k * 32, r * 32, k * 32 + 32, r * 32 + 32)).getbbox())
overworld([cell(0, 0), cell(3, 0), cell(1, 0), cell(0, 1), cell(0, 3), cell(3, 1), cell(3, 3), cell(1, 1), cell(1, 3)], 32, 32, 'colress')

# ---------------- Zinnia (witte achtergrond -> transparant via floodfill vanaf de randen)
z = Image.open(SRC + 'zinnia/zinnia_bron.png').convert('RGBA')
def clear_white(im):
    im = im.copy()
    for p in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
        if im.getpixel(p)[:3] == (255, 255, 255):
            ImageDraw.floodfill(im, p, (0, 0, 0, 0), thresh=10)
    return im
zt = clear_white(z.crop((66, 0, 130, 90)))
front_pic(zt, zt.getbbox(), 'zinnia')
def zf(x0, y0, x1, y1):
    f = clear_white(z.crop((x0 - 1, y0 - 1, x1 + 2, y1 + 2)))
    return f.crop(f.getbbox())
# rijen: zuid (2 frames), noord (3), west (3)
s0, s1 = zf(3, 2, 18, 22), zf(23, 2, 39, 22)
n0, n1, n2 = zf(3, 30, 18, 49), zf(23, 30, 39, 49), zf(43, 30, 58, 49)
w0, w1, w2 = zf(3, 59, 18, 78), zf(23, 59, 39, 78), zf(43, 59, 58, 78)
overworld([s0, n0, w0, s1, s1.transpose(Image.FLIP_LEFT_RIGHT), n1, n2, w1, w2], 16, 32, 'zinnia')
