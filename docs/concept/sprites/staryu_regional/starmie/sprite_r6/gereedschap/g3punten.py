# g3punten.py: meet de twee Gen 3 Starmie-punten die Jordi aanwees (referenties/jordi_starmie_punten.png):
# 'rl' = lichte punt naar rechts (tip 59,33), 'br' = donkere punt naar rechtsonder (tip 54,47). Schijven van 1 px loodrecht op de as kern->tip.
# Gebruik: cd starmie && python3 sprite_r6/gereedschap/g3punten.py
import sys,numpy as np
sys.path.insert(0,'gereedschap'); from gen3 import laad,punt_van,C,TIPS
g,pal=laad()
for n in ('rl','br'):
    m=np.zeros((64,64),bool)
    for y,x in zip(*np.where(g>0)):
        if punt_van(x,y)==n: m[y,x]=True
    ys,xs=np.where(m); p=np.stack([xs+.5,ys+.5],1); c=np.array(C)
    d=np.hypot(*(p-c).T); tip=p[np.argmax(d)]; ax=(tip-c)/np.linalg.norm(tip-c); pe=np.array([-ax[1],ax[0]])
    t=(p-c)@ax; s=(p-c)@pe; T=t.max()
    print(n,'tip',tip,'richting',np.degrees(np.arctan2(-ax[1],ax[0])),'T',T)
    for k in range(0,12):
        sl=(t>T-k-1)&(t<=T-k)
        print(' slice',k,'breedte',round(s[sl].max()-s[sl].min()+1,1) if sl.any() else 0,'n',sl.sum(),'s',np.round(np.sort(s[sl]),1) if sl.sum()<8 else '')
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    for y in range(y0,y1+1): print('  %2d'%y,''.join(('.' if not m[y,x] else '0123456789ABCDEF'[g[y,x]]) for x in range(x0,x1+1)))
