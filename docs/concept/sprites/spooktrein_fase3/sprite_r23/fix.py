# r24 = r23 + keurfix (16 nov). Coördinaten (y,x).
# 1. Jordi: "alleen de rechtse < moet iets kleiner" / "3 pixels ipv 5": variant A = (y50,x22),(51,21),(52,22) blijven;
#    (49,23) -> A (plaatrij), (53,23) -> C (plaatrij). Variant B (naar rechts, 7 px) alleen op het vel.
# 2. Dubbele/driedubbele zwarte rechterrand (x24+x25(+x26) y47-54): één rand op x25 (zoals r20), x24 plaat,
#    hoekige rechteronderhoek (54,25),(55,25) zwart; bovenhoek een schuin stapje (47,27)-(48,26)-(49,25).
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r23/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette()
r20=np.array(Image.open(D+'sprite_r20/sprite.png')).astype(int)
def bouw(variant):
    a=r.copy()
    def zet(l,v):
        for p in l: a[p]=v
    if variant=='A':
        zet([(49,23)],10); zet([(53,23)],12)
    else:
        zet([(49,23)],10); zet([(53,23)],12); zet([(50,22),(51,21)],11); zet([(52,22)],12)
        zet([(50,23),(51,22),(52,23)],1)
    # rechterrand
    zet([(47,24),(47,25)],7); zet([(47,26),(48,24)],11); zet([(48,25)],11); zet([(49,24)],10)
    zet([(y,24) for y in range(50,55)],12); zet([(54,25),(55,25)],1)
    return a
A=bouw('A'); B=bouw('B')
KV=np.zeros((64,64),bool); KV[44:61,0:31]=True
for a in (A,B):
    assert (a[~KV]==r[~KV]).all() and (a[~KV]==r20[~KV]).all(),'buiten zone gewijzigd'
    assert set(np.unique(a))<=set(np.unique(r)),'nieuwe index'
assert (A!=r).sum()<=15, (A!=r).sum()
if __name__=='__main__':
    print('A gewijzigd',int((A!=r).sum()),'B',int((B!=r).sum()))
    print('    '+' '.join('%2d'%x for x in range(30)))
    for y in range(43,59): print('%2d  '%y+' '.join(' .' if q==0 else '%2X'%q for q in A[y,:30]))
    def save(a,p):
        o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal); o.save(p,transparency=0); return o
    o=save(A,D+'sprite_r24/sprite.png'); o.resize((512,512),Image.NEAREST).save(D+'sprite_r24/sprite_8x.png',transparency=0)
    save(B,D+'sprite_r24/variant_B.png')
