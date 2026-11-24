# r5: (1) tinten onderkop + lijf naar het model (warmer/lichter), (2) krans-ogen . - . - . ^ . - . - .
# A (hoofd, claydol_g3r5.png): 2 nieuwe paletslots, alleen pixels in de zones krijgen ze (5->W1, 6->W2); rest diff 0.
# B (claydol_g3r5_paletB.png): alleen palet 5/6 globaal naar W1/W2 (pixels gelijk aan A-ogen), raakt de hele sprite.
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'r5'); sys.path.insert(0,'r4'); sys.path.insert(0,'r2')
import numpy as np
from PIL import Image
from zones import E,PAL,M,MAIN,ONDERKOP,LIJF,L,label
from ogen import ogen, STIP
PAL0=Image.open('eindkeuring/claydol_eind.png').getpalette()
W1=(149,135,113)   # model-mediaan middentoon onderkop (152,138,116) en lijf (146,131,109)
W2=(92,82,68)      # model schaduw onderkop (96,87,71) / lijnen lijf (82,72,61)
ZONE=ONDERKOP|LIJF
S,log=ogen(E)
OOG=S!=E
A=S.copy(); A[ZONE&(S==5)]=10; A[ZONE&(S==6)]=11
PA=list(PAL0); PA[30:36]=list(W1)+list(W2)
PB=list(PAL0); PB[15:21]=list(W1)+list(W2)
# controles
assert ((A>0)==(E>0)).all(), 'silhouet'
_,n=label(A>0,diag=True); assert n==3, n
assert not (OOG&ZONE).any()
buiten=(A!=E)&~ZONE&~OOG; assert not buiten.any()
assert ((E==7)==(A==7)).all(), 'lijn 7'
assert (((E==6)|(E==7))[ZONE] == ((A==11)|(A==7))[ZONE]).all(), 'lijnen/donker blijven donker'
print('componenten 8-buur:',n)
print('oog-pixels gewijzigd:',OOG.sum(), '| onderkop:',((A!=E)&ONDERKOP).sum(),'(5->W1 %d, 6->W2 %d)'%((ONDERKOP&(E==5)).sum(),(ONDERKOP&(E==6)).sum()),
      '| lijf:',((A!=E)&LIJF).sum(),'(5->W1 %d, 6->W2 %d)'%((LIJF&(E==5)).sum(),(LIJF&(E==6)).sum()),'| erbuiten:',buiten.sum())
for l in log: print(*l)
# meting na
P=np.array(PA[:48]).reshape(16,3)
for nm,Z in [('onderkop',ONDERKOP),('lijf',LIJF)]:
    s=Z&(A>=3)&(A!=7)&(A!=8)&(A!=9)
    pe=PAL[E[s]]; pa=P[A[s]]; m=M[s]
    print(nm,'lum sprite oud %.0f nieuw %.0f model %.0f | R-B oud %.0f nieuw %.0f model %.0f | |dlum| oud %.1f nieuw %.1f'%(
      L(pe).mean(),L(pa).mean(),L(m).mean(),(pe[:,0]-pe[:,2]).mean(),(pa[:,0]-pa[:,2]).mean(),(m[:,0]-m[:,2]).mean(),
      abs(L(pe)-L(m)).mean(),abs(L(pa)-L(m)).mean()))
def save(X,pal,fn):
    im=Image.fromarray(X.astype('uint8'),'P'); im.putpalette(pal); im.save(fn,transparency=0)
save(A,PA,'r5/claydol_g3r5.png'); save(S,PB,'r5/claydol_g3r5_paletB.png'); np.save('r5/sprite_r5.npy',A)
rgb=lambda X,pal:Image.fromarray(np.array(pal[:48],'uint8').reshape(16,3)[X])
rgb(A,PA).resize((512,512),0).save('r5/claydol_g3r5_8x.png')
rgb(S,PB).resize((512,512),0).save('r5/claydol_g3r5_paletB_8x.png')
