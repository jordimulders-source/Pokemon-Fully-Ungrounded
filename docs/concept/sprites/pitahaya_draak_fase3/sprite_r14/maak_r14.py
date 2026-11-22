# Pitahaya-draak fase 3, r14: eindkeuring op r13_G (FAIL klein), precies 7 px. Basis ../sprite_r13/pitahaya3_r13_G.png.
import numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B0 = Image.open('../sprite_r13/pitahaya3_r13_G.png'); R = np.asarray(B0).astype(int); pal = B0.getpalette()
P = [(11,29,'W','w','1 schaduw achterin de bek'),
     (58,45,'g','G','2 banding staartlus'), (58,46,'g','G','2 banding staartlus'), (58,47,'g','G','2 banding staartlus'),
     (23,59,'d','r','3 knots: rechtsonder donkerst, niet links'),
     (15,51,'h','H','4 rafel lichtkant'), (16,51,'h','H','4 rafel lichtkant')]
o = R.copy(); log = []
for x, y, oud, nw, w in P:
    assert CH[o[y, x]] == oud, (x, y, CH[o[y, x]]); o[y, x] = CH.index(nw); log.append('%s | %d | %d | %s -> %s' % (w, x, y, oud, nw))
assert (o != R).sum() == 7 and ((o > 0) == (R > 0)).all() and len(set(o.flatten())) <= 16
im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save('pitahaya3_r14.png', transparency=0)
open('pitahaya3_r14_afwijkingen.txt', 'w').write('# pitahaya3_r14.png t.o.v. ../sprite_r13/pitahaya3_r13_G.png: 7 px (tekens %s)\n%s\n' % (CH, '\n'.join(log)))
print('ok', (o != R).sum())
