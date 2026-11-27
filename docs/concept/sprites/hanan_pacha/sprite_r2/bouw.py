# r2: basis = r1.png (vleugels, lijf) + vleugelschaduw (alleen tinten, silhouet en pengrenzen gelijk) + r5-staart onder
# (staart.py -> onder_kaal.npy) + geschaalde kop met kraag (kop.py -> kop_<f>.npy) + oog 1-op-1 uit een Gen 3-vogel.
# Gebruik: python3 bouw.py   (bouwt sprite_k120/k135/k150.png en tel.txt)
import sys, numpy as np; from PIL import Image
from scipy import ndimage
sys.path.insert(0,'gereedschap'); from gemeen import *
r1=np.array(Image.open('r1.png')).astype(int)
onder=np.load('onder_kaal.npy')
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
GRP={2:'g',3:'g',4:'g',5:'g',6:'w',7:'w',8:'r',9:'r',10:'r',11:'o',12:'o',15:'o',13:'p',14:'w'}
DONKER={'g':2,'w':6,'r':8,'o':11,'p':13}
def nb(o,Y,X,d=N4): return [o[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else 0 for dy,dx in d]
def schoon(o,zone):
    """technische opschoning zoals r1, alleen binnen zone (bool 64x64): binnenlijnen -> donkerste eigen tint, buitenlijn, ontkorrelen"""
    v=o.copy()
    for Y,X in zip(*np.where((v==1)&zone)):
        n8=nb(v,Y,X,N8)
        if 0 in n8: continue
        gs=[GRP[k] for k in n8 if k in GRP and k!=13]
        if gs:
            t={g:gs.count(g) for g in set(gs)}; b=max(t.values()); o[Y,X]=DONKER['g' if t.get('g',0)==b else max(t,key=t.get)]
    v=o.copy()
    for Y,X in zip(*np.where((v>0)&zone)):
        k=v[Y,X]
        if k==13: continue
        u,d,l,r=nb(v,Y,X)
        if 0 not in (u,d,l,r) or (l==0 and r==0) or (u==0 and d==0): continue
        if r==0 or d==0: o[Y,X]=1
        elif k==1:
            gs=[GRP[q] for q in nb(v,Y,X,N8) if q in GRP and q!=13]; o[Y,X]=DONKER[max(set(gs),key=gs.count)] if gs else 1
        else: o[Y,X]=DONKER[GRP[k]]
    for _ in range(2):
        for k,mi in ((3,3),(4,3),(5,2),(7,2),(9,3),(10,2),(12,2)):
            lab,n=ndimage.label((o==k)&zone)
            for i in range(1,n+1):
                m=lab==i
                if m.sum()>=mi: continue
                bu=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if 0<=Y+dy<64 and 0<=X+dx<64
                    and GRP.get(o[Y+dy,X+dx])==GRP[k] and o[Y+dy,X+dx] not in (k,DONKER[GRP[k]])]
                if bu: o[m]=max(set(bu),key=bu.count)
tel={}
# ---------- 1. onderkant: r5-staart achter de r7-klauwen (rijen >= 42) ----------
o=r1.copy(); ONDER=42
zone_onder=np.zeros((64,64),bool); zone_onder[ONDER:,:]=True
o[ONDER:]=onder[ONDER:]
schoon(o,zone_onder)
tel['onder (staart+klauwen), anders dan r1']=int((o[ONDER:]!=r1[ONDER:]).sum())
# ---------- 2. vleugelschaduw: alleen tinten binnen de groep, licht van linksboven ----------
# lichtrand: buur linksboven/boven/links buiten de groep en buur rechtsonder binnen de groep -> lichtste tint;
# schaduwrand: omgekeerd -> schaduwtint. Groepsgrenzen (pengrenzen) en silhouet veranderen niet.
LICHT={4:5,12:15,9:10,6:7}; DONK={4:3,12:11,9:8,7:6}
vleugel=np.zeros((64,64),bool); vleugel[:ONDER,:]=True
KOPZONE=(15,14,33,34)          # x0,y0,x1,y1: oude kop + kraag blijft buiten de vleugelschaduw
vleugel[KOPZONE[1]:KOPZONE[3],KOPZONE[0]:KOPZONE[2]]=False
v=o.copy()
def afstand(Y,X,G,dirs):
    best=9
    for dy,dx in dirs:
        n=0; y,x=Y,X
        while True:
            y+=dy; x+=dx; n+=1
            q=v[y,x] if 0<=y<64 and 0<=x<64 else 0
            if GRP.get(q)!=G or q==DONKER[G] or n>=9: break
        best=min(best,n)
    return best
LD=((-1,-1),(-1,0),(0,-1)); SD=((1,1),(1,0),(0,1))
for Y,X in zip(*np.where(vleugel&(v>0))):
    k=v[Y,X]
    if k not in LICHT and k not in DONK: continue
    G=GRP[k]; dl=afstand(Y,X,G,LD); ds=afstand(Y,X,G,SD)
    # lichtrand linksboven: 1 px, 2 px waar het vlak dik is; schaduwsikkel rechtsonder idem (volgt de vorm, geen rechte band)
    if k in LICHT and (dl==1 and ds>=2 or dl==2 and ds>=4): o[Y,X]=LICHT[k]
    elif k in DONK and (ds==1 and dl>=2 or ds==2 and dl>=4): o[Y,X]=DONK[k]
tel['vleugelschaduw (alleen tint)']=int((o!=v).sum())
basis=o.copy()
# ---------- 3. kop + kraag, 3 varianten ----------
def stempel(naam):
    im=Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%naam); return np.array(im)
OGEN={  # bron, uitsnede (x0,y0,x1,y1), kleurmap bronindex -> ons palet, oogmidden in de bron
 'spearow':('spearow',(23,21,28,27),{15:1,1:7,9:8,13:8},(25.0,23.5)),
 'pidgeot':('pidgeot',(11,23,16,28),{15:1,1:7,14:8,2:6},(13.0,25.0)),
}
KEUS={120:'spearow',135:'pidgeot',150:'pidgeot'}
A=np.array([23.5,33.1]); OOG=np.array([22.0,20.5])      # aanzetpunt kraag en oogmidden (r1/r7) in spritecoordinaten
for fk in (120,135,150):
    f=fk/100; o=basis.copy(); kop=np.load('kop_%d.npy'%fk)
    oud=np.zeros((64,64),bool); oud[KOPZONE[1]:KOPZONE[3],KOPZONE[0]:KOPZONE[2]]=np.isin(r1[KOPZONE[1]:KOPZONE[3],KOPZONE[0]:KOPZONE[2]],[8,9,10,14])
    kop=kop.copy(); kop[kop==13]=1            # grijze kraaglijn van het model is lijn, geen penpunt
    km=kop>0
    o[km]=kop[km]
    # koprand tegen vleugel/lijf: rand van de koplaag die aan een niet-kop figuurpixel grenst -> donkerste eigen tint (binnenlijn)
    v=o.copy(); nr=0
    for Y,X in zip(*np.where(km)):
        if v[Y,X] in (1,2,6,8,13): continue
        buiten=[(Y+dy,X+dx) for dy,dx in N4 if 0<=Y+dy<64 and 0<=X+dx<64 and not km[Y+dy,X+dx] and v[Y+dy,X+dx]>0]
        if buiten and GRP.get(v[Y,X]) in ('r','w'):
            o[Y,X]={'r':8,'w':6}[GRP[v[Y,X]]] if v[Y,X]!=14 else 14; nr+=o[Y,X]!=v[Y,X]
    for X,Y in ((21,20),(22,20),(18,22),(17,23),(18,23),(19,23),(17,24),(18,24),(16,23),(16,24),(17,22)): oud[Y,X]=True   # r1-hand oog/snavel
    rest=oud&~km
    # niet-bedekte oude koppixels: kleur van de dichtstbijzijnde pixel die geen kop is (vleugel/lijf erachter), mechanisch
    vrij=(o>0)&~oud&~km&~np.isin(o,[1,2]); _,(iy,ix)=ndimage.distance_transform_edt(~vrij,return_indices=True)
    o[rest]=o[iy[rest],ix[rest]]
    t={'kop/kraag uit model (geschaald)':int(km.sum()),'oude koppixels niet bedekt':int(rest.sum()),'koprand binnenlijn':int(nr)}
    # kop-rand: technische opschoning binnen de kop (+1 px rand)
    zone=ndimage.binary_dilation(km,iterations=1)
    v=o.copy(); schoon(o,zone); t['opschoning kop']=int((o!=v).sum())
    # snavel: modellijnen rond de snavel blijven zwart (anders smelt hij in de witte vleugelband); lichtste snavelpixel = ivoor 7
    sn=np.load('snavel_%d.npy'%fk); rond=ndimage.binary_dilation(sn,structure=np.ones((3,3)))&~sn
    terug=rond&(v==1)&(o!=1); o[terug]=1; t['snavellijn terug']=int(terug.sum())
    ys_,xs_=np.where(sn)
    if len(ys_):
        top=ys_==ys_.min(); X_=xs_[top].min(); Y_=ys_.min()
        if o[Y_,X_]!=7: o[Y_,X_]=7; t['snavel licht']=1
    # snavel ligt nu over de witte vleugelband: buren buiten de kop krijgen de zwarte snavelomlijning van het model
    nl=0
    for Y,X in zip(ys_,xs_):
        for dy,dx in N4:
            YY,XX=Y+dy,X+dx
            if 0<=YY<64 and 0<=XX<64 and not km[YY,XX] and o[YY,XX] not in (0,1): o[YY,XX]=1; nl+=1
    t['snavelomlijning tegen vleugel']=nl
    # oog: 1-op-1 uit een Gen 3-vogel, omgekleurd, op het geschaalde modeloog
    bron,(x0,y0,x1,y1),kmap,mid=OGEN[KEUS[fk]]; s=stempel(bron)
    doel=A+(OOG-A)*f; dx=int(round(doel[0]-mid[0])); dy=int(round(doel[1]-mid[1])); n=0
    for yy in range(y0,y1):
        for xx in range(x0,x1):
            k=s[yy,xx]
            if k in kmap:
                X,Y=xx+dx,yy+dy
                if o[Y,X]!=kmap[k]: n+=1
                o[Y,X]=kmap[k]
    t['oog (%s, %d px gestempeld)'%(bron,sum(1 for yy in range(y0,y1) for xx in range(x0,x1) if s[yy,xx] in kmap))]=n
    # klauwpixel dat los uitsteekt (3+ kanten achtergrond) -> weg
    for Y,X in zip(*np.where(np.isin(o,[7,14]))):
        if Y>=42 and sum(1 for dy,dx in N4 if not(0<=Y+dy<64 and 0<=X+dx<64) or o[Y+dy,X+dx]==0)>=3: o[Y,X]=0; t['uitstekende klauwpixel weg']=t.get('uitstekende klauwpixel weg',0)+1
    los=[(Y,X) for Y,X in zip(*np.where(o>0)) if all(not(0<=Y+dy<64 and 0<=X+dx<64) or o[Y+dy,X+dx]==0 for dy,dx in N8)]
    for Y,X in los: o[Y,X]=0
    t['losse pixel weg']=len(los)
    np.save('sprite_k%d.npy'%fk,o); opslaan(o,'sprite_k%d.png'%fk)
    tel['k%d'%fk]=t
for k,v in tel.items(): print(k,v)
