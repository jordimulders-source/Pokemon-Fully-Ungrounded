# r17 (alleen a_L1): basis r16-a_L1. Minder zwart, betere aansluiting, zigzag als heldere getrapte lijn.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r14'); sys.path.insert(0,'../sprite_r9')
from r14 import KL2, stuk, tint, B, H, W
INV={v:k for k,v in KL2.items()}
def rollen(f):
    im=Image.open(f); pal=np.array(im.getpalette()[:48]).reshape(16,3)
    return np.array([INV.get(tuple(c),'?') for c in pal])[np.asarray(im)]
R16=rollen('../sprite_r16/astro_a_L1.png')
def zwart(R): return int(sum(1 for y in range(26,47) for x in range(W) if R[y,x] in 'K1'))
KL={'r':('R','Q','Q'),'B':('B','B','b'),'W':('W','W','L')}
def bouw():
    R=R16.copy()
    # 1a. zwarte lijnen in het masker -> donkerrood Q (vorm blijft gelijk)
    for y in range(27,33):
        for x in range(28,37):
            if stuk[y,x]=='RO' and R[y,x]=='1': R[y,x]='Q'
    # 2. borst -> dijen: grotere getrapte tanden (2-3 px) die in elkaar grijpen; tinten per kolom
    TAND={(32,29):'B',(32,30):'r',(32,35):'r',
          (33,29):'B',(33,30):'B',(33,31):'r',(33,33):'r',(33,34):'r',(33,35):'B',(33,36):'B',
          (34,29):'B',(34,30):'r',(34,34):'r',(34,35):'r',(34,36):'B',(34,37):'B',
          (35,29):'B',(35,30):'B',(35,34):'r',(35,35):'B',(35,36):'B',(35,37):'B',
          (36,29):'B',(36,30):'B',(36,34):'B',(36,35):'B',(36,36):'B'}
    for (y,x),m in TAND.items():
        assert stuk[y,x],(y,x); R[y,x]=KL[m][tint[y,x]]
    # 3. zigzag: een heldere getrapte lijn van 1 px per rij, treden van 2 rijen, met de pijp mee; rij 46 punt blijft
    POS={36:0,37:0,38:1,39:1,40:2,41:2,42:1,43:1,44:0,45:0}
    for s in ('LL','RL'):
        for y,p in POS.items():
            r=[i for i in range(W) if stuk[y,i]==s]
            for i,x in enumerate(r): R[y,x]=KL['W' if i==p else 'B'][tint[y,x]]
    # 1b. spleet: binnenkant van de linkerpijp (x31) en de spleettop -> donkerste beentint / donkerrood
    for y in range(34,47):
        if R[y,31]=='K': R[y,31]='b'
    R[33,32]='Q'
    # selout lichtkant opnieuw: donkerste tint van het aangrenzende vlak (zelfde regel als r16)
    DONKER={'R':'Q','Q':'Q','B':'b','b':'b','W':'L','L':'S','M':'S','D':'S','Y':'D'}
    for y in range(26,48):
        for x in range(W):
            if B[y,x]!='K' or stuk[y,x]: continue
            if B[y,x-1]=='.' and stuk[y,x+1]: R[y,x]=DONKER.get(R[y,x+1],'S')
    return R
if __name__=='__main__':
    R=bouw(); print('zwart rij 26-46 (K en 1): r16 =',zwart(R16),' r17 =',zwart(R))
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,keys
    out=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[c for k in keys for c in KL2[k]]; out.putpalette(flat+[0]*(768-len(flat))); out.save('astro_a_L1.png',transparency=0)
    print(len(keys),'kleuren'); print('   '+''.join(str(i%10) for i in range(16,46)))
    for y in range(24,49): print('%2d '%y+''.join(R[y,16:46]))
