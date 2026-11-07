"""r10: Swellows snavel (anim_front.png, eerste frame) letterlijk overzetten.
Knipt de snavelpixels (Swellows snaveltinten g/j/m/n en zwart f) uit x4-16, y11-19, zet ze met een vaste kleurtabel om naar ons palet
en verschuift ze naar onze snavelvoet: (x, y) -> (x + 8, y - 4). Schrijft snavel_swellow.txt (tekening-regels, rij kolom pixels).
Draaien: python3.11 swellow_snavel.py"""
from PIL import Image
im = Image.open('../../../../../../graphics/pokemon/swellow/anim_front.png')
pal = im.getpalette()
# Swellows snaveltinten (index in zijn palet) -> onze
TABEL = {(230, 180, 98): ('a', 'm, lichtste hoorn -> a crème licht'),
         (222, 164, 49): ('b', 'j, lichte hoorn -> b crème basis (lichte hoorn)'),
         (148, 90, 16): ('g', 'n, midden -> g grijs'),
         (82, 65, 32): ('G', 'g, donker/omlijning/mondlijn -> G donkergrijs (onze donkerste snaveltint)'),
         (16, 16, 16): ('k', 'f, zwart (schaduwkant ondersnavel) -> k zwart')}
DX, DY = 8, -4
def main():
    cel = {}
    for y in range(11, 20):
        for x in range(4, 17):
            i = im.getpixel((x, y)); rgb = tuple(pal[3 * i:3 * i + 3])
            if rgb in TABEL: cel[(x, y)] = TABEL[rgb][0]
    # zwart buiten de snavel (keelomlijning, oog) niet meenemen: alleen f die aan snaveltinten grenst links-onder
    cel = {p: c for p, c in cel.items() if not (c == 'k' and p[0] >= 10)}
    regels = []
    for y in sorted({p[1] for p in cel}):
        xs = sorted(x for x, yy in cel if yy == y)
        run = []
        for x in xs:
            if run and x != run[-1] + 1:
                regels.append(f'{y + DY} {run[0] + DX} ' + ''.join(cel[(xx, y)] for xx in run)); run = []
            run.append(x)
        regels.append(f'{y + DY} {run[0] + DX} ' + ''.join(cel[(xx, y)] for xx in run))
    with open('snavel_swellow.txt', 'w') as f:
        f.write('# Swellows snavel, letterlijk omgekleurd (swellow_snavel.py). Kleurtabel:\n')
        for rgb, (c, t) in TABEL.items(): f.write(f'#   {rgb} {t}\n')
        f.write('\n'.join(regels) + '\n')
    print(open('snavel_swellow.txt').read())

if __name__ == "__main__":
    main()
