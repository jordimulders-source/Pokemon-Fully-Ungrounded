# vel.png: lama 8x | model (r4 + poten r12, handschoenen r3 erop) op dezelfde schaal 8x | oude sprite 8x
#          | 1x op licht en donker | close-ups kop en poten 12x naast het model
import os, sys, subprocess; from PIL import Image, ImageDraw
HIER = os.path.dirname(os.path.abspath(__file__)); R1D = os.path.dirname(HIER); FASE2 = os.path.dirname(os.path.dirname(R1D))
sys.path.insert(0, HIER); from reduceer import S, X0, Y0, COLS
def rgba(p):
    im = Image.open(p)
    if im.mode == 'P': im.save('/tmp/_v.png', transparency=0); im = Image.open('/tmp/_v.png')
    return im.convert('RGBA')
def op(im, bg=(255, 255, 255)):
    b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im); return b.convert('RGB')
lama = rgba(os.path.join(R1D, 'lama.png')); oud = rgba(os.path.join(FASE2, 'af/lama.png'))
ox = (64 - COLS) // 2; xl = X0 - ox * S; yt = Y0 - 1 * S
_src = Image.open(os.path.join(FASE2, 'gemini/poten/r4_poten_r12.png')).convert('RGB'); _w = Image.new('RGB', (1400, 1400), (255, 255, 255)); _w.paste(_src, (200, 200)); xl += 200; yt += 200
mdl = _w.crop((int(xl), int(yt), int(xl + 64 * S), int(yt + 64 * S))).resize((512, 512), Image.LANCZOS)
pan = [op(lama.resize((512, 512), Image.NEAREST)), mdl, op(oud.resize((512, 512), Image.NEAREST))]
W = Image.new('RGB', (3 * 512 + 4 * 10 + 2 * 64 + 10, 512 + 20 + 330), (235, 235, 235))
for k, p in enumerate(pan): W.paste(p, (10 + k * 522, 10))
W.paste(op(lama, (248, 248, 240)), (10 + 3 * 522, 10)); W.paste(op(lama, (40, 44, 56)), (10 + 3 * 522, 84))
W.paste(op(oud, (248, 248, 240)), (10 + 3 * 522 + 70, 10)); W.paste(op(oud, (40, 44, 56)), (10 + 3 * 522 + 70, 84))
d = ImageDraw.Draw(W)
for k, t in enumerate(('r1 (8x)', 'model r4 + poten r12, zelfde schaal (handschoenen: r3)', 'oude Llamauler (af/)')): d.text((14 + k * 522, 12), t, fill=(0, 0, 0))
d.text((14 + 3 * 522, 160), '1x: r1 | oud', fill=(0, 0, 0))
y = 532
for naam, box in (('kop', (9, 0, 29, 22)), ('poten', (10, 48, 56, 63))):
    subprocess.run(['python3', os.path.join(HIER, 'closeup.py'), os.path.join(R1D, 'lama.png'), '/tmp/_cl.png'] + [str(v) for v in box], env=dict(os.environ, Z='12'), check=True)
    c = Image.open('/tmp/_cl.png'); W.paste(c, (10, y) if naam == 'kop' else (10 + c.width + 20 if False else 530, y)); 
W.save(os.path.join(R1D, 'vel.png')); print('vel', W.size)
