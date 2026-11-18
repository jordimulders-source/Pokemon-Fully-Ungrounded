# Pitahaya-draak fase 3, r13 (maker). Basis = ../sprite_r12/pitahaya3_r12.png. Alleen de 5 pixels van Jordi
# (8,30) (9,30) (10,30) (8,31) (9,31) en directe buren in de bek. Jordi: "check bij de 5 pixels die ik gelijnd heb of de
# schaduwkleur nog klopt". Model gemeten (mediaan per spritepixel): y29 x8-10 wit (±250); y30 x8-10 donkerroze tandvlees
# (154,55,91)/(154,95,117)/(131,49,77); ondertanden y31: x8 (107,90,93) donker, x9 (179,174,178) lichtgrijs; hoektand (6,31) (146,138,143).
# Gebruik: python3 maak_r13.py
import numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B0 = Image.open('../sprite_r12/pitahaya3_r12.png'); R = np.asarray(B0).astype(int); pal = B0.getpalette()
V = {
 # F: vlees wit tot onderaan, alleen achterin (rechts) schaduw; tandvlees d als korte scheiding op y31, tanden 1 px lager in de lip.
 'F': [(8,30,'w','W'), (9,30,'w','W'), (8,31,'W','d'), (9,31,'W','d'), (8,32,'r','W'), (9,32,'r','w')],
 # G: vlees wit, achterin w; ondertanden in de schaduw van de bovenkaak (model: grijs, links donkerder): (8,31) w, (9,31) q.
 'G': [(8,30,'w','W'), (9,30,'w','W'), (8,31,'W','w'), (9,31,'W','q')],
 # H: vlees vooraan wit, schaduw groeit naar achteren (x9-10 w); ondertanden lichtgrijs w (model ±179), lichter dan q, donkerder dan vlees.
 'H': [(8,30,'w','W'), (8,31,'W','w'), (9,31,'W','w')],
}
for n, px in V.items():
    o = R.copy(); log = []
    for x, y, oud, nw in px:
        assert CH[o[y, x]] == oud, (n, x, y, CH[o[y, x]]); o[y, x] = CH.index(nw); log.append('%s | %d | %d | %s -> %s' % (n, x, y, oud, nw))
    assert ((o > 0) == (R > 0)).all()
    assert all(26 <= y <= 32 and 7 <= x <= 10 for y, x in np.argwhere(o != R))
    im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save('pitahaya3_r13_%s.png' % n, transparency=0)
    with open('pitahaya3_r13_afwijkingen.txt', 'a' if n != 'F' else 'w') as f:
        f.write('# pitahaya3_r13_%s.png t.o.v. r12: %d px\n%s\n\n' % (n, len(log), '\n'.join(log)))
    print(n, len(log))
