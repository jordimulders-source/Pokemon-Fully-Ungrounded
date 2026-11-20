# r17: pixelblad (blad64.npy) -> palet (uit modelkleuren, tinten uit elkaar) -> bevroren delen uit r16 -> technisch opschonen
import numpy as np, sys, json; sys.path.insert(0,'.')
from PIL import Image
from klassen import klassen; from bevroren import *
B=np.load('blad64.npy',allow_pickle=True).item(); rgb=B['rgb']; M=B['mask']
k,L=klassen(rgb,M)
p16=np.array(Image.open('../r16/hoatzin.png').getpalette()[:48]).reshape(16,3)
PAL=[(0x98,0xD0,0xA0),          # 0 transparant (zoals r16)
     (0x1C,0x10,0x1A),          # 1 lijn      (model, L 20)
     (0x3A,0x26,0x33),          # 2 donker    (model #33212C, L 40 -> 45)
     (0x64,0x48,0x5A),          # 3 midden    (model #66495B, L 83)
     (0x8C,0x6A,0x7E),          # 4 licht     (model #8A687A, L 117)
     (0xB4,0x94,0xA8),          # 5 strepen   (model #C6ABBE, L 181 -> 157: stap ±39)
     tuple(p16[6]),tuple(p16[7]),   # 6-7 kuif bruin (r16; Jordi: kuif bruiner)
     tuple(p16[8]),tuple(p16[9]),tuple(p16[10]),   # 8-10 blauw gezicht + rood oog (r16, bevroren)
     tuple(p16[11]),tuple(p16[12]),tuple(p16[13]), # 11-13 buik D
     tuple(p16[14]),tuple(p16[15])]               # 14-15 grijs snavel/poten (r16)
assert len(PAL)==16
LM=np.array([20,45,82,118,157])
idx=np.zeros((64,64),int)
mf=np.isin(k,['mauve','lijn','staart'])|((k=='grijs')&(Y<45))|((k=='blauw')&False)
W=B['why']; T=B['toon']
LL=np.where(W=='modus',T,L)          # vulling: gladde toonkaart; gepromoveerde lijnen/strepen: eigen modelkleur
idx[mf]=1+np.abs(LL[mf][:,None]-LM[None]).argmin(1)
b=k=='bruin'; idx[b]=np.where(L[b]<30,1,np.where(L[b]<62,6,7))
g=(k=='grijs')&(Y>=45); idx[g]=np.where(L[g]>=94,15,14)
# poten (onder de buik, links van de staart): het model is daar grijs met zwarte omlijning -> grijze tinten, geen mauve
POOT=M&(Y>=51)&(X<37)&~np.isin(k,['buik','staart'])
pv=POOT&(W!='dark')&(LL>=45); idx[pv]=np.where(LL[pv]>=92,15,14)
pd=POOT&~pv; idx[pd]=1
u=k=='buik'; idx[u]=np.where(L[u]<100,11,np.where(L[u]<118,12,13))
bl=k=='blauw'; idx[bl]=np.where(L[bl]<90,8,9)
# donkere VULLING (modus won, geen gepromoveerde lijn) is geen buitenlijn: -> tint 2; lijn 1 alleen voor gepromoveerde dunne modellijnen en de rand
vul1=(idx==1)&np.isin(W,['modus','mdark'])&~POOT; idx[vul1]=2
A=idx.copy(); np.save('stapA.npy',A)              # stap A: alleen kleurvertaling van het pixelblad
# bevroren delen uit r16, als geheel verschoven
SH=json.load(open('schuif.json'))
Ms=maskers(); frozen=np.zeros((64,64),bool); fz={}
for n,(dx,dy) in SH.items():
    m=Ms[n]; s=schuif(m,dx,dy); src=np.zeros((64,64),int); ys,xs=np.where(m)
    src[ys+dy,xs+dx]=R16[ys,xs]
    idx[s]=src[s]; frozen|=s; fz[n]=s
stapF=idx.copy()
# opschonen: (a) buitenlijn: randpixel (grenst aan transparant) in een lichte vlaktint -> lijn
def nb(a,y,x):
    return [a[y+dy,x+dx] for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)) if 0<=y+dy<64 and 0<=x+dx<64]
log=[]
cur=idx.copy()
for y in range(64):
    for x in range(64):
        if cur[y,x]==0 or frozen[y,x]: continue
        if 0 in nb(idx,y,x) or y in (0,63) or x in (0,63):
            if cur[y,x] in (3,4,5,7,13,15):
                new=1; log.append(('buitenlijn',x,y,int(cur[y,x]),new)); cur[y,x]=new
# (b) ruis: pixel zonder gelijke 8-buur (geen strepen/glans 5, geen bevroren) -> meest voorkomende 4-buurkleur
for it in range(2):
    nxt=cur.copy()
    for y in range(1,63):
        for x in range(1,63):
            v=cur[y,x]
            if v==0 or frozen[y,x] or v in (1,5): continue
            n8=cur[y-1:y+2,x-1:x+2].ravel(); same=(n8==v).sum()-1
            if same==0:
                n4=[c for c in nb(cur,y,x) if c!=0]
                if not n4: continue
                vals,cn=np.unique(n4,return_counts=True); new=int(vals[cn.argmax()])
                if new!=v: nxt[y,x]=new; log.append(('ruis',x,y,int(v),new))
    cur=nxt
out=cur
im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette([c for t in PAL for c in t]); im.info['transparency']=0
im.save('hoatzin.png',transparency=0); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%t for t in PAL))
np.save('r17.npy',out); json.dump(log,open('log.json','w'))
# telling per zone: afwijking t.o.v. het gemapte pixelblad (stap A)
Z={'kuif':(Y<22)&(X<30),'kop':(Y>=19)&(Y<30)&(X<16),'vleugel':(X>=28)&(Y<46),'nek/lijf':(Y>=22)&(Y<50)&(X>=12)&(X<34),
   'poten':(Y>=50)&(X<38),'staart':(Y>=46)&(X>=35)}
d=(out!=A)
print('afwijkend van stap A totaal',d.sum(),'van',(out>0).sum(),'| silhouet t.o.v. blad',((out>0)!=M).sum())
for n,z in Z.items(): print('  %-9s'%n,'px',(z&(out>0)).sum(),'afw',(d&z).sum(),' waarvan bevroren',(d&z&frozen).sum(),' opschoning',(d&z&~frozen).sum())
from collections import Counter; print('opschoning',Counter(l[0] for l in log))
print('kleuren',len(np.unique(out)))
