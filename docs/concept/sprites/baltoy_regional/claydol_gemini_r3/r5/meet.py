import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r4'); sys.path.insert(0,'r2')
from PIL import Image
from natcoord import NY,NX,NAT
from cc import label
E=np.array(Image.open('eindkeuring/claydol_eind.png')); PAL=np.array(Image.open('eindkeuring/claydol_eind.png').getpalette()[:48]).reshape(16,3)
R3=np.load('r3/sprite_r3.npy'); print('silhouet eind==r3:',((E>0)==(R3>0)).all(), 'natcoord ok:',((NY>=0)==(E>0)).all())
comp,n=label(E>0,diag=True); print('comp',n)
M=np.zeros((64,64,3),int); ok=NY>=0; M[ok]=NAT[NY[ok],NX[ok]]
L=lambda c:(c*[0.299,0.587,0.114]).sum(-1)
np.save('r5/M.npy',M)
for y in range(28,61):
  print('%2d'%y,' '.join(('%3d'%L(M[y,x]) if E[y,x] else '  .') for x in range(10,56)))
print('mismatch natcoord:',np.argwhere((NY>=0)!=(E>0)).tolist()[:20])
L3=lambda c:(np.asarray(c)*[0.299,0.587,0.114]).sum(-1)
# zones
body=(comp==comp[50,30])
HEAD=np.zeros((64,64),bool); HEAD[27:40,10:51]=True
lowhead=HEAD&body
LIJF=np.zeros((64,64),bool); LIJF[40:61,10:51]=True; lijf=LIJF&body
from collections import Counter
for nm,Z in [('onderkop',lowhead),('lijf',lijf)]:
  print('==',nm, Z.sum())
  steen=Z&(E>=1)&(E<=7)
  pl=L3(PAL[E[steen]]); ml=L3(M[steen])
  print(' sprite lum gem %.1f model %.1f'%(pl.mean(),ml.mean()))
  print(' sprite R-B %.1f model R-B %.1f'%((PAL[E[steen]][:,0]-PAL[E[steen]][:,2]).mean(),(M[steen][:,0]-M[steen][:,2]).mean()))
  print(' sprite idx',sorted(Counter(E[steen]).items()))
  # model cluster colors
  c=Counter(tuple(v) for v in M[steen]); 
  q=Counter((tuple((np.array(k)//12*12))) for k in c.elements())
  print(' model kleuren top', c.most_common(12))
  # per model lum band what sprite idx
  for lo,hi in [(0,40),(40,110),(110,160),(160,200),(200,256)]:
    s=steen&(L3(M)>=lo)&(L3(M)<hi)
    print('  model lum %d-%d: n=%d sprite'%(lo,hi,s.sum()), sorted(Counter(E[s]).items()))
