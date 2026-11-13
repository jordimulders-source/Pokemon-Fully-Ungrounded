# met de hand: per-pixelreparaties op het scriptraster (rasterco's j,i van het 66x66-raster, fase 0,0).
# elke regel: j, i, nieuw, reden (gemeten in het model, natief x=2i..2i+1, y=2j..2j+1)
import sys
E = [
 # kop: bovenkant (creme stuk, lichte tint linksboven zoals het model)
 (12, 14, 'f', 'creme stuk, model hf/es'), (12, 16, 'b', 'blauw stuk, model ss/bb (voeg zit erboven)'),
 (13, 10, 'h', 'lichtste creme, model hh/hf'),
 # rood stukje op het voorhoofd (verdween in de reductie)
 (14, 8, 'p', 'rood stukje voorhoofd, model pR/ps'), (15, 7, 'p', 'idem, model pp/rs'),
 # oog: zwart 3x2 + onderpunt, glans grijs links (model y30-34, x28-33, glans x29 y31-32)
 (15, 14, 'g', 'oogglans'), (15, 17, 'c', 'lichtblauw rechts van het oog, model ss/cc'), (15, 18, 'c', 'idem, model ss/cc'), (15, 15, 'k', 'oog'), (15, 16, 'k', 'oog'),
 (16, 13, 'c', 'blauw naast het oog, model cs/rs'), (16, 14, 'k', 'oog'), (16, 15, 'k', 'oog'), (16, 16, 'k', 'oog'),
 (17, 15, 'q', 'onder het oog: voeg (model ##/ss), los van het zwarte stuk eronder'), (17, 14, 'R', 'rood stuk onder het oog, model r#/Rr'),
 (16, 10, 'b', 'blauw, model bb/br'), (16, 11, 'b', 'blauw, model bb/rr'), (16, 12, 'b', 'blauw, model bs/rr'),
 # blauw snuitstuk tot aan het oog (de modelvoeg op y30 is een halve spritepixel; als hele rij donkerblauw slokte hij het oog op)
 (15, 8, 'c', 'model rs/cw'), (15, 9, 'c', 'model ss/cc'), (15, 10, 'c', 'model ss/cb'), (15, 11, 'b', 'model ss/ba'), (15, 12, 'b', 'model ab/sc'),
 (16, 18, 'c', 'blauw, model cc/cs'), (16, 20, 'h', 'creme stuk, model hs/hh'), (16, 21, 'R', 'rood, model RR/es'),
 (18, 19, 'f', 'creme stuk, model hh/sh'),
 # snuitpunt rood, lichte tint zoals het model
 (18, 5, 'p', 'snuitpunt, model p#/pp'), (19, 5, 'p', 'snuitpunt, model pp/pR'),
 # bovenkaak: lippenlijn y41-42 zwart, tanden eronder (model: hoektand links x11-13 y43-48, rechts x20-23 y44-48)
 (21, 7, 'w', 'basis linker hoektand, model cw/ww'), (21, 8, 'k', 'lippenlijn, model c#/ww'), (21, 9, 'k', 'lippenlijn'),
 (21, 10, 'k', 'lippenlijn, model ##/ww'), (21, 11, 'k', 'lippenlijn, model #s/c#'),
 (22, 6, 'w', 'linker hoektand, model cb/wb'), (22, 10, 'w', 'rechter hoektand, model ww/ww'), (22, 11, 'w', 'rechter hoektand, model wc/wc'),
 (23, 10, 'w', 'rechter hoektand, model ew/#c'), (23, 11, 'w', 'rechter hoektand, model wc/wc'),
 (24, 10, 'r', 'muil, model r#/rr'), (24, 11, 'c', 'punt rechter hoektand, model cc/##'),
 # onderkaak: twee tandjes + witte rand ertussen (U), model x17/x24 y56-59, wit y59-60
 (28, 9, 'w', 'linker ondertand (1 px naar rechts: x16 is omlijning)'), (28, 11, 'p', 'tong licht, model ps/ps'),
 (29, 8, 'k', 'omlijning onderkaak'), (29, 9, 'w', 'linker ondertand'), (29, 10, 'c', 'binnenkant tandenrij, model ##/cc'),
 (29, 11, 'c', 'binnenkant tandenrij, model ss/cs'),
 (27, 11, 'p', 'lichtere tong, model pp/pp'),
 # neus: zwart stuk met grijze glans linksboven (model x12-14 y34-35)
 (17, 6, 'g', 'glans op de neus'),
 # staartpunt: zwart stuk met grijsblauwe ribbels (model lum 80-110, verdwenen want als voeg gelezen)
 (16, 48, 'g', 'ribbel staartpunt'), (15, 49, 'g', 'ribbel'), (14, 50, 'g', 'ribbel (was blauw)'),
 (15, 51, 'g', 'ribbel (was voeg)'), (15, 52, 'g', 'ribbel (was blauw)'), (14, 53, 'g', 'ribbel'),
 (13, 52, 'g', 'ribbel'), (13, 54, 'g', 'ribbel'), (14, 54, 'g', 'ribbel'),
 # voorpoot: lichtste blauw was als creme/wit gelezen; tenen gescheiden door voegen op x31 en x39-40 (model)
 (53, 15, 'c', 'poot licht, model ac/ww'), (53, 16, 'c', 'model cc/cc'), (53, 17, 'c', 'model cc/sb'),
 (54, 14, 'c', 'poot licht, model ww/ww'), (54, 15, 'c', 'model wc/cc'), (54, 16, 'c', 'model ca/ac'), (54, 17, 'c', 'model cc/hc'),
 (54, 20, 'd', 'teenvoeg, model cc/sc'), (54, 22, 'b', 'model bb/cb'), (54, 23, 'b', 'model bf/bs'),
 (55, 14, 'c', 'model cw/cc'), (55, 15, 'd', 'teenvoeg x31'), (55, 16, 'c', 'model ch/cc'), (55, 17, 'c', 'model hc/hc (was creme)'),
 (55, 18, 'c', 'model cc/cc'), (55, 19, 'd', 'teenvoeg x39'), (55, 20, 'c', 'model ch/hh (was creme)'), (55, 21, 'c', 'model hc/cc'),
 (56, 15, 'd', 'teenvoeg x31'), (56, 16, 'b', 'model cc/bb'), (56, 17, 'b', ''), (56, 18, 'b', ''), (56, 19, 'd', 'teenvoeg x40'),
 (56, 20, 'b', 'model cc/bb'), (56, 21, 'b', ''),
 (57, 15, 'd', 'teenvoeg x31'), (57, 19, 'd', 'teenvoeg x40'),
 # achterpoot (dichtbij): teenlijnen uit het model (x107, x112)
 (51, 53, 'q', 'teenlijn, model r#/r#'), (51, 56, 'q', 'teenlijn, model sR/#r'), (52, 56, 'q', 'teenlijn, model #r/##'),
 (30, 9, 'c', 'tandenrij, model cc/##'), (30, 10, 'w', 'witte rand, model ww/##'), (30, 11, 'w', 'witte rand, model ww/##'),
]
if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    rows = [list(l.rstrip('\n')) for l in open(src)]
    for j, i, c, why in E:
        rows[j][i] = c
    open(dst, 'w').write(''.join(''.join(r) + '\n' for r in rows))
    print(len(E), 'handwijzigingen')
