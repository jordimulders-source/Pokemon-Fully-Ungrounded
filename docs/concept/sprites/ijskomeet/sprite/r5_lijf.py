# r5: naden 1-op-1 uit het model (r5_dun.py, drempel 0.09), zone kop-onderkant + lijf; vlakken belicht als r4
import numpy as np, subprocess
from gio import from_txt, to_txt, CH
subprocess.run(['python3','r5_dun.py','0.09'],capture_output=True)
o=from_txt('r4.txt'); H,W=o.shape; C={c:i for i,c in enumerate(CH)}
S=np.load('r5_seam.npy'); zone=np.load('r5_zone.npy')
# zone: alleen vanaf rij 36, en in de kop links van de kern
for y in range(H):
    for x in range(W):
        if y<36 or (y<39 and x>21): zone[y,x]=0
zone&=~np.isin(o,[C['r'],C['c'],C['C'],C['g']])
S&=zone
# gaten dichten (gemeten op het model): rechterplaat linkerrand
for (x,y) in [(24,47),(24,48)]: S[y,x]=1
# onderste rij: geen doorlopende horizontale naad -> licht hellend, voet langer/platter
for x in range(13,22): S[55,x]=0
for x in range(21,25): S[56,x]=0
for (x,y) in [(13,55),(14,55),(15,55),(16,55),(17,55),(18,56),(19,56),(20,56),(21,56),(22,56),(23,56),(24,57)]: S[y,x]=1
for (x,y) in [(24,58),(25,58),(26,58)]: S[y,x]=0
for (x,y) in [(25,58)]: S[y,x]=1
# vlakken
lab=-np.ones_like(o); n=0
for y in range(H):
    for x in range(W):
        if zone[y,x] and not S[y,x] and lab[y,x]<0:
            st=[(y,x)]; lab[y,x]=n
            while st:
                a,b=st.pop()
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    q,r=a+dy,b+dx
                    if 0<=q<H and 0<=r<W and zone[q,r] and not S[q,r] and lab[q,r]<0: lab[q,r]=n; st.append((q,r))
            n+=1
LI={'W':'W','L':'W','M':'L','D':'M'}; DK={'W':'L','L':'M','M':'D','D':'D'}
kop=lab[40,10]
out=o.copy()
for k in range(n):
    pts=np.argwhere(lab==k)
    cols=[CH[o[y,x]] for y,x in pts if CH[o[y,x]] in 'WLMD']
    base=max('WLMD',key=cols.count) if cols else 'L'
    ys=pts[:,0]; y0,y1=ys.min(),ys.max()
    for y,x in pts:
        if k==kop:
            t=CH[o[y,x]] if CH[o[y,x]] in 'WL' else 'L'
            if S[y+1,x]: t='M'
            out[y,x]=C[t]; continue
        b=base
        if len(pts)>40 and y>y0+(y1-y0)*0.66: b=DK[base]
        if y>=57 and base in 'LM': b=DK[base] if y>=58 else b  # voet onder donkerder
        if S[y+1,x] or (o[y+1,x]==C['K'] and y>=56): t=DK[b]
        elif S[y-1,x] or S[y,x-1]: t=LI[b]
        else: t=b
        out[y,x]=C[t]
out[S]=C['S']
to_txt(out,'r5_lijf.txt'); np.save('r5_seam_af.npy',S)
for y in range(34,61): print('%2d '%y+''.join('.' if v<0 else CH[v] for v in out[y,:36]))
