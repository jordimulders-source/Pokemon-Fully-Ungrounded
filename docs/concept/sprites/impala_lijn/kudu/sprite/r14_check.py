# Bewijs r14 t.o.v. r13: silhouet, oog K4, strepen, vulling (alles behalve lijnrol) en per-zone telling.
import numpy as np
from PIL import Image
g0=np.load('/dev/stdin') if False else None
P={'302418':'0','F8D888':'L','D8A850':'M','A07030':'D','D8AC30':'l','B08824':'m','7C5A10':'d','4A4A52':'A','8A8A92':'3',
   'C8C8CC':'4','FFFFFF':'W','E0A090':'R','B06A58':'r','5C4434':'K'}
a=np.array(Image.open('r13/kudu_r13.png').convert('RGBA'))
g0=np.array([['.' if a[y,x,3]==0 else P['%02X%02X%02X'%tuple(a[y,x,:3])] for x in range(64)] for y in range(64)])
im=Image.open('r14/kudu_r14.png'); assert im.mode=='P'; idx=np.array(im); g=np.load('r14/grid.npy')
pal=np.array(im.getpalette()[:48]).reshape(16,3)
print('modus',im.mode,'kleuren in gebruik',len(np.unique(idx))-1,'(+ index 0 transparant), index 0 alleen op transparant:',((idx==0)==(g=='.')).all())
print('silhouet (alpha) diff:',((g0=='.')!=(g=='.')).sum())
oog=(slice(21,25),slice(15,20)); print('oogvlak K4 x15-19 y21-24 diff (letters):',(g0[oog]!=g[oog]).sum(),'| K-tint 5C4434 -> 6E4614 (zelfde rol)')
print('W-pixels (strepen, slijprand, snuit) diff:',((g0=='W')!=(g=='W')).sum())
VUL=set('LMDlmd34WRr')
print('vulpixels (niet-lijn) veranderd van letter:',((g0!=g)&np.isin(g0,list(VUL))).sum(),'-> alleen de 2 open randen (M->K) zijn vul->lijn')
print('hoornvulling (3/4/W in hoornbox) diff:',((g0!=g)&np.isin(g0,list('34W'))).sum())
ch=np.argwhere(g0!=g)
Z={'hoorns (y<15)':lambda x,y:y<15,'kop/oren (y15-29, x<24)':lambda x,y:15<=y<30 and x<24,
   'manen+franje+halsstrook (x14-37, y23-42, niet kop)':lambda x,y:23<=y<=42 and 14<=x<=37 and not (y<30 and x<24),
   'lijf/staart':lambda x,y:y<=46 and x>37,'poten (y>=43)':lambda x,y:y>=43}
tel={k:0 for k in Z}; tel['overig']=0
for y,x in ch:
    for k,f in Z.items():
        if f(x,y): tel[k]+=1; break
    else: tel['overig']+=1
print('veranderde px per zone:',tel,'totaal',len(ch))
from collections import Counter
print('overgangen:',Counter(g0[y,x]+'->'+g[y,x] for y,x in ch))
dark=np.isin(g,list('0K')).sum()/(g!='.').sum(); dark0=np.isin(g0,list('0K')).sum()/(g0!='.').sum()
print('aandeel zeer donker (0+K): r13 %.3f -> r14 %.3f (E3 band 0,10-0,25)'%(dark0,dark))
print('zwart 0 op de rand r13 %d -> r14 %d'%((g0=='0').sum(),(g=='0').sum()))
