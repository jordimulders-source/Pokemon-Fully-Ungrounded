"""Proef 'kop uit vormpunten': de kop wordt niet verkleind uit pixels, maar uit een handvol hoekpunten
die op de FRONT zijn afgelezen (meten, niet ontwerpen). Hoekpunten -> zelfde transformatie als a2
(kop 0.50, oren 0.56 rond de nek) -> polygonen gerasterd met 8x8 supersampling (dekking >= DREMPEL).
Oog = vaste bouwsteen (zwart + 1 witte glans) op de omgerekende plek. Lijf = icon_a2_af (Jordi's keuze).
python3 kop_vector.py uit [kopfactor] [oorfactor] [drempel]"""
import sys, numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/viscacha/'; S=sys.path[0]+'/'
uit=sys.argv[1]; SK=float(sys.argv[2]) if len(sys.argv)>2 else .50; SO=float(sys.argv[3]) if len(sys.argv)>3 else .56
DR=float(sys.argv[4]) if len(sys.argv)>4 else .5
FS=float(sys.argv[5]) if len(sys.argv)>5 else .65
base=np.array(Image.open(D+'icoon/onderdelen/icon_a2_af.png'))[:32].copy(); PAL=Image.open(D+'icoon/onderdelen/icon_a2_af.png').getpalette()
s_l=.38; NEK=np.array([21.,38.]); OFF=np.array([12.,8.]); SH=np.array([-7.,-2.])   # werkvlak -> icoon (a2_off)
def T(p,s): return OFF+NEK*s_l+(np.array(p,float)-NEK)*s+SH
# ---- vormpunten, afgelezen op de front (x,y in frontpixels, rand = buitenkant omlijning) ----
VORM={
 'verre oor':  ('oor',[(9.5,26),(9,20),(10,16),(11.5,14.8),(13,16.5),(14,21),(14.5,25)]),
 'kop':        ('kop',[(9,27),(12,25.5),(19,25.5),(23,26),(25,29),(24,34),(21,38),(15,38.5),(9.5,38.5),(7.5,37),(6.5,34.5),(7.5,31),(8.5,28.5)]),
 'nabije oor': ('oor',[(19,26),(19.5,21),(21,17.5),(23,15.8),(25.5,15.8),(27,17),(27,22),(26,26)]),
 'wangpluk':   ('kenmerk',[(6,27.5),(7.5,29),(9.5,32),(8.5,33.5),(5.5,33),(4.8,31)]),
 'kraag':      ('kenmerk',[(26.5,27.5),(27.5,29),(24.5,32),(22.5,35),(22.5,37.8),(20.5,36.2),(19.5,37.8),(17.8,35.5),(19.5,32),(23,29.2)]),
}
OOG=(16.5,30.0)
BASIS={'verre oor':(12,26),'nabije oor':(22,26)}          # midden van het zwarte oog in de front (glans op x=16)
KLEUR={'verre oor':6,'kop':7,'nabije oor':7,'wangpluk':9,'kraag':9}
ORDE=['verre oor','kop','nabije oor','wangpluk','kraag']
def raster(poly):
    Z=8; im=Image.new('L',(32*Z,32*Z),0); ImageDraw.Draw(im).polygon([tuple(p*Z) for p in poly],fill=255)
    a=np.array(im,float).reshape(32,Z,32,Z).mean((1,3))/255; return a>=DR
M={};
for n in ORDE:
    soort,pts=VORM[n]
    if soort=='oor':   # oor schaalt rond zijn eigen basis, die met de kop meegaat (aanhechting vast)
        b=np.array(BASIS[n]); M[n]=raster([T(b,SK)+(np.array(p)-b)*SO for p in pts])
    elif soort=='kenmerk':   # herkenningsteken: plek met de kop mee, maat overdreven (FS rond zijn eigen midden)
        c=np.mean(pts,0); M[n]=raster([T(c,SK)+(np.array(p)-c)*FS for p in pts])
    else: M[n]=raster([T(p,SK) for p in pts])
kopgeb=M['kop']|M['verre oor']|M['nabije oor']|M['wangpluk']|M['kraag']
out=base.copy()
# oude kop weg (alles links-boven van de nek dat niet tot het lijf hoort)
oud=np.zeros((32,32),bool); oud[:21,:16]=True
lijfmask=(base>0)&~oud
out[oud&~lijfmask]=0
lay=np.full((32,32),-1)
for r,n in enumerate(ORDE):
    out[M[n]]=KLEUR[n]; lay[M[n]]=r
# schaduw: kop onderste rij en rechterkant van de onderkaak donkerder (zoals de front: 3/4 onder de kaak)
# binnenlijn: verre oor tegen de kop
for y,x in zip(*np.nonzero(M['verre oor'])):
    for dy,dx in ((0,1),(1,0),(1,1)):
        yy,xx=y+dy,x+dx
        if yy<32 and xx<32 and lay[yy,xx]==1 and not M['kop'][y,x]: out[y,x]=15
# oorbinnenkant nabij oor: kolom links van de rand in 6 (front: cc-strook)
for y in range(32):
    xs=np.nonzero(M['nabije oor'][y]&~M['kop'][y])[0]
    if len(xs)>=3: out[y,xs[-2]]=6
# oog-bouwsteen
e=T(OOG,SK); ex,ey=int(np.floor(e[0])),int(np.floor(e[1]))
out[ey,ex-1]=3; out[ey,ex]=15; out[ey+1,ex-1]=15; out[ey+1,ex]=15
# kraag: punten licht (9), binnenkant goud (8)
for y,x in zip(*np.nonzero(M['kraag'])):
    if M['kop'][y,x] and x>0 and M['kraag'][y,x-1] and M['kraag'][y-1,x] if y>0 else False: out[y,x]=8
# snorharen: 1-px lijnen vanaf de snuitpunt, richting zoals in de front (naar links en linksonder)
sn=T((6.5,35),SK); sx,sy=int(sn[0]),int(sn[1])
for (dx,dy) in [(-1,0),(-2,0),(-3,-1),(-1,1),(-2,2)]:
    if out[sy+dy,sx+dx]==0: out[sy+dy,sx+dx]=1
# buitenomlijning opnieuw voor de nieuwe kop (boven 15, onder 14)
fig=(out>0)&(out!=1); p=np.pad(fig,1); rand=fig&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
yy,_=np.nonzero(fig); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(rand&kopgeb)):
    if out[y,x] not in (3,15): out[y,x]=15 if y<mid else 14
im=Image.fromarray(np.vstack([out,out]).astype(np.uint8),'P'); im.putpalette(PAL); im.save(S+uit+'.png')
for r in out[5:26,0:22]: print(''.join('.' if v==0 else '%x'%v for v in r))
