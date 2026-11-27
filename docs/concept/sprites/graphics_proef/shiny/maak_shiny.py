#!/usr/bin/env python3
"""Shiny-voorstellen voor de nieuwe designs (alleen voorstellen, niets in graphics/ of src/).

Leest de soortenlijst uit showcase/maak_vel.py (SECTIES) en de recepten uit recepten.py
(één idee per lijn, doelkleur per kleurgroep). Per soort: shiny/<slug>_shiny.pal (JASC-PAL,
16 kleuren), shiny/png/<slug>_shiny.png (voorbeeld) en per sectie een vel shiny/vel_<sectie>.png
(3x, normaal | shiny naast elkaar, per lijn een rij met het idee erboven).

Gebruik:  python3 maak_shiny.py            -> alles
          python3 maak_shiny.py idx <slug>  -> indexkaart (kijkhulp) in shiny/idx/
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.abspath(os.path.join(HIER, '../..')) + '/'
ROOT = os.path.abspath(os.path.join(SPR, '../../..')) + '/'
sys.path.insert(0, ROOT + 'tools/grounded/variants')
sys.path.insert(0, HIER)
from colorlib import to_oklch, from_oklch, recolor, gba  # noqa: E402
import recepten  # noqa: E402

F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = F.replace('-Bold', '')


def secties():
    src = open(SPR + 'showcase/maak_vel.py').read()
    ns = {}
    exec(src[src.index('SECTIES=['):src.index('F="/usr')], ns)
    return ns['SECTIES']


def slug_van(pad):
    stem = os.path.splitext(os.path.basename(pad))[0]
    return {'cuyby/ronde4/anim_front.png': 'cuyby', 'cuyby_evo/ronde6/anim_front.png': 'cuychu',
            'emolga_evo/af/model.png': 'colugo'}.get(pad, stem)


def laad(pad):
    """64x64 (bovenste helft van een blad), als (pixels[64*64] met index, palet[16] RGB)."""
    im = Image.open(SPR + pad)
    if im.mode == 'P':
        im = im.crop((0, 0, 64, 64))
        pal = im.getpalette()[:48]
        pal += [0] * (48 - len(pal))
        pal = [tuple(pal[3 * i:3 * i + 3]) for i in range(16)]
        px = list(im.getdata())
        return px, pal
    # RGBA (Scrapstack, glitch-lijn): kleuren op aantal sorteren, index 0 = transparant
    im = im.convert('RGBA').crop((0, 0, 64, 64))
    kl = sorted(((n, c) for n, c in im.getcolors(4096) if c[3]), reverse=True)
    assert len(kl) <= 15, (pad, len(kl))
    pal = [(0, 0, 0)] + [c[:3] for n, c in kl]
    pal += [(0, 0, 0)] * (16 - len(pal))
    nr = {c: i + 1 for i, (n, c) in enumerate(kl)}
    px = [nr.get(c, 0) if c[3] else 0 for c in im.getdata()]
    return px, pal


def doel(pal, idxs, base, spec):
    """spec: '#rrggbb' (absoluut voor de basisindex) of dict(h=, c=, dl=, L=, cm=)."""
    if isinstance(spec, str):
        return spec
    bL, bC, bh = to_oklch(pal[base])
    L = spec.get('L', bL + spec.get('dl', 0.0))
    C = spec['c'] if 'c' in spec else bC * spec.get('cm', 1.0)
    h = spec.get('h', bh)
    return from_oklch(L, C, h)


def shiny_palet(slug, px, pal, optie='A'):
    lijn = recepten.LIJN_VAN[slug]
    rec = lijn if optie == 'A' else lijn['B']
    kleuren = rec['kleuren']
    groepen = lijn['groepen'][slug]
    if optie == 'B' and slug in rec.get('groepen', {}):
        groepen = rec['groepen'][slug]
    tel = [px.count(i) for i in range(16)]
    nieuw = list(pal)
    for groep, idxs in groepen.items():
        idxs = [i for i in idxs if tel[i]] or idxs
        if groep.startswith('_'):
            continue
        spec = kleuren[groep]
        opts = {}
        if isinstance(spec, tuple):
            spec, opts = spec
        base = opts.get('base') if isinstance(opts.get('base'), int) else max(idxs, key=lambda i: tel[i])
        t = doel(pal, idxs, base, spec)
        uit = recolor(pal, idxs, base, t, lscale=opts.get('l', 1.0), hshift=opts.get('hs', 1.0))
        for i, c in uit.items():
            # omlijning (donkere tinten langs de rand) nooit lichter dan het origineel
            if to_oklch(pal[i])[0] < 0.30 and to_oklch(c)[0] > to_oklch(pal[i])[0] + 0.02:
                L0 = to_oklch(pal[i])[0]
                _, C1, h1 = to_oklch(c)
                c = gba(from_oklch(L0, C1, h1))
            nieuw[i] = c
    return [gba(c) if i else pal[0] for i, c in enumerate(nieuw)]


def schrijf_pal(pad, pal):
    with open(pad, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            f.write('%d %d %d\n' % c)


def beeld(px, pal):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    im.putdata([(*pal[i], 255) if i else (0, 0, 0, 0) for i in px])
    return im


def verschil(px, pal, sp):
    """Gemiddelde OKLab-afstand per gekleurde pixel (controle 'nauwelijks anders')."""
    import math
    tot = n = 0
    for i in px:
        if not i:
            continue
        a, b = to_oklch(pal[i]), to_oklch(sp[i])
        da = a[1] * math.cos(math.radians(a[2])) - b[1] * math.cos(math.radians(b[2]))
        db = a[1] * math.sin(math.radians(a[2])) - b[1] * math.sin(math.radians(b[2]))
        tot += math.sqrt((a[0] - b[0]) ** 2 + da * da + db * db)
        n += 1
    return tot / max(n, 1)


def indexkaart(slug):
    for t, items in secties():
        for p, n, ty in items:
            if slug_van(p) == slug:
                px, pal = laad(p)
                S = 12
                img = Image.new('RGB', (64 * S + 220, 64 * S), (255, 255, 255))
                d = ImageDraw.Draw(img)
                f = ImageFont.truetype(FR, 9)
                for y in range(64):
                    for x in range(64):
                        i = px[y * 64 + x]
                        if not i:
                            continue
                        c = pal[i]
                        d.rectangle((x * S, y * S, x * S + S - 1, y * S + S - 1), fill=c)
                        L = to_oklch(c)[0]
                        d.text((x * S + 1, y * S + 1), '%d' % i, font=f, fill=(0, 0, 0) if L > 0.6 else (255, 255, 255))
                fb = ImageFont.truetype(FR, 16)
                for i in range(1, 16):
                    d.rectangle((64 * S + 10, i * 40, 64 * S + 40, i * 40 + 30), fill=pal[i])
                    d.text((64 * S + 50, i * 40 + 6), '%d  %d' % (i, px.count(i)), font=fb, fill=(0, 0, 0))
                os.makedirs(HIER + '/idx', exist_ok=True)
                img.save(HIER + '/idx/%s.png' % slug)
                return


def vel(naam, titel, lijnen, sp_data, S=3):
    """Eén rij (of meer) per lijn: per soort normaal | shiny (| B)."""
    ft = ImageFont.truetype(F, 34)
    fl = ImageFont.truetype(F, 22)
    fi = ImageFont.truetype(FR, 18)
    fn = ImageFont.truetype(F, 17)
    PER = 4  # soorten per rij
    pw = 64 * S
    W = 40 + PER * (3 * pw + 40)
    rijen = []
    for lijn in lijnen:
        n = len(lijn['soorten'])
        breed = 3 if 'B' in lijn else 2
        per = PER if breed == 2 else 3
        rijen.append((lijn, breed, per, (n + per - 1) // per))
    H = 90 + sum(70 + r * (pw + 44) for _, _, _, r in rijen) + 20
    W = max(W, 40 + 3 * (3 * pw + 30))
    img = Image.new('RGB', (W, H), (246, 242, 233))
    d = ImageDraw.Draw(img)
    d.text((20, 22), titel, font=ft, fill=(50, 40, 35))
    y = 90
    for lijn, breed, per, r in rijen:
        idee = lijn['idee'] + ('   |   B: ' + lijn['B']['idee'] if 'B' in lijn else '')
        d.text((20, y + 6), lijn['naam'], font=fl, fill=(90, 60, 40))
        tx = 20 + d.textlength(lijn['naam'], font=fl) + 16
        fz = fi
        z = 18
        while tx + d.textlength(idee, font=fz) > W - 20 and z > 11:
            z -= 1
            fz = ImageFont.truetype(FR, z)
        d.text((tx, y + 10), idee, font=fz, fill=(70, 70, 70))
        d.line((20, y + 40, W - 20, y + 40), fill=(200, 185, 165), width=2)
        y += 52
        cw = breed * pw + 24 + (breed - 1) * 6
        for k, slug in enumerate(lijn['soorten']):
            x = 20 + (k % per) * (cw + 18)
            yy = y + (k // per) * (pw + 44)
            px, pal, nm, shinies = sp_data[slug]
            d.rounded_rectangle((x, yy, x + cw, yy + pw + 36), 10, fill=(255, 253, 248), outline=(220, 212, 198), width=2)
            beelden = [pal] + shinies
            for j, p in enumerate(beelden):
                a = beeld(px, p).resize((pw, pw), Image.NEAREST)
                xx = x + 12 + j * (pw + 6)
                if j:
                    d.rectangle((xx, yy + 4, xx + pw - 1, yy + pw + 3), fill=(236, 242, 250) if j == 1 else (250, 238, 236))
                img.paste(a, (xx, yy + 4), a)
            lab = nm + ('   (normaal | A | B)' if breed == 3 else '')
            f = fn
            z = 17
            while d.textlength(lab, font=f) > cw - 10 and z > 10:
                z -= 1
                f = ImageFont.truetype(F, z)
            d.text((x + (cw - d.textlength(lab, font=f)) / 2, yy + pw + 10), lab, font=f, fill=(40, 35, 30))
        y += r * (pw + 44) + 18
    img = img.crop((0, 0, W, y + 10))
    img.save(HIER + '/' + naam)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == 'idx':
        for s in sys.argv[2:]:
            indexkaart(s)
        return
    os.makedirs(HIER + '/png', exist_ok=True)
    sp_data = {}
    sectie_van = {}
    zwak = []
    for t, items in secties():
        for p, n, ty in items:
            slug = slug_van(p)
            sectie_van[slug] = t
            px, pal = laad(p)
            if slug not in recepten.LIJN_VAN:
                print('GEEN RECEPT', slug)
                continue
            lijn = recepten.LIJN_VAN[slug]
            shinies = []
            for opt in (['A', 'B'] if 'B' in lijn else ['A']):
                sp = shiny_palet(slug, px, pal, opt)
                suf = '' if opt == 'A' else '_B'
                schrijf_pal(HIER + '/%s_shiny%s.pal' % (slug, suf), sp)
                beeld(px, sp).save(HIER + '/png/%s_shiny%s.png' % (slug, suf))
                v = verschil(px, pal, sp)
                if v < 0.035:
                    zwak.append('%s%s %.3f' % (slug, suf, v))
                shinies.append(sp)
            sp_data[slug] = (px, pal, n.replace('"', ''), shinies)
    for z in zwak:
        print('WEINIG VERSCHIL', z)
    groep = {}
    for lijn in recepten.LIJNEN:
        s = sectie_van[lijn['soorten'][0]]
        groep.setdefault(s, []).append(lijn)
    namen = {'New': 'new', 'Evolutions of existing Pokémon': 'evolutions',
             'Regional forms / convergent Pokémon': 'regional', 'Legendaries': 'legendaries'}
    for s, lijnen in groep.items():
        if s == 'New':
            helft = (len(lijnen) + 1) // 2
            vel('vel_new_1.png', 'Shiny-voorstellen — New (1/2)', lijnen[:helft], sp_data)
            vel('vel_new_2.png', 'Shiny-voorstellen — New (2/2)', lijnen[helft:], sp_data)
        else:
            vel('vel_%s.png' % namen[s], 'Shiny-voorstellen — ' + s, lijnen, sp_data)


if __name__ == '__main__':
    main()
