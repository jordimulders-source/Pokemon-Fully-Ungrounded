# Bewaakt p6 t.o.v. p5: silhouet 0, r11-lijnen ongewijzigd, palet gelijk, diff alleen in het voorhoofd (y20-25, x12-24),
# oog/oren/buitenlijn gelijk; clusterscan lila/crème (< 3 px) in patroonzones (lijf, voorhoofd, staart).
import sys, numpy as np
from collections import deque
from PIL import Image
R=np.array(Image.open('../r11/welp_r11.png')); P5=np.array(Image.open('../p5/welp_p5.png'))
f=sys.argv[1] if len(sys.argv)>1 else 'welp_p6.png'; im=Image.open(f); a=np.array(im); ok=True
def m(k,v,g):
    global ok; ok&=bool(g); print(k.ljust(40),v,'OK' if g else 'FOUT')
print(f)
m('silhouet-diff',int(((a>0)!=(R>0)).sum()),((a>0)!=(R>0)).sum()==0)
m('r11-lijnen (1,2) gewijzigd',int((np.isin(R,[1,2])&(a!=R)).sum()),(np.isin(R,[1,2])&(a!=R)).sum()==0)
m('palet gelijk / indexen',len(set(a.ravel())),im.getpalette()[:48]==Image.open('../r11/welp_r11.png').getpalette()[:48] and len(set(a.ravel()))<=16)
z=np.zeros(a.shape,bool); z[20:26,12:25]=True; d=a!=P5
m('diff met p5 buiten voorhoofd',int((d&~z).sum()),(d&~z).sum()==0)
print('   diff voorhoofd',int((d&z).sum()),'px')
m('oog (y26-29) gelijk aan r11',int((a[26:30]!=R[26:30]).sum()),(a[26:30]!=R[26:30]).sum()==0)
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
print('ALLES OK' if ok else 'FOUT'); sys.exit(0 if ok else 1)
