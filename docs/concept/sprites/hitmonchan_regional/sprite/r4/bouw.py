# r4: buitenlijn-tint. Randpixels (achtergrondbuur) met een lichte tint (index >=6):
#  - lichtkant (achtergrond boven of links): donkerste modelkleur in dat gebied (M_donker) als die <=5 is, anders 4 (de selout-tint van het model);
#  - schaduwkant (alleen rechts/onder achtergrond): 1 als M_donker <=3, anders M_donker.
# Alleen de tint verandert, niet de plek. Basis r3.
import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
S=np.load(D+'r3/idx.npy'); Dk=np.load(D+'M_donker.npy'); pal=eval(open(D+'pal.txt').read())
H,W=S.shape; P=np.pad(S,1); T=S.copy(); log=[]
for y in range(H):
    for x in range(W):
        if S[y,x]<6: continue
        N,Sd,Wd,E=P[y,x+1]==0,P[y+2,x+1]==0,P[y+1,x]==0,P[y+1,x+2]==0
        if not (N or Sd or Wd or E): continue
        if N or Wd: v=Dk[y,x] if 1<=Dk[y,x]<=5 else 4
        else: v=1 if Dk[y,x]<=3 else Dk[y,x]
        T[y,x]=v; log.append(f'({x},{y}) {S[y,x]}->{v}')
np.save(D+'r4/idx.npy',T); open(D+'r4/log.txt','w').write('\n'.join(log)+'\n'); print(len(log))
save_p64(T,pal,D+'r4/sprite.png'); save_idx(T,pal,D+'r4/r4_8x.png',8)
