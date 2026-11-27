# kale reductie: comp_nat + mat_nat -> 64x64 materiaal + kleur (paletindex), lijn wint bij kfrac>=TH
import numpy as np
from reduceer import X0,Y0,s,LEFT,TOP
PAL=[(152,208,160),(16,14,12),
 (178,166,96),(228,216,138),(244,236,172),     # 2-4 stekel
 (90,71,62),(116,95,78),(140,118,100),         # 5-7 schild bruin
 (180,154,114),(222,204,170),                  # 8-9 (8 warmer: staartzand r3_3 (178,148,111)) beige (band, rand, strepen, staart)
 (46,46,48),(66,66,66),(100,100,96),(128,126,120),  # 10-13 grijs
 (208,112,60),(240,166,104)]                     # 14-15 oog
RAMP={'S':[2,3,4],'B':[5,6,7,8,9],'E':[5,6,7,8,9],'T':[1,5,6,8,9],'G':[10,11,12,13],'O':[14,15]}
def basis(TH=0.33,AL=0.45):
    nat=np.load('comp_nat.npy').astype(float); M=np.load('mat_nat.npy')
    I=np.zeros((64,64),int); MAT=np.full((64,64),'.'); INFO={}
    for sy in range(64):
        for sx in range(64):
            ya=Y0+(sy-TOP)*s; xa=X0+(sx-LEFT)*s; tot=0; w_m={}; c_m={}
            for y in range(int(np.floor(ya)),int(np.ceil(ya+s))):
                for x in range(int(np.floor(xa)),int(np.ceil(xa+s))):
                    w=max(0,min(y+1,ya+s)-max(y,ya))*max(0,min(x+1,xa+s)-max(x,xa))
                    if w<=0: continue
                    tot+=w
                    if not(0<=y<100 and 0<=x<100): continue
                    m=M[y,x]
                    if m=='.': continue
                    w_m[m]=w_m.get(m,0)+w; c_m[m]=c_m.get(m,0)+w*nat[y,x]
            a=sum(w_m.values())/tot
            INFO[(sy,sx)]=(a,{k:v/tot for k,v in w_m.items()})
            if a<AL: continue
            if w_m.get('K',0)/tot>=TH: I[sy,sx]=1; MAT[sy,sx]='K'; continue
            if w_m.get('O',0)>0: m='O'
            else: m=max((k for k in w_m if k!='K'),key=lambda k:w_m[k],default='K')
            if m=='K': I[sy,sx]=1; MAT[sy,sx]='K'; continue
            c=c_m[m]/w_m[m]
            # schild: bruin en beige samen gemiddeld (B+E) zodat de strepen hun eigen tint houden
            if m in 'BE':
                ww=w_m.get('B',0)+w_m.get('E',0); c=(c_m.get('B',0)+c_m.get('E',0))/ww
                m='E' if w_m.get('E',0)>w_m.get('B',0) else 'B'
            r=RAMP[m]; I[sy,sx]=r[int(np.argmin([((np.array(PAL[i])-c)**2).sum() for i in r]))]; MAT[sy,sx]=m
    return I,MAT,INFO
def png(I,f,z=1):
    from PIL import Image
    im=Image.fromarray(I.astype('uint8'),'P'); im.putpalette(sum(PAL,())+(0,)*(768-3*len(PAL)))
    if z>1: im=im.resize((64*z,64*z),Image.NEAREST)
    im.save(f,transparency=0)
if __name__=='__main__':
    import sys
    I,MAT,INFO=basis(float(sys.argv[1]) if len(sys.argv)>1 else 0.33)
    np.save('kaal_I.npy',I); np.save('kaal_MAT.npy',MAT); png(I,'kaal.png'); png(I,'kaal_8x.png',8)
