# r14 = r13 met alleen een nieuwe stekel (png rij 57..63); rij 0..56 diff 0.
# Vormen per rij (png x van..tot, inclusief omlijning). Belichting: rij 57 = schaduw direct onder het lijf (licht->donker naar rechts);
# daaronder voorvlak links licht (smal uitlopend naar een heldere tip), ribbe van onder de lijfribbe (png x35) schuin naar de tip,
# zijvlak rechts donker; omlijning: selout links (6), zwart rechts/onder (9).
import sys; sys.path.insert(0,'gereedschap'); from r4lib import op, rgba
import numpy as np; from PIL import Image
src=np.array(Image.open('sprite_r13/baltoy_r13.png')); PAL=Image.open('sprite_r13/baltoy_r13.png').getpalette()
VORM={
 'A':{57:(29,36),58:(29,36),59:(30,35),60:(31,34),61:(32,33)},                       # model: breed, kort, kegel (geen hals)
 'B':{57:(29,36),58:(29,36),59:(30,35),60:(30,35),61:(31,34),62:(31,34),63:(32,33)}, # zuivere spits, 2:1 symmetrisch
 'C':{57:(31,34),58:(30,35),59:(29,36),60:(30,35),61:(31,34),62:(32,33)},            # kleine ruit
}
def stekel(k):
    a=src.copy(); a[57:64,:]=0
    rows=VORM[k]; top=min(rows); tip=max(rows); last=tip-1      # laatste rij = alleen omlijning (zwart)
    for y,(x0,x1) in rows.items():
        # ribbe: van png x35 (onder de lijfribbe) naar het midden van de tip
        rib=round(35+(32.5-35)*(y-top)/max(1,tip-top))
        for x in range(x0,x1+1):
            if y==tip: v=9
            elif x==x1: v=9
            elif x==x0: v=9 if y==top else 6                     # selout links (lichtkant)
            elif y==top: v=[6,7,7,8][min(3,int((x-x0-1)/max(1,(x1-x0-1))*4))]   # schaduw onder het lijf
            elif x>rib: v=6 if x>rib+1 else 5                    # zijvlak
            elif x==rib: v=4                                      # ribbe
            else: v=1 if y==last else (3 if x==rib-1 else 2)     # voorvlak, tip helder
            a[y,x]=v+1
    return a
if __name__=='__main__':
    for k in 'ABC':
        a=stekel(k); p=f'sprite_r14/baltoy_r14{k}.png'; im=Image.fromarray(a,'P'); im.putpalette(PAL); im.save(p,transparency=0)
        op(rgba(Image.open(p)),(255,255,255,255),8).save(f'sprite_r14/baltoy_r14{k}_8x.png')
        m=a!=src; print(k,'gewijzigd',int(m.sum()),'boven rij 57:',int(m[:57].sum()))
        for y in range(55,64): print('  ',y,''.join('.' if v==0 else ('%x'%(v-1) if v<11 else 'R') for v in a[y,24:42]))
