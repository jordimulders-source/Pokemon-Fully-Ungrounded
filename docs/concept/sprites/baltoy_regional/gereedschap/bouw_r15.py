# r15 = r13 met alleen een nieuwe stekel (png rij 57..63; rij 0..56 diff 0), overgenomen uit het model (gereedschap/natief.png,
# natief rij 72..82, x 43..57). Schaal 2x: sprite-x = 35 + (natief-x - 55)/2 (natief lijfribbe x55 = sprite-ribbe x35).
# Lagen: natief 72 hals -> rij 57; 73 bovenvlak -> 58; 74/75 rand (onderste helft, rij 75) -> 59; kegel 76/77 -> 60, 78/79 -> 61, 80/81 -> 62; tip 82 -> 63.
# Tinten: model 175 -> 2, 140 -> 4, 133 -> 5, 97 -> 7, rand links 64/68 -> 8, omlijning -> 9 (zelfde verhouding als lijf model -> sprite).
import sys; sys.path.insert(0,'gereedschap'); from r4lib import op, rgba
import numpy as np; from PIL import Image
src=np.array(Image.open('sprite_r13/baltoy_r13.png')); PAL=Image.open('sprite_r13/baltoy_r13.png').getpalette()
K=9
STEKEL={  # rij: {x: tint}
 57:{30:K,31:7,32:7,33:7,34:7,35:K},                          # hals          (model rij 72: K 98 97 99 97 K, x45..55)
 58:{30:K,31:7,32:7,33:7,34:7,35:7,36:K},                     # bovenvlak     (model rij 73: K 97..97 K, x44..56; rechts 1 breder dan de hals)
 59:{29:8,30:2,31:4,32:4,33:4,34:6,35:5,36:K},                # rand, breedst, links verder uit (model rij 75: 68 173 140.. 97 133.. K, x43..57)
 60:{30:K,31:2,32:2,33:2,34:5,35:5,36:K},                     # kegel         (model 76/77: K 172.. 137 133.. K)
 61:{31:K,32:2,33:3,34:5,35:K},                               #               (model 78/79: K 175.. 136 132 K)
 62:{32:K,33:3,34:K},                                         #               (model 80/81: K 174/137 134 K)
 63:{33:K,34:K},                                              # platte tip    (model 82: K K K, x50..52)
}
def bouw():
    a=src.copy(); a[57:64,:]=0
    for y,r in STEKEL.items():
        for x,v in r.items(): a[y,x]=v+1
    return a
if __name__=='__main__':
    a=bouw(); p='sprite_r15/baltoy_r15.png'; im=Image.fromarray(a,'P'); im.putpalette(PAL); im.save(p,transparency=0)
    op(rgba(Image.open(p)),(255,255,255,255),8).save('sprite_r15/baltoy_r15_8x.png')
    m=a!=src; print('gewijzigd',int(m.sum()),'boven rij 57:',int(m[:57].sum()),'transparant/zwart boven 57 gelijk:',bool((a[:57]==src[:57]).all()))
    for y in range(54,64): print('  ',y,''.join('.' if v==0 else ('%x'%(v-1) if v<11 else 'R') for v in a[y,24:42]))
