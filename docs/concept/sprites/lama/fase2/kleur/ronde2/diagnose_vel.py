"""Diagnosevel lama fase 2 ronde 2: bron (poppetje, onderlaag, foto's 1/3/4, alpaca) naast ronde 1c, plus vacht-kleurvergelijking met Game Freak."""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); L = os.path.abspath(os.path.join(HERE, '../../..'))
ROOT = os.path.abspath(os.path.join(L, '../../../..'))
def fit(im, w, h, bg=(255, 255, 255)):
    im = im.convert('RGBA'); s = min(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    b = Image.new('RGBA', (w, h), bg + (255,)); b.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2)); return b
def spr(p, s, bg=(236, 236, 236)):
    im = Image.open(p).convert('RGBA').crop((0, 0, 64, 64)); b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(im)
    return b.resize((64 * s, 64 * s), Image.NEAREST)
def gf(n):
    d = os.path.join(ROOT, 'graphics/pokemon', n); p = os.path.join(d, 'anim_front_gba.png')
    return p if os.path.exists(p) else os.path.join(d, 'anim_front.png')
lijn = Image.open(os.path.join(L, 'ontwerp/lijn_ronde2.png')); f2 = lijn.crop((300, 40, 600, 390))
row1 = [('poppetje fase 2 (lijn_ronde2)', fit(f2, 256, 256)), ('onderlaag', fit(Image.open(os.path.join(L, 'fase2/silhouet/onderlaag_256.png')), 256, 256)),
        ('foto 1 (pose)', fit(Image.open(os.path.join(L, 'referenties/foto1_lama_driekwart_POSE.png')), 256, 256)),
        ('foto 3 (oorkwasten, aguayo)', fit(Image.open(os.path.join(L, 'referenties/foto3_kudde_oorkwasten_aguayo.webp')), 256, 256)),
        ('foto 4', fit(Image.open(os.path.join(L, 'referenties/foto4_bont_bruin_wit.webp')), 256, 256))]
row2 = [('alpaca (fase 1) 4x', spr(os.path.join(L, 'referenties/fase1_alpaca.png'), 4)), ('ronde 1c 4x', spr(os.path.join(L, 'fase2/kleur/ronde1c/lama.png'), 4))]
row3 = [(n + ' 3x', spr(gf(n), 3)) for n in ['stantler', 'eevee', 'ponyta', 'furret', 'girafarig']] + [('lama 1c 3x', spr(os.path.join(L, 'fase2/kleur/ronde1c/lama.png'), 3))]
W = 5 * 268 + 12; img = Image.new('RGBA', (W, 24 + 256 + 30 + 256 + 30 + 192 + 90), (255, 255, 255, 255)); d = ImageDraw.Draw(img)
y = 18
for i, (t, im) in enumerate(row1): img.paste(im, (12 + i * 268, y)); d.text((12 + i * 268, y - 14), t, fill=(0, 0, 0))
y += 256 + 30
for i, (t, im) in enumerate(row2): img.paste(im, (12 + i * 268, y)); d.text((12 + i * 268, y - 14), t, fill=(0, 0, 0))
# opmerkingen naast ronde 1c
notes = ['DIAGNOSE (zie DIAGNOSE.md):', 'kop: smalle wig met puntsnuit = hert/paard;', '  geen ronde schedel, geen splitlip-snuit', 'oren: rechte sprieten = hert/geit;', '  lama: banaanoren, punten naar binnen',
         'hals: gladde buis even breed als de kop;', '  lama: dikke wolhals, kop steekt eruit', 'lijf: wol alleen in de omtrek, vacht dof', 'poten: verre voorpoot = recht paaltje (x30-34)',
         '  knikjes van 1 px; geen wolbroek/-mouw', 'staart: klein knopje', 'kleur: 5 bruintinten, 23% schaduw + 16% donker', '  + 14% omlijning; licht maar 6% (GF 20-30%)']
for i, t in enumerate(notes): d.text((12 + 2 * 268 + 10, y + i * 18), t, fill=(150, 0, 0) if i == 0 else (0, 0, 0))
y += 256 + 30
for i, (t, im) in enumerate(row3): img.paste(im, (12 + i * 200, y)); d.text((12 + i * 200, y - 14), t, fill=(0, 0, 0))
y += 192 + 12
def ramp(x, y, t, cols):
    d.text((x, y), t, fill=(0, 0, 0))
    for i, c in enumerate(cols): d.rectangle([x + i * 30, y + 14, x + i * 30 + 28, y + 40], fill=tuple(int(c[j:j + 2], 16) for j in (0, 2, 4)))
ramp(12, y, 'Stantler vacht', ['ffffac', 'ffd573', 'e6b45a', 'b48331', '7b4100'])
ramp(200, y, 'Eevee vacht + kraag', ['e6b473', 'c59452', 'a47b31', '625229', 'eee6c5', 'ded5a4'])
ramp(420, y, 'lama 1c vacht', ['e2b47c', 'c88e55', 'a86a3a', '74401f', '2a161a'])
ramp(600, y, 'VOORSTEL ronde 2 (h, l, b, s, d)', ['f8e2a8', 'efc27a', 'd69a52', 'a8683a', '6c3a20'])
ramp(800, y, 'VOORSTEL wolpunt/borst (optie)', ['fbefcf', 'ead1a0'])
img.save(os.path.join(HERE, 'diagnose.png')); print(img.size)
