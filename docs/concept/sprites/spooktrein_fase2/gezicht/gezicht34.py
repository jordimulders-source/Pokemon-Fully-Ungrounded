# Gezicht in 3/4 naar links (Jordi 16 nov: "het gezicht is nu te frontaal"): middelpunt naar links,
# rechterhelft van de mond (verre kant) ingekort, verre oog smaller en dichter bij het midden.
import sys
from PIL import Image
src, uit, variant, cx, fac = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
im = Image.open(src); px = im.load()
for y in range(10, 24):
    for x in range(23, 45):
        if px[x, y] in (1, 5):
            buren = [px[xx, y] for xx in list(range(x - 4, x)) + list(range(x + 1, x + 5)) if px[xx, y] in (2, 3, 4)]
            px[x, y] = max(set(buren), key=buren.count) if buren else 2
MONDEN = {
 'B2': (14, [7, 11, 13, 15, 17, 17, 17, 17, 15, 13, 11, 7], {7: 7, 8: 11, 9: 11, 10: 9}),
 'B3': (14, [9, 13, 15, 17, 17, 19, 19, 19, 17, 17, 15, 13], {7: 9, 8: 13, 9: 13, 10: 11}),
}
y0, rijen, tong = MONDEN[variant]
# Jordi: "de mond valt nu aan de linkerkant erbuiten": mond alleen binnen de geest, met 1 px geest eromheen
geest = {(x, y) for x in range(64) for y in range(64) if px[x, y] in (1, 2, 3, 4, 5) and y < 30}
binnen = {(x, y) for (x, y) in geest if px[x, y] != 1 or 14 <= y < 30 and 23 <= x <= 44} 
binnen = {(x, y) for (x, y) in geest if px[x, y] in (2, 3, 4)}
mag = {(x, y) for (x, y) in binnen if all((x + dx, y) in binnen or px[x + dx, y] in range(7, 14) for dx in (-1, 1))}
def zet(i, w, v):
    h = w // 2
    for x in range(cx - h, cx + round(h * fac) + 1):
        if (x, y0 + i) in mag: px[x, y0 + i] = v
for i, w in enumerate(rijen): zet(i, w, 1)
if "--tong" in sys.argv: [zet(i, w, 5) for i, w in tong.items()]  # Jordi 16 nov: "haal de tong maar weg"
OGEN = {
 'o2': (['.1111.', '111111', '11..11', '1....1'], ['.111.', '11111', '11.11', '1...1']),
 'o3': (['..11..', '.1111.', '111111', '11..11', '1....1'], ['..1..', '.111.', '11111', '11.11', '1...1']),
}
NABIJ, VER = OGEN[sys.argv[6]]
oy = y0 - len(NABIJ) - 1
ogen = [(cx - 8, NABIJ), (cx + 3, VER)]
for ox, oog in ogen:
    for j, r in enumerate(oog):
        for i, c in enumerate(r):
            if c == '1': px[ox + i, oy + j] = 1
im.save(uit, transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save(uit.replace('.png', '_8x.png'))
