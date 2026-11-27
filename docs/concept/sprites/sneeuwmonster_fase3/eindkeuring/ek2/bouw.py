# Ronde ek2 (sauna-yeti eindkeuring). Jordi: "midden, waarom is het hoofd nog een volledig effen kleur trouwens?"
# 1. pupilvariant A ("midden", eindkeuring/ogen/ogen.py): rechterpupil 1 px naar links, (33,24) <-> (34,24).
# 2. gezichtshuid in drie tinten volgens de gemeten modelhuid per spritepixel (natief raster, alleen huidcellen):
#    licht = w (modelhuid lichtste cellen (229,244,252) ~ w (244,250,255)), basis = h (200,226,236), schaduw = m (162,191,222)
#    (modelhuid-schaduwcellen (168,195,211)). Geen paletwijziging: w en m worden hergebruikt.
#    Regel per h-pixel: gemiddelde huid-L >= 222 -> licht (niet naast w-vacht, anders loopt het gezicht in de vacht over);
#    < 214 -> schaduw; anders basis. Losse pixel zonder buur van dezelfde klasse (8-buren) -> basis (geen tintvlakjes van 1 px).
# Lijnen, leden, pupillen, neus, glimlach: niet aangeraakt (assert: alleen h-pixels veranderen, plus de pupilwissel).
# Gebruik: cd sneeuwmonster_fase3 && python3 eindkeuring/ek2/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import MX0,MY0,F,CH
U='eindkeuring/ek2/'
im=Image.open('eindkeuring/sauna_yeti_ek.png'); ek=np.asarray(im).astype(int); PAL=im.getpalette()
o=ek.copy()
o[24,33],o[24,34]=ek[24,34],ek[24,33]                       # 1. pupil A
assert CH[o[24,33]]=='K' and CH[o[24,34]]=='w'
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[.299,.587,.114]
r,g,b=n[...,0],n[...,1],n[...,2]; huid=(L>=150)&((g-r)>=12)&((b-g)<=18)
yy,xx=np.mgrid[0:n.shape[0],0:n.shape[1]]
Xm=np.floor((xx+0.5-MX0)/F).astype(int); Ym=np.floor((yy+0.5-MY0)/F).astype(int)
klas={}; gem={}
for Y in range(20,33):
    for X in range(23,40):
        if ek[Y,X]!=5: continue
        c=L[(Xm==X)&(Ym==Y)&huid]
        if len(c)<2: continue
        v=c.mean(); gem[(X,Y)]=v
        naastvacht=any(ek[Y+dy,X+dx]==6 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
        klas[(X,Y)]=6 if (v>=222 and not naastvacht) else 4 if v<214 else 5
for (X,Y),k in list(klas.items()):
    if k!=5 and not any(klas.get((X+dx,Y+dy))==k or (k==4 and ek[Y+dy,X+dx]==4 and (dx or dy)) for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy):
        klas[(X,Y)]=5
stap={4:[],5:[],6:[]}
for (X,Y),k in klas.items():
    if k!=5: o[Y,X]=k; stap[k].append(((X,Y),int(gem[(X,Y)])))
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=ek)]
assert all(ek[Y,X]==5 or (X,Y) in ((33,24),(34,24)) for X,Y in D)
assert ((ek>0)==(o>0)).all()
print('pupil A: (33,24) w->K, (34,24) K->w')
print('licht (h->w) %d px:'%len(stap[6]),stap[6]); print('schaduw (h->m) %d px:'%len(stap[4]),stap[4])
print('basis blijft h:',sum(1 for k in klas.values() if k==5),'px; totaal diff',len(D))
q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(PAL); q.save(U+'sauna_yeti_ek2.png',transparency=0)
def op(img,bg=(255,255,255)):
    a=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(a==0,0,255)
    B=Image.new('RGBA',img.size,bg+(255,)); B.alpha_composite(Image.fromarray(rgba)); return B.convert('RGB')
e2=Image.open(U+'sauna_yeti_ek2.png'); op(e2).resize((512,512),0).save(U+'sauna_yeti_ek2_8x.png')
_m=np.asarray(Image.open('model.png').convert('RGB')).copy(); _m[_m.max(2)<12]=255; _m=Image.fromarray(_m); P5=1408/240
_w=Image.new('RGB',(int(64*F*P5),int(64*F*P5)),(255,255,255)); _w.paste(_m,(-int((MX0-1)*P5+4.5),-int((MY0-1)*P5+5))); mod=_w.resize((512,512),Image.LANCZOS)
X0,Y0,X1,Y1,s=20,18,42,34,16
nat=Image.open('natief.png').convert('RGB')
mz=nat.crop((int(round(MX0+X0*F)),int(round(MY0+Y0*F)),int(round(MX0+X1*F)),int(round(MY0+Y1*F)))).resize(((X1-X0)*s,(Y1-Y0)*s),0)
zs=[op(i.crop((X0,Y0,X1,Y1))).resize(((X1-X0)*s,(Y1-Y0)*s),0) for i in (im,e2)]+[mz]
V=Image.new('RGB',(3*532+10,24+512+40+zs[0].height+30+2*(64+40)),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,img) in enumerate((('ek',op(im).resize((512,512),0)),('ek2',op(e2).resize((512,512),0)),('model',mod))):
    V.paste(img,(10+i*532,24)); d.text((14+i*532,6),t,fill='black')
y=24+512+30; d.text((10,y-16),'gezicht 16x: ek | ek2 | model',fill='black')
for i,z in enumerate(zs): V.paste(z,(10+i*(z.width+16),y))
y+=zs[0].height+30
f2=Image.open('../sneeuwmonster_fase2/af/sneeuwmonster2.png')
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(V.width,64+30),bg),(0,y-6))
    for i,(t,img) in enumerate((('ek',im),('ek2',e2),('fase 2',f2),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Zapacha',Image.open('../viscacha/af/viscacha.png')))):
        V.paste(op(img,bg),(10+i*120,y)); d.text((10+i*120,y+66),t,fill=(0,0,0) if j==0 else (230,230,230))
    y+=64+40
V.save(U+'vel.png'); print('vel',V.size)
