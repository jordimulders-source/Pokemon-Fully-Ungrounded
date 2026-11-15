# Bewaakt p7 t.o.v. p6/p4: silhouet 0, r11-lijnen ongewijzigd, palet gelijk, oog (y26-29) = r11,
# diff met p6 alleen in de zones voorhoofd / tong-poot / rugband+krul / staart; geen index 6 in rugband en voorhoofd;
# clusterscan lila/crème < 3 px in de patroonzones; telt verschil met p4.
import sys, numpy as np
from collections import deque
from PIL import Image
R=np.array(Image.open('../r11/welp_r11.png')); P6=np.array(Image.open('../p6/welp_p6.png')); P4=np.array(Image.open('../p4/welp_p4.png'))
im=Image.open('welp_p7.png'); a=np.array(im); ok=True
def m(k,v,g):
    global ok; ok&=bool(g); print(k.ljust(44),v,'OK' if g else 'FOUT')
m('silhouet-diff',int(((a>0)!=(R>0)).sum()),((a>0)!=(R>0)).sum()==0)
m('r11-lijnen (1,2) gewijzigd',int((np.isin(R,[1,2])&(a!=R)).sum()),(np.isin(R,[1,2])&(a!=R)).sum()==0)
m('palet gelijk / indexen',len(set(a.ravel())),im.getpalette()[:48]==Image.open('../r11/welp_r11.png').getpalette()[:48] and len(set(a.ravel()))<=16)
m('oog (y26-29) = r11',int((a[26:30]!=R[26:30]).sum()),(a[26:30]!=R[26:30]).sum()==0)
Z={'voorhoofd':(12,20,25,26),'tong/poot':(10,41,15,43),'rug':(30,31,45,43),'staart':(51,52,57,57)}
z=np.zeros(a.shape,bool)
for (x0,y0,x1,y1) in Z.values(): z[y0:y1,x0:x1]=True
d=a!=P6; m('diff met p6 buiten de zones',int((d&~z).sum()),(d&~z).sum()==0)
for k,(x0,y0,x1,y1) in Z.items(): print('   diff',k,int(d[y0:y1,x0:x1].sum()),'px')
rz=np.zeros(a.shape,bool); rz[31:38,30:45]=True; rz[38:43,37:45]=True; rz[20:26,12:25]=True
m('index 6 in rugband/voorhoofd',int(((a==6)&rz).sum()),((a==6)&rz).sum()==0)
pz=np.zeros(a.shape,bool); pz[31:57,22:50]=True; pz[19:26,11:25]=True; pz[49:57,50:57]=True
for g,idx in {'lila':[6,7,8],'creme':[9,11]}.items():
    msk=np.isin(a,idx)&pz; seen=np.zeros_like(msk); klein=[]
    for y,x in zip(*np.where(msk)):
        if seen[y,x]: continue
        q=deque([(y,x)]); seen[y,x]=True; c=[]
        while q:
            cy,cx=q.popleft(); c.append((int(cx),int(cy)))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if msk[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
        if len(c)<3: klein.append(c)
    m('clusters < 3 px '+g,klein,len(klein)==0)
print('verschil met p4:',int((a!=P4).sum()),'px (p6 had 38)')
print('ALLES OK' if ok else 'FOUT'); sys.exit(0 if ok else 1)
