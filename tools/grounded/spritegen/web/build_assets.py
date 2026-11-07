"""Verzamelt wat de editor nodig heeft in assets.json: echte Gen 3-sprites (vergelijken), kleurhellingen uit hun
paletten (gids B5: kleuren overnemen van een bestaande sprite) en voorbeeldtekeningen. Draaien vanuit de repo-root."""
import base64, colorsys, io, json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SPRITES = ['vulpix', 'sentret', 'furret', 'zigzagoon', 'linoone', 'rattata', 'poochyena', 'teddiursa', 'eevee', 'meowth',
           'pikachu', 'treecko', 'mudkip', 'torchic', 'hitmonchan']


def uri(im, fmt='PNG', **kw):
    b = io.BytesIO(); im.save(b, fmt, **kw)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()


def sprite(n):
    im = Image.open(f'graphics/pokemon/{n}/anim_front.png')
    a = np.array(im)[:64, :64]
    rgb = np.array(im.convert('RGB'))[:64, :64]
    o = np.zeros((64, 64, 4), np.uint8); o[..., :3] = rgb; o[..., 3] = (a != 0) * 255
    return Image.fromarray(o, 'RGBA'), a, im.getpalette()[:48]


def ramps(a, pal):
    cnt = np.bincount(a.ravel(), minlength=16)
    cols = []
    for i in range(1, 16):
        if cnt[i] < 4:
            continue
        r, g, b = pal[i * 3:i * 3 + 3]
        lum = 0.3 * r + 0.59 * g + 0.11 * b
        if lum < 28 or min(r, g, b) > 238:
            continue
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        cols.append(dict(c=(r, g, b), h=h, s=s, lum=lum, n=int(cnt[i])))
    groups = []
    for c in sorted(cols, key=lambda c: -c['n']):
        for gr in groups:
            g0 = gr[0]
            dh = min(abs(c['h'] - g0['h']), 1 - abs(c['h'] - g0['h']))
            grey = c['s'] < 0.12 and g0['s'] < 0.12
            if grey or (dh < 0.045 and abs(c['s'] - g0['s']) < 0.25 and (c['s'] >= 0.12) == (g0['s'] >= 0.12)):
                gr.append(c); break
        else:
            groups.append([c])
    out = []
    for gr in groups:
        gr = sorted(gr, key=lambda c: -c['lum'])
        if len(gr) < 3:
            continue
        if len(gr) >= 4:
            h, b, s, l = gr[0]['c'], gr[1]['c'], gr[2]['c'], gr[-1]['c']
        else:
            h, b, s = gr[0]['c'], gr[1]['c'], gr[2]['c']; l = tuple(int(v * 0.5) for v in s)
        out.append(dict(h=h, b=b, s=s, l=l, n=sum(c['n'] for c in gr)))
    return sorted(out, key=lambda r: -r['n'])


data = dict(refs={}, presets=[], samples={})
for n in SPRITES:
    im, a, pal = sprite(n)
    data['refs'][n] = uri(im)
    for i, r in enumerate(ramps(a, pal)):
        data['presets'].append(dict(name=f'{n.capitalize()} {i + 1}', h=r['h'], b=r['b'], s=r['s'], l=r['l']))
art = Image.open(os.path.join(HERE, 'assets/vulpix_sugimori.png')).convert('RGB')
VULPIX = {  # de R/S-kleuren van Vulpix, zoals de gids ze voor zijn pixel-over gebruikte
    'oranje': dict(h=(255, 148, 90), b=(222, 115, 41), s=(189, 74, 41), l=(115, 32, 0)),
    'bruin': dict(h=(246, 189, 123), b=(230, 148, 106), s=(189, 115, 90), l=(128, 80, 48)),
    'creme': dict(h=(255, 230, 180), b=(255, 222, 148), s=(246, 189, 123), l=(160, 112, 64))}
data['samples']['vulpix'] = dict(name='Vulpix (gids; DC tekende naar de oude art)', src=uri(art, 'JPEG', quality=90), k=3, compare=['vulpix'], ramps=VULPIX,
                                 extra=uri(Image.open(os.path.join(HERE, 'assets/vulpix_dc_pixelover.png')).convert('RGB')))
HITMONCHAN = {  # R/S-palet van Hitmonchan (graphics/pokemon/hitmonchan/normal.pal)
    'huid': dict(h=(238, 213, 156), b=(205, 180, 123), s=(164, 139, 115), l=(90, 65, 16)),
    'handschoen': dict(h=(255, 148, 90), b=(230, 98, 74), s=(189, 49, 74), l=(139, 32, 0)),
    'tuniek': dict(h=(255, 246, 255), b=(222, 205, 222), s=(197, 180, 197), l=(98, 74, 115))}
hart = Image.open(os.path.join(HERE, 'assets/hitmonchan_sugimori.png')).convert('RGB')
data['samples']['hitmonchan'] = dict(name='Hitmonchan (gids: zelfde tekening als DC)', src=uri(hart, 'JPEG', quality=90), k=5, compare=['hitmonchan'], ramps=HITMONCHAN,
                                     extra=uri(Image.open(os.path.join(HERE, 'assets/hitmonchan_dc_pixelover.png')).convert('RGB')))
tek = Image.open(os.path.join(HERE, 'assets/olinguito_tekening.png')).convert('RGB')
data['samples']['olinguito'] = dict(name='Olinguito (modeltekening)', src=uri(tek), k=6, compare=['zigzagoon', 'linoone', 'sentret'])
json.dump(data, open(os.path.join(HERE, 'assets.json'), 'w'))
print('presets', len(data['presets']), 'kB', os.path.getsize(os.path.join(HERE, 'assets.json')) // 1024)
