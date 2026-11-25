# bouw.py ronde 14 = eindkeuring Dragonfly Cave op sprite_r13 (rapport: eindkeuring_r13/rapport.md).
# Jordi 24 nov: "top, stuur maar naar de eindkeuring, let op lijnen, schaduwconsistentie, kleurtinten. Ook dat de bollen
# om het hoofd heen goed gelijnd zijn. Verder onder de staart een paar onnodige pixels".
# Alleen lijnpixels en tinten; silhouet alleen gewijzigd in zone A (onder de staart). Palet ongewijzigd.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r14/bouw.py
import numpy as np
from PIL import Image, ImageDraw

ch = '.KbcdfSCeLMogWwD'          # 0 transparant, 1 K zwart, 2 b, 3 c, 4 d, 5 f (bruin), 6 S, 7 C, 10 M, 15 D (creme), 8 e, 9 L (donker), 11 o, 12 g (oranje), 13 W, 14 w
I = {c: i for i, c in enumerate(ch)}
im13 = Image.open('sprite_r13/sprite.png'); PAL = np.array(im13.getpalette()[:48]).reshape(16, 3).astype('uint8')
r13 = np.asarray(im13).astype(int); o = r13.copy()

# (x, y): (verwacht in r13, nieuw)
ZONES = {
 'A staartonderkant (punt 4)': {
    (54, 49): ('K', '.'),    # zwevende zwarte pixel
    (53, 50): ('K', '.'),    # nopje in de heuplijn (niet in het model)
    (52, 50): ('c', 'K'),    #   -> heuplijn sluit weer op x52
    (52, 46): ('g', 'K'), (53, 46): ('g', 'K'),   # staartstompje onder de staart -> onderlijn van de staart
    (52, 47): ('g', '.'), (53, 47): ('K', '.'),   # stompje weg
 },
 'B helm en klep (lijnen)': {
    (34, 7):  ('b', 'K'),    # helmtop: K b K om en om -> zwart begint bij x33
    (20, 12): ('c', 'b'),    # kleppunt: dambord b/c, lichte tint op de buitenrand -> lijn
    (19, 13): ('c', 'b'),
    (35, 14): ('e', 'b'),    # onderlijn klep: log-tint/bijna zwart binnenin -> eigen donkerste bruin
    (38, 15): ('c', 'b'),    # onderlijn klep rechts: b c b -> doorlopend b
    (20, 15): ('e', 'b'),    # idem links (bijna zwart binnenin)
 },
 'C kraagbollen links': {
    (18, 17): ('c', 'b'), (18, 18): ('c', 'b'), (17, 21): ('c', 'b'), (17, 22): ('c', 'b'), (18, 23): ('c', 'b'),  # rand bol/hand: b c b c -> b
    (21, 21): ('D', 'e'),    # creme-lijntint naast de snuit -> snuitlijn (eigen donkerste e)
    (21, 22): ('D', 'd'),    # creme-lijntint in de bol -> bolvulling (snuitlijn ligt op x22)
 },
 'D kraagbollen onder': {
    (20, 29): ('K', 'b'), (21, 29): ('K', 'b'), (22, 29): ('K', 'b'),                       # binnenlijn niet zwart
    (24, 31): ('K', 'b'), (25, 32): ('K', 'b'), (26, 32): ('K', 'b'), (27, 32): ('K', 'b'), (28, 32): ('K', 'b'), (29, 31): ('K', 'b'),
    (31, 31): ('c', 'b'), (32, 32): ('d', 'b'), (33, 32): ('d', 'b'), (34, 32): ('d', 'b'), (35, 31): ('d', 'b'),  # bol onder rechts had geen onderlijn (model: lijn)
    (36, 30): ('d', 'b'),    # losse bruine pixel tussen lijn en bandje -> lijn naar het bandje (model: lijn)
    (35, 30): ('b', 'c'),    #   -> geen 2x2 lijnklont; schaduwrand van de bol
    (35, 32): ('d', 'b'),    #   -> anders losse bruine pixel onder de nieuwe onderlijn
 },
 'E kraagbollen rechts': {
    (39, 16): ('c', 'b'), (40, 17): ('c', 'b'), (40, 18): ('c', 'b'),   # naad bol rechtsboven (model-naad), sluit op (39,15) en (41,19)
    (40, 20): ('d', 'b'), (40, 21): ('d', 'b'), (39, 22): ('d', 'b'),   # naad tussen bol rechts-midden en bol rechts (sluit op (39,23))
    (39, 20): ('d', 'c'), (39, 21): ('d', 'c'), (38, 22): ('d', 'c'),   # schaduwsikkel rechts in die bol (licht linksboven)
    (40, 25): ('e', 'b'), (41, 25): ('e', 'b'),                         # onderlijn bol: log-tint -> eigen donkerste bruin
    (40, 26): ('b', 'c'),                                               # anders 3-px lijnklont
    (43, 22): ('K', 'c'), (42, 23): ('K', 'c'), (43, 24): ('K', 'c'),   # 2x2-zwartklont -> lijn 1 px: (44,22)(43,23)(42,24)
 },
 'F tuinbroek linkerrand': {
    (18, 42): ('D', 'b'), (18, 43): ('D', 'b'), (18, 44): ('D', 'b'),   # buitenlijn b b b b D D D b -> overal b (lijfpatroon, regel 4)
 },
 'G staart bovenrand': {
    (59, 21): ('g', 'K'),    # g K g K om en om -> zwart vanaf x58
 },
}

fout = []
for zone, px in ZONES.items():
    for (x, y), (oud, nieuw) in px.items():
        if r13[y, x] != I[oud]: fout.append((zone, x, y, ch[r13[y, x]], oud))
        o[y, x] = I[nieuw]
assert not fout, fout

def save(idx, pad, z=None):
    im = Image.new('P', (64, 64)); im.putpalette(PAL.ravel().tolist() + [0] * 3 * 240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad, transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64 * z, 64 * z), Image.NEAREST).save(pad.replace('.png', f'_{z}x.png'))
save(o, 'sprite_r14/sprite.png', 8)

# ---- bewijs: diff per zone, diff 0 erbuiten, silhouet alleen in zone A
alle = {p for px in ZONES.values() for p in px}
diff = {(int(x), int(y)) for y, x in np.argwhere(o != r13)}
for zone, px in ZONES.items(): print(f'{zone}: {sum(1 for p in px if p in diff)} px gewijzigd')
print('totaal gewijzigd:', len(diff), '| buiten de zones:', sorted(diff - alle))
sil = {(int(x), int(y)) for y, x in np.argwhere((o > 0) != (r13 > 0))}
print('silhouet gewijzigd:', sorted(sil), '| buiten zone A:', sorted(sil - set(ZONES['A staartonderkant (punt 4)'])))
assert not (diff - alle) and not (sil - set(ZONES['A staartonderkant (punt 4)']))
print('kleuren gebruikt:', len(set(np.unique(o)) - {0}), '+ transparant')

# ---- vel: r14 | r13 | model 8x ; kop 12x ; staartonderkant 12x ; Gen 3 ; 1x licht/donker
BG = (152, 208, 160)
def rgb(idx, bg=BG):
    t = Image.new('RGB', (64, 64), bg); t.paste(Image.fromarray(PAL[idx]), (0, 0), Image.fromarray(((idx > 0) * 255).astype('uint8'))); return t
def big(img, z, box=(0, 0, 64, 64)): return img.crop(box).resize(((box[2] - box[0]) * z, (box[3] - box[1]) * z), Image.NEAREST)
def mark(img, z, box, pts, kleur=(255, 0, 255)):
    d = ImageDraw.Draw(img)
    for (x, y) in pts:
        if box[0] <= x < box[2] and box[1] <= y < box[3]:
            X, Y = (x - box[0]) * z, (y - box[1]) * z; d.rectangle([X, Y, X + z - 1, Y + z - 1], outline=kleur, width=2)
    return img
model = Image.open('model/r10_k8_64.png').convert('RGB')
def gen3(n):
    g = Image.open(f'../../../../graphics/pokemon/{n}/anim_front.png'); a = np.asarray(g)[:64]
    P = np.array(g.getpalette()[:48]).reshape(16, 3).astype('uint8'); t = Image.new('RGB', (64, 64), BG)
    t.paste(Image.fromarray(P[a]), (0, 0), Image.fromarray(((a > 0) * 255).astype('uint8'))); return t
G3 = ['bibarel', 'linoone', 'ursaring', 'swampert', 'furret']

V = Image.new('RGB', (1580, 2330), 'white'); d = ImageDraw.Draw(V)
for i, (img, t) in enumerate([(rgb(o), 'r14 8x'), (rgb(r13), 'r13 8x'), (model, 'model (r10_k8, kale reductie) 8x')]):
    V.paste(big(img, 8), (10 + i * 522, 24)); d.text((10 + i * 522, 8), t, fill='black')
y0 = 560; kb = (14, 4, 48, 34)
for i, (img, t) in enumerate([(mark(big(rgb(o), 12, kb), 12, kb, diff), 'kop r14 12x (magenta = gewijzigd)'), (big(rgb(r13), 12, kb), 'kop r13 12x')]):
    V.paste(img, (10 + i * 418, y0 + 18)); d.text((10 + i * 418, y0), t, fill='black')
y0 += 18 + 360 + 14; sb = (44, 40, 60, 54)
for i, (img, t) in enumerate([(mark(big(rgb(o), 12, sb), 12, sb, diff), 'staartonderkant r14 12x'), (big(rgb(r13), 12, sb), 'staartonderkant r13 12x'), (big(model, 12, sb), 'model 12x')]):
    V.paste(img, (10 + i * 205, y0 + 18)); d.text((10 + i * 205, y0), t, fill='black')
y0 += 18 + 168 + 14
d.text((10, y0), 'naast echte Gen 3-sprites (4x): r14 | ' + ' | '.join(G3), fill='black')
for i, img in enumerate([rgb(o)] + [gen3(n) for n in G3]): V.paste(big(img, 4), (10 + i * 262, y0 + 18))
y0 += 18 + 256 + 14
d.text((10, y0), '1x licht / donker: r14, r13, ' + ', '.join(G3), fill='black')
for j, bg in enumerate([(248, 248, 248), (40, 40, 48)]):
    for i, img in enumerate([rgb(o, bg), rgb(r13, bg)] + [gen3(n) for n in G3]):
        if i >= 2:  # Gen 3 op dezelfde achtergrond
            g = Image.open(f'../../../../graphics/pokemon/{G3[i-2]}/anim_front.png'); a = np.asarray(g)[:64]
            P = np.array(g.getpalette()[:48]).reshape(16, 3).astype('uint8'); img = Image.new('RGB', (64, 64), bg)
            img.paste(Image.fromarray(P[a]), (0, 0), Image.fromarray(((a > 0) * 255).astype('uint8')))
        V.paste(img, (10 + i * 74, y0 + 18 + j * 72))
V.crop((0, 0, 1580, y0 + 18 + 150)).save('sprite_r14/vel.png')

# los vergelijkingsvel op 8x voor de keuring
W = Image.new('RGB', (6 * 520, 540), 'white'); dw = ImageDraw.Draw(W)
for i, (img, t) in enumerate([(rgb(o), 'r14')] + [(gen3(n), n) for n in G3]):
    W.paste(big(img, 8), (i * 520, 22)); dw.text((i * 520 + 4, 4), t, fill='black')
W.save('eindkeuring_r13/vergelijk_gen3_8x.png')
