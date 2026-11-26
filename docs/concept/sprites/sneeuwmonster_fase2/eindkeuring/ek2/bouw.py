# Sneeuwmonster fase 2, eindkeuring ronde ek2 (Jordi: "ooglid is een horizontale lijn en de stenen zijn nog niet helemaal herkenbaar als stenen").
# Start = eindkeuring/sneeuwmonster2_ek.png. Alleen: lidlijn van beide ogen + grijstinten binnen de stenen. Palet ongewijzigd.
# Gebruik: cd sneeuwmonster_fase2 && python3 eindkeuring/ek2/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import MX0,MY0,F,s2m,MODEL
U='eindkeuring/ek2/'
im=Image.open('eindkeuring/sneeuwmonster2_ek.png'); base=np.asarray(im).astype(int); p=im.getpalette()[:48]
PAL=[tuple(p[3*i:3*i+3]) for i in range(16)]
a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); L=a@[.299,.587,.114]; warm=(a[...,0]-a[...,2]>60)&(a[...,0]>150)
def blok(X,Y):
    xa,xb=int(round(s2m(X,0)[0])),int(round(s2m(X+1,0)[0])); ya,yb=int(round(s2m(0,Y)[1])),int(round(s2m(0,Y+1)[1]))
    return L[ya:yb,xa:xb],warm[ya:yb,xa:xb]
o=base.copy(); log={}
def zet(stap,X,Y,n,van):
    assert base[Y,X] in van,(stap,X,Y,base[Y,X]); o[Y,X]=n; log.setdefault(stap,[]).append((X,Y,n))
# ---- 1. OOGLID: per kolom de lidrij uit het model (donkergewogen zwaartepunt van L<70 binnen het oog, buiten de kasrand)
def lidrij(X,lo,hi):
    xa,xb=int(round(s2m(X,0)[0])),int(round(s2m(X+1,0)[0])); ya,yb=int(s2m(0,lo)[1]),int(s2m(0,hi)[1])
    col=L[ya:yb,xa:xb]; yy=((np.arange(ya,yb)-MY0)/F)[:,None]+0*col; w=np.clip(70-col,0,None); return (yy*w).sum()/w.sum()
LID={}
for X in range(21,25): LID[X]=lidrij(X,20.5,22.8)
for X in range(30,35): LID[X]=lidrij(X,20.8,23.2)
print('lid (model, spriterij):',{X:round(v,2) for X,v in LID.items()})
# linkeroog: x22-24 rij 21 (21,4); x21 = 21,74 (buitenhoek zakt): naar rij 22. rechteroog: x30-31 rij 21 (21,9/21,7), x32-34 rij 22 (22,0/22,4/22,7).
NIEUW={21:22,22:21,23:21,24:21, 30:21,31:21,32:22,33:22,34:22}
for X,Yn in NIEUW.items():
    Yo=21 if X<=24 else 22
    if Yn!=Yo:
        zet('O1 lidlijn volgt het model',X,Yn,1,{10,11})
        zet('O1 lidlijn volgt het model',X,Yo,10,{1})          # oude lidpixel -> donker grijs van de kas (model L79-109)
zet('O2 lichte kas boven het lid rechts',31,20,11,{10})          # het licht van (31,21) schuift mee omhoog; model L136 (G 165 / g 92)
# ---- 2. STENEN: grijstinten binnen de steen uit de modelhelderheid van de steenpixels (niet-gloed, L<150) per spritepixel
# >=78 -> 11 lichte facetrand (licht linksboven); 56-78 -> 10 licht facet; 30-56 -> 12 donkergrijs steenvlak; <30 -> 1 scheur/diepste schaduw. Gloed en buitenrand blijven.
SZ=lambda X,Y: 18<=X<=29 and 33<=Y<=50
N4=((1,0),(-1,0),(0,1),(0,-1))
STEEN={1,10,11,12,13,14,15}
for Y in range(33,51):
    for X in range(18,30):
        v=base[Y,X]
        if v not in (1,10,11,12): continue
        if not all(base[Y+dy,X+dx] in STEEN for dx,dy in N4): continue      # rand blijft (zwart = omlijning van de steen)
        l,wm=blok(X,Y); st=(l<150)&~wm
        if st.sum()<4: continue
        m=l[st].mean(); n=11 if m>=78 else 10 if m>=56 else 12 if m>=30 else 1
        if n!=v: zet('S2 stenen: facetten uit het model',X,Y,n,{v}); log.setdefault('_m',[]).append((X,Y,round(m)))
# ---- asserts: alleen ogen en steeninterieur gewijzigd; silhouet, mond, emmer, vacht index-diff 0
assert ((base>0)==(o>0)).all()
OGEN=lambda X,Y: (21<=X<=24 and 19<=Y<=23) or (30<=X<=34 and 20<=Y<=24)
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
for X,Y in D: assert OGEN(X,Y) or (SZ(X,Y) and base[Y,X] in (1,10,11,12)),(X,Y)
MOND={(20,24),(21,25),(22,26),(23,26),(24,25),(25,25),(26,25),(27,25),(28,26),(29,26),(30,26),(31,26),(32,26),(33,26),(34,25),(35,24)}
assert not [q for q in D if q in MOND]
assert not [q for q in D if base[q[1],q[0]] in (2,3,4,5,6,7,8,9)], 'vacht/emmer'
print('asserts: silhouet, mond, emmer (7-9), vacht (2-6), band buiten de ogen: index-diff 0')
for k,v in log.items(): print(k,len(v),v)
print('totaal',len(D),'px')
q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette([v for c in PAL for v in c]); q.save(U+'sneeuwmonster2_ek2.png',transparency=0)
Image.open(U+'sneeuwmonster2_ek2.png').convert('RGBA').resize((512,512),Image.NEAREST).save(U+'sneeuwmonster2_ek2_8x.png')
st=o[33:51,17:31]; print('stenen: gloed',np.isin(st,[13,14,15]).sum(),'K',(st==1).sum(),'12',(st==12).sum(),'10',(st==10).sum(),'11',(st==11).sum())
# ---- vel
def op(img,bg):
    arr=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(arr==0,0,255)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(Image.fromarray(rgba)); return b.convert('RGB')
ek=Image.open('eindkeuring/sneeuwmonster2_ek.png'); ek2=Image.open(U+'sneeuwmonster2_ek2.png')
M=Image.open(MODEL).convert('RGB')
def modelcrop(x0,y0,x1,y1,size):
    (a0,b0),(a1,b1)=s2m(x0,y0),s2m(x1,y1); w=Image.new('RGB',(int(a1-a0),int(b1-b0)),(255,255,255)); w.paste(M,(-int(a0),-int(b0))); return w.resize(size,Image.LANCZOS)
V=Image.new('RGB',(3*532,24+512+20+96+30+228+30+2*150),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,img) in enumerate((('ek',op(ek,(255,255,255)).resize((512,512),0)),('ek2',op(ek2,(255,255,255)).resize((512,512),0)),('model',modelcrop(0,0,64,64,(512,512))))):
    V.paste(img,(i*532,24)); d.text((i*532+4,6),t,fill='black')
y=24+512+20
for t,box in (('ogen 12x',(19,18,37,26)),('stenen 12x',(17,32,31,51))):
    x0,y0,x1,y1=box; sz=((x1-x0)*12,(y1-y0)*12)
    ims=[op(ek,(255,255,255)).crop(box).resize(sz,0),op(ek2,(255,255,255)).crop(box).resize(sz,0),modelcrop(*box,sz)]
    for i,img in enumerate(ims): V.paste(img,(i*532,y+14))
    d.text((4,y),t+': ek | ek2 | model',fill='black'); y+=sz[1]+30
fase1=Image.open('../sneeuwmonster/af/sneeuwmonster.png')
rij=[('ek',ek),('ek2',ek2),('fase 1',fase1),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Dundragoon',Image.open('../dundragoon/af/dundragoon.png')),('Zapacha',Image.open('../viscacha/af/viscacha.png'))]
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(V.width,146),bg),(0,y)); 
    for i,(t,img) in enumerate(rij):
        x=10+i*212 if i<3 else 10+3*212+(i-3)*90; V.paste(op(img,bg),(x,y+40))
        if i<3: V.paste(op(img,bg).resize((128,128),0),(x+70,y+8))
        d.text((x,y+110),t,fill=(0,0,0) if j==0 else (230,230,230))
    y+=150
V=V.crop((0,0,V.width,y)); V.save(U+'vel.png'); print('vel',V.size)
