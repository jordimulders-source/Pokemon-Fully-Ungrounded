# Bewaakt p5 t.o.v. p4: silhouet-diff 0, r11-lijnen (1,2) ongewijzigd, palet gelijk, wijzigingen alleen in de 4 zones
# (tong/poot-grens, rugband+krul, voorhoofdsband, staart); clusterscan lila/crème (clusters < 3 px) in de patroonzones (lijf, voorhoofd, staart; oog en tanden niet).
import sys, numpy as np
from collections import deque
from PIL import Image
R=np.array(Image.open('../r11/welp_r11.png')); P4=np.array(Image.open('../p4/welp_p4.png'))
im=Image.open(sys.argv[1] if len(sys.argv)>1 else 'welp_p5.png'); a=np.array(im); ok=True
def m(k,v,g):
    global ok; ok&=bool(g); print(k.ljust(44),v,'OK' if g else 'FOUT')
m('silhouet-diff t.o.v. r11/p4',int(((a>0)!=(R>0)).sum()),((a>0)!=(R>0)).sum()==0)
m('r11-lijnpixels (1,2) gewijzigd',int((np.isin(R,[1,2])&(a!=R)).sum()),(np.isin(R,[1,2])&(a!=R)).sum()==0)
m('palet gelijk / indexen',len(set(a.ravel())),im.getpalette()[:48]==Image.open('../r11/welp_r11.png').getpalette()[:48] and len(set(a.ravel()))<=16)
Z={'tong/poot':(10,41,14,42),'voorhoofd':(11,20,22,26),'rug':(31,32,43,43),'staart':(51,52,56,57)}
zone=np.zeros(a.shape,bool)
for (x0,y0,x1,y1) in Z.values(): zone[y0:y1,x0:x1]=True
d=a!=P4
m('diff t.o.v. p4 buiten de 4 zones',int((d&~zone).sum()),(d&~zone).sum()==0)
for k,(x0,y0,x1,y1) in Z.items(): print('   diff',k,int(d[y0:y1,x0:x1].sum()),'px')
oog=[(20,27),(21,28),(12,27),(13,28)]
m('oogpixels gelijk aan r11',[(x,y) for x,y in oog if a[y,x]!=R[y,x]],all(a[y,x]==R[y,x] for x,y in oog))
for g,idx in {'lila':[6,7,8],'creme':[9,11]}.items():
    pz=np.zeros(a.shape,bool); pz[31:57,22:50]=True; pz[19:26,11:23]=True; pz[49:57,50:57]=True  # patroonzones (geen oog/tanden)
    msk=np.isin(a,idx)&pz; seen=np.zeros_like(msk); klein=[]
    for y,x in zip(*np.where(msk)):
        if seen[y,x]: continue
        q=deque([(y,x)]); seen[y,x]=True; c=[]
        while q:
            cy,cx=q.popleft(); c.append((int(cx),int(cy)))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if 0<=ny<64 and 0<=nx<64 and msk[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
        if len(c)<3: klein.append(c)
    m('clusters < 3 px '+g,klein,len(klein)==0)
print('ALLES OK' if ok else 'FOUT'); sys.exit(0 if ok else 1)
