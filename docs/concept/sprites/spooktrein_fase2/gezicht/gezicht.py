# Gezicht spooktrein fase 2 (Jordi 16 nov): mond "groot en rond", tong zoals in het model (index 5), geen tanden;
# ogen "zoals de geest links in het rood" (alleen de vorm: brede gebogen boogjes), groot mag.
# Oude ogen en mond worden eerst geesttint; daarna mond (omlijning-kleur binnen, zoals model) en ogen (omlijning).
import sys
from PIL import Image
src, uit, variant = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src); px = im.load()
# oude ogen + mond wissen (zone x25-43, y12-22) -> lichtste geesttint van de rij eromheen
for y in range(10, 24):
    for x in range(25, 44):
        if px[x, y] in (1, 5):
            buren = [px[xx, y] for xx in list(range(x - 4, x)) + list(range(x + 1, x + 5)) if px[xx, y] in (2, 3, 4)]
            px[x, y] = max(set(buren), key=buren.count) if buren else 2
MONDEN = {  # rijbreedtes van boven naar beneden; tongrijen (vanaf boven, breedte)
 'A': (15, [5, 9, 11, 13, 13, 13, 13, 13, 11, 9, 5], {6: 5, 7: 7, 8: 7, 9: 5}),
 'B': (15, [7, 11, 13, 15, 15, 15, 15, 15, 13, 11, 7], {6: 5, 7: 9, 8: 9, 9: 7}),
 'B2': (14, [7, 11, 13, 15, 17, 17, 17, 17, 15, 13, 11, 7], {7: 7, 8: 11, 9: 11, 10: 9}),
 'B3': (14, [9, 13, 15, 17, 17, 19, 19, 19, 17, 17, 15, 13], {7: 9, 8: 13, 9: 13, 10: 11}),
 'C': (14, [5, 9, 11, 11, 13, 13, 13, 13, 13, 11, 11, 9, 5], {8: 5, 9: 7, 10: 7, 11: 5}),
}
y0, rijen, tong = MONDEN[variant]
cx = 34
for i, w in enumerate(rijen):
    for x in range(cx - w // 2, cx + w // 2 + 1):
        if px[x, y0 + i] not in range(7, 14): px[x, y0 + i] = 1  # wagon staat ervoor
for i, w in tong.items():
    for x in range(cx - w // 2, cx + w // 2 + 1):
        if px[x, y0 + i] not in range(7, 14): px[x, y0 + i] = 5
OOG = ['..11..', '.1111.', '11..11', '1....1'] if len(sys.argv) > 4 else ['.1111.', '11..11', '1....1']
oy = y0 - len(OOG) - 1
for ox in (26, 37):
    for j, r in enumerate(OOG):
        for i, c in enumerate(r):
            if c == '1': px[ox + i, oy + j] = 1
im.save(uit, transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save(uit.replace('.png', '_8x.png'))
