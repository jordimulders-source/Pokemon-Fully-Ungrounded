# Bewaakt p2: silhouet-diff 0 t.o.v. r11, lijnen (1,2) ongewijzigd, palet gelijk, y<30 gelijk aan r11,
# diff t.o.v. p1_C alleen in de patroonzones; clusterscan: patroonpixels zonder 4-buur uit dezelfde kleurgroep (lila/crème)
# en clusters < 3 px per groep.
import sys, numpy as np
from PIL import Image
R=np.array(Image.open('../r11/welp_r11.png')); C=np.array(Image.open('../p1/welp_p1_C.png'))
im=Image.open(sys.argv[1] if len(sys.argv)>1 else 'welp_p2.png'); a=np.array(im)
ok=True
def m(k,v,good): global ok; ok&=good; print(k.ljust(42),v,'OK' if good else 'FOUT')
m('silhouet-diff t.o.v. r11',int(((a>0)!=(R>0)).sum()),((a>0)!=(R>0)).sum()==0)
m('lijnpixels (1,2) gewijzigd',int((np.isin(R,[1,2])&(a!=R)).sum()),(np.isin(R,[1,2])&(a!=R)).sum()==0)
m('diff t.o.v. r11 voor y<30',int((a[:30]!=R[:30]).sum()),(a[:30]!=R[:30]).sum()==0)
m('palet gelijk aan r11 / indexen incl. transparant',(im.getpalette()[:48]==Image.open('../r11/welp_r11.png').getpalette()[:48],len(set(a.ravel()))),im.getpalette()[:48]==Image.open('../r11/welp_r11.png').getpalette()[:48] and len(set(a.ravel()))<=16)
zone=np.zeros(a.shape,bool); zone[31:57,22:50]=True   # lijfpatroonzone (schouder, rug, heup, staartje)
d=(a!=C); m('diff t.o.v. p1_C buiten lijfzone',int((d&~zone).sum()-(d[:30]).sum()),(d&~zone).sum()-(d[:30]).sum()==0)
print('diff t.o.v. p1_C binnen lijfzone:',int((d&zone).sum()),'px; t.o.v. r11 totaal:',int((a!=R).sum()))
G={'lila':[6,7,8],'creme':[9,11,14]}
from collections import deque
for g,idx in G.items():
    msk=np.isin(a,idx)&zone&~np.isin(R,[14])  # voeten-perzik van r11 telt niet
    seen=np.zeros_like(msk); klein=[]
    for y,x in zip(*np.where(msk)):
        if seen[y,x]: continue
        q=deque([(y,x)]); seen[y,x]=True; comp=[]
        while q:
            cy,cx=q.popleft(); comp.append((cx,cy))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if 0<=ny<64 and 0<=nx<64 and msk[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
        if len(comp)<3: klein.append(comp)
    m('clusters < 3 px in groep '+g,klein,len(klein)==0)
print('ALLES OK' if ok else 'FOUT'); sys.exit(0 if ok else 1)
