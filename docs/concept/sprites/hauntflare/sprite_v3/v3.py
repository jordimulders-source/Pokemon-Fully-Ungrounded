# Hauntflare v3: herkleuren op de plek, vanaf ../sprite_v2/hauntflare_v2.png. Niets getekend.
# Punten (coordinator): 1 glans terug, 2 oogcontrast, 3 ring voorkant 3 tonen langs de band, 4 kluwen ring/kuif,
# 5 bol 3 tinten + glans + selout zonder 1-2 px vlekjes. Gebruik (repo-root): python3 .../sprite_v3/v3.py
import json
from PIL import Image; import numpy as np
from scipy import ndimage as nd
D='docs/concept/sprites/hauntflare/'; V2=D+'sprite_v2/'; S=D+'sprite_v3/'
K4=[[0,1,0],[1,1,1],[0,1,0]]; K8=np.ones((3,3))
im2=Image.open(V2+'hauntflare_v2.png'); PALF=im2.getpalette()[:48]
o2=np.array(im2).astype(int); out=o2.copy()
G=np.load(V2+'groep.npy'); GZ=np.load(V2+'gezicht_masker.npy')
OP=o2>0; RAND=OP&nd.binary_dilation(~OP,K4)
yy,xx=np.mgrid[:64,:64]
LOG={}
def zet(mask,v,naam):
    ys,xs=np.where(mask&(out!=v)); LOG.setdefault(naam,[]).extend((int(x),int(y),int(out[y,x]),int(v)) for y,x in zip(ys,xs)); out[mask]=v
# ---------- model -> basis afbeelding (zelfde als basis.py / bouw.py) ----------
M=np.asarray(Image.open(D+'model/model_claude_natief.png').convert('RGB')).astype(int)
MW=M.min(2)>=0xe0
# achtergrond = wit dat met de beeldrand verbonden is; wit binnen de bol is glans
lab,_=nd.label(MW); rb=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); BG=np.isin(lab,[v for v in rb if v])
# de ringgaten zijn ook achtergrond (wit omsloten door ringpixels): alleen wit binnen de bolellips telt als glans
myy,mxx=np.mgrid[:99,:99]; mell=((mxx-38)/27.5)**2+((myy-41)/26)**2<=0.85
GL=(M.min(2)>=0xd0)&~BG&mell        # glans = wit (>=e0) + de lichte glansrand (d0-df) van het model
OUDGZ=np.zeros_like(GL); OUDGZ[35:54,25:47]=True   # oude modelogen (ook licht) tellen niet als glans
GL&=~OUDGZ
ys,xs=np.where(~MW); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
cw,ch=x1-x0,y1-y0; s=62/max(cw,ch); W,H=round(cw*s),round(ch*s); ox=(64-W)//2; oy=64-H-1
BX=ox+np.floor((mxx-x0+0.5)*W/cw).astype(int); BY=oy+np.floor((myy-y0+0.5)*H/ch).astype(int)
cnt=np.zeros((64,64)); tot=np.zeros((64,64))
np.add.at(cnt,(BY[GL],BX[GL]),1); IN=(~MW)|GL; np.add.at(tot,(BY[IN],BX[IN]),1)
GLANS=(cnt/np.maximum(tot,1)>=0.5)&(G==1)&~RAND
print('glans in basis',[(int(x),int(y),int(GZ[y,x])) for y,x in zip(*np.where(GLANS))])
LOG['model_glans_px']=int(GL.sum())
BOL=(G==1)&~RAND&~GZ
# ---------- 5) bol: 3 tinten (6/7/8) + glans (9) + selout (5) ----------
zet(BOL&(out==9)&~GLANS,8,'bol_9_naar_8')                 # wervel-licht buiten de glans -> licht
zet(BOL&(out==5)&~nd.binary_dilation(RAND|GZ,K8),6,'bol_5_binnen_naar_6')   # selout alleen aan de rand/het gezicht
zet(BOL&(out==14),8,'bol_14_naar_8')
# ---------- 1) glans terug op de plek van het model (niet onder gezichtspixels) ----------
zet(GLANS&~GZ,9,'glans')
# ---------- 5b) 1-2 px vlekjes in de bol gaan op in de buurtint (8-verbonden), glans blijft ----------
for _ in range(6):
    n=0
    for t in (6,7,8):
        l,k=nd.label(BOL&(out==t)&~GLANS,K8)
        for i in range(1,k+1):
            cl=l==i
            if cl.sum()>=3: continue
            nb=[out[y+a,x+b] for y,x in zip(*np.where(cl)) for a in(-1,0,1) for b in(-1,0,1)
                if (a or b) and BOL[y+a,x+b] and out[y+a,x+b] in (6,7,8,9) and out[y+a,x+b]!=t]
            if nb:
                nv=max(set(nb),key=nb.count); zet(cl,nv,'bol_vlekjes'); n+=1
    if not n: break
# ---------- 2) oogcontrast: geen oogwit direct naast glans/lichtroze -> middentint ----------
oogwit=GZ&(out==14)
naast=nd.binary_dilation(oogwit,K8)&BOL&np.isin(out,[8,9])
zet(naast,7,'oog_omgeving_middentint')
# glanskern: waar het model wit (>=e0) heeft, de glans wit, maar nooit binnen 2 px van een oogwit
cw2=np.zeros((64,64)); GW=MW&~BG&mell&~OUDGZ; np.add.at(cw2,(BY[GW],BX[GW]),1)
KERN=(cw2/np.maximum(tot,1)>=0.5)&(out==9)&~nd.binary_dilation(oogwit,K8,iterations=2)
zet(KERN,14,'glans_kern_wit')
# ---------- 5c) laatste pas: 1-2 px vlekjes (ook glans) die niet tegen een oogwit liggen -> buurtint ----------
OOGRAND=nd.binary_dilation(oogwit,K8)
TAND=nd.binary_fill_holes(nd.binary_dilation(GZ&~oogwit,K8,iterations=1))&~GZ   # bolroze binnen het gezicht (tanden)
for t in (6,7,8,9):
    l,k=nd.label(BOL&(out==t),K8)
    for i in range(1,k+1):
        cl=l==i
        if cl.sum()>=3 or (cl&(OOGRAND|TAND)).any(): continue
        nb=[out[y+a,x+b] for y,x in zip(*np.where(cl)) for a in(-1,0,1) for b in(-1,0,1)
            if (a or b) and BOL[y+a,x+b] and out[y+a,x+b] in (6,7,8) and out[y+a,x+b]!=t]
        if nb: zet(cl,max(set(nb),key=nb.count),'bol_vlekjes_laatste')
# ---------- 4) kluwen ring/kuif x45-50, y23-28 ----------
# roze bolpixels buiten de bolomlijning (x>=45) zijn de kuifpunt van het model -> kuifrood; donkerrode pixel in de
# ringomlijning -> zwart (een omlijning)
for x,y in [(45,25),(45,26)]:
    m=np.zeros((64,64),bool); m[y,x]=True; zet(m,11,'kluwen'); G[y,x]=3
m=np.zeros((64,64),bool); m[27,48]=True; zet(m,1,'kluwen')
# ---------- 3) ring: per verticale strook langs de band licht boven, midden, donker onder ----------
RINGV=(G==2)&np.isin(o2,[2,3,4])
# middellijn van de ring (linkerpunt ~(0,39), rechterpunt ~(59,31)); achterkant = boven die lijn
yc=lambda x:39-(x/59)*8
ACHTER=RINGV&(yy<yc(xx))
bolkuif=np.isin(G,[1,3])&OP
dichtbij=nd.binary_dilation(bolkuif,K8,iterations=3)
for x in range(64):
    y=0
    while y<64:
        if RINGV[y,x]:
            y2=y
            while y2+1<64 and RINGV[y2+1,x]: y2+=1
            L=y2-y+1
            for i,yy_ in enumerate(range(y,y2+1)):
                if L>=3: t=4 if i==0 else (2 if i==L-1 else 3)
                elif L==2: t=3 if i==0 else 2
                else: t=3
                if ACHTER[yy_,x] and dichtbij[yy_,x]: t=max(2,t-1)     # verdwijnt achter bol/kuif: donkerder
                m=np.zeros((64,64),bool); m[yy_,x]=True; zet(m,t,'ring')
            y=y2+1
        else: y+=1
# ring: losse 1-2 px tonen (8-verbonden) -> buurtint
for _ in range(4):
    n=0
    for t in (2,3,4):
        l,k=nd.label(RINGV&(out==t),K8)
        for i in range(1,k+1):
            cl=l==i
            if cl.sum()>=3: continue
            nb=[out[y+a,x+b] for y,x in zip(*np.where(cl)) for a in(-1,0,1) for b in(-1,0,1)
                if (a or b) and RINGV[y+a,x+b] and out[y+a,x+b]!=t]
            if nb: nv=max(set(nb),key=nb.count); zet(cl,nv,'ring_vlekjes'); n+=1
    if not n: break
# ---------- opslaan ----------
pim=Image.fromarray(out.astype('uint8'),'P'); pim.putpalette(PALF+[0]*(768-48)); pim.save(S+'hauntflare_v3.png',transparency=0)
P=np.array(PALF).reshape(-1,3); rgb=P[out].astype('uint8'); rgb[out==0]=255
Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(S+'hauntflare_v3_8x.png')
np.save(S+'gezicht_masker.npy',GZ)
d=out!=o2
LOG['diff_totaal']=int(d.sum())
LOG['diff_buiten_bol_ring_kluwen']=[(int(x),int(y)) for y,x in zip(*np.where(d&~((G==1)|(G==2)|((xx>=44)&(xx<=50)&(yy>=22)&(yy<=28)))))]
LOG['diff_op_gezicht_of_rand']=[(int(x),int(y)) for y,x in zip(*np.where(d&(GZ|(RAND&~((xx>=44)&(xx<=50)&(yy>=22)&(yy<=28))))))]
json.dump(LOG,open(S+'v3_log.json','w'))
print({k:(len(v) if isinstance(v,list) else v) for k,v in LOG.items()})
