# r4: exacte 2x2-reductie van het natieve raster (68x70 -> 34x35), Krassault-stijl (octillery_evo/sprite3/half2.py).
# Niets getekend: elke spritepixel komt uit zijn 2x2-blok modelklassen (klassen.py). Gebruik: python3 gereedschap/half_r4.py [oy ox]
# Regels per blok: >=3 transparant -> transparant; lijn (K/D) als >=2 lijnpixels, of 1 lijnpixel op de buitenrand;
# rood als >=2 rood; anders meerderheid van de vulklassen (bij gelijkspel de donkerste: lijnen/kerven blijven).
import numpy as np, sys
sys.path.insert(0,'gereedschap'); from klassen import laad
S='.KDdmMlhRr'
def reduceer(oy=0,ox=0):
    k,_=laad(); k=np.pad(k,((1,1),(1,1)))[1-oy:,1-ox:]
    H,W=k.shape; h,w=H//2,W//2; o=np.zeros((h,w),int)
    for j in range(h):
        for i in range(w):
            b=k[2*j:2*j+2,2*i:2*i+2].ravel()
            if (b==0).sum()>=3: continue
            ln=b[(b==1)|(b==2)]; rd=b[b>=8]; vul=b[(b>=3)&(b<=7)]
            rand=(b==0).any()
            if len(ln)>=2 or (len(ln)>=1 and rand): o[j,i]=1 if (ln==1).sum()>=(ln==2).sum() else 2; continue
            if len(rd)>=2: o[j,i]=8 if (rd==8).sum()>=(rd==9).sum() else 9; continue
            if len(vul)==0: o[j,i]=ln[0] if len(ln) else rd[0]; continue
            v,c=np.unique(vul,return_counts=True); o[j,i]=v[c==c.max()].min()
    ys,xs=np.where(o>0); return o[ys.min():ys.max()+1,xs.min():xs.max()+1]
if __name__=='__main__':
    oy,ox=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (0,0)
    o=reduceer(oy,ox); print(o.shape)
    for y,r in enumerate(o): print('%2d '%y+''.join(S[v] for v in r))
