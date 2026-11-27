# r12 = r11 + F opnieuw (na de toonkaart): ontkorrelen (Krassault-regel): vultint-clusters < 3 px (geen lijn 1/2, geen glans 10/12, niet in oog/ring/
#   kussentje/teen-zones) nemen de meest voorkomende 8-buurtint uit dezelfde kleurgroep over. Herhaald tot stabiel. Gelogd.
from PIL import Image; import numpy as np, sys
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']')
L=np.load(D+'r11/idx.npy').copy(); H,W=L.shape
GROEP={3:{3,4,5,11},4:{3,4,5,11},11:{3,4,5,11,12},5:{3,4,5,6,7,11},6:{5,6,7,8},7:{5,6,7,8,9},8:{6,7,8,9},9:{7,8,9},
       13:{13,14,15},14:{13,14,15,12},15:{13,14,15,12,9}}
VAST=np.zeros((H,W),bool)
VAST[11:23,30:50]=True; VAST[44:54,46:59]=True; VAST[24:34,16:30]=True
VAST[2:7,29:35]=True; VAST[53:57,49:52]=True; VAST[59:63,51:59]=True
log=open(D+'r12/log.txt','w'); n=0
for it in range(4):
    ch=0
    for k in GROEP:
        lab,m=ndimage.label(L==k)
        for i in range(1,m+1):
            ys,xs=np.where(lab==i)
            if len(ys)>=3 or VAST[ys,xs].any(): continue
            nb=[]
            for y,x in zip(ys,xs):
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        yy,xx=y+dy,x+dx
                        if 0<=yy<H and 0<=xx<W and L[yy,xx] in GROEP[k] and L[yy,xx]!=k: nb.append(L[yy,xx])
            if not nb: continue
            t=max(set(nb),key=nb.count)
            for y,x in zip(ys,xs): log.write(f'({x},{y}) {k}->{t} F ontkorrel\n'); L[y,x]=t; n+=1; ch+=1
    if ch==0: break
print('F gewijzigd',n)
np.save(D+'r12/idx.npy',L); save_p64(L,PAL,D+'r12/sprite.png'); save_idx(L,PAL,D+'r12/r9_10x.png',10)
