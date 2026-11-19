# poten.py: poten met de hand op het raster (vorm uit het model, legs.png): schenen 3 tinten (licht links), tenen met
# lichte bovenrij en donkere onderrij, zwarte klauwpunten; verre poot (links) een stap donkerder (E/2), nabije F/E/2.
# Omlijning: 2 aan de lichtkant (boven/links), 1 aan de schaduwkant. Leest kuif.npy, schrijft poten.npy + hoatzin.png
import numpy as np
H = '0123456789ABCDEF'
VER = (14, [  # x vanaf 14, y vanaf 49
 "..........1EE21...",   # 49
 "..........1EE21...",   # 50
 ".........1EE21....",   # 51
 ".........1EE21....",   # 52
 ".........1EE21....",   # 53
 "........1EEE21....",   # 54
 "...222222EEEE21...",   # 55
 "..2EEEEEEEEEEEE1..",   # 56
 ".11222222E2222211.",   # 57
 ".1 111111E211111 1",   # 58
 "........1E21......",   # 59
 "........111.......",   # 60
])
NAB = (27, [  # x vanaf 27, y vanaf 49
 "....1FE21...",   # 49
 "....1FE21...",   # 50
 "....1FE21...",   # 51
 "....1FE21...",   # 52
 "....1FE21...",   # 53
 "....1FE21...",   # 54
 "..22FFEE21..",   # 55
 ".2FFFEEFE1..",   # 56
 "11E2FE21FE1.",   # 57
 ".111F21.121 ".replace(' ','.'),  # 58
 "...1F21...1.",   # 59
 "...1E21.....",   # 60
 "..1E21......",   # 61
 "..111.......",   # 62
 "...1........",   # 63
])
a = np.load('kuif.npy'); P = np.load('part.npy')
# oude poten weg (onderdelen poot_v/poot_n en hun ring) in het pootgebied
for y in range(49, 64):
    for x in range(13, 38):
        if y == 49 and not (24 <= x <= 36): continue
        if P[y, x] in (1,):   # staart blijft
            continue
        if y >= 50 or P[y, x] in (5, 6) or a[y, x] in (14, 15):
            a[y, x] = 0
for x0, rows in (VER, NAB):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '.': continue
            a[49+j, x0+i] = 0 if ch == ' ' else H.index(ch)
for y in range(44, 50):
    for x in range(13, 38):
        if a[y, x] in (14, 15) and not ((x0 := (14 if x < 27 else 27)) <= x and (VER if x < 27 else NAB)[1][y-49][x-x0] in 'EF' if y >= 49 else False):
            a[y, x] = 11
np.save('poten.npy', a)
if __name__ == '__main__':
    from PIL import Image; from geom import PAL
    im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
