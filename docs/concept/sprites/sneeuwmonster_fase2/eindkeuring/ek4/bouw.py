# Sneeuwmonster fase 2, eindkeuring ronde ek4 (Jordi: "kan je ze nog een klein beetje meer omringen, paar pixels aan de linkerkant van het steen
# zoals in het model? het rechteroog is boven nog een beetje puntig, verder vind ik hem goed"). Start = ek3 A en B. Palet ongewijzigd.
# Gebruik: cd sneeuwmonster_fase2 && python3 eindkeuring/ek4/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import s2m, MODEL
U='eindkeuring/ek4/'
a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); L=a@[.299,.587,.114]; warm=(a[...,0]-a[...,2]>60)&(a[...,0]>150)
def gloed(X,Y):   # gloedaandeel van het model in de steen/rand van deze spritepixel
    xa,xb=int(round(s2m(X,0)[0])),int(round(s2m(X+1,0)[0])); ya,yb=int(round(s2m(0,Y)[1])),int(round(s2m(0,Y+1)[1]))
    l=L[ya:yb,xa:xb]; w=warm[ya:yb,xa:xb]; st=(l<150)|w; return w.sum()/max(st.sum(),1)
# 1. gloed links aan de rand van elke steen, op de plekken waar het model links gloed heeft (gemeten; geen geel: >=50 % oranje, anders rood)
LINKS={'A':[(21,36),(21,39),(22,40),(21,44),(21,47)], 'B':[(21,36),(21,39),(22,40),(21,44),(20,47)]}
# 2. rechteroog: de puntige top = 2 donkere lijnpixels direct boven het oog (31,19) s, (32,19) l; model daar wit (L245/246) -> w.
#    Het oog wordt zo boven 3 px breed op 5 (zoals links 2 op 4): ronde bovenrand. Maat, kas en lidlijn van ek2 ongewijzigd.
OOGTOP=[(31,19,6,{3}),(32,19,6,{2})]
for v in ('A','B'):
    im=Image.open('eindkeuring/ek3/sneeuwmonster2_ek3%s.png'%v); base=np.asarray(im).astype(int); p=im.getpalette()[:48]
    o=base.copy(); log=[]
    for X,Y in LINKS[v]:
        g=gloed(X,Y); n=14 if g>=0.5 else 13
        assert base[Y,X]==1, (v,X,Y,base[Y,X])                     # alleen zwarte randpixels van de steen
        o[Y,X]=n; log.append((X,Y,'o' if n==14 else 'r',round(g*100)))
    for X,Y,n,van in OOGTOP:
        assert base[Y,X] in van; o[Y,X]=n; log.append((X,Y,'w'))
    D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
    assert ((base>0)==(o>0)).all() and len(D)==len(LINKS[v])+2
    print(v,'gewijzigd t.o.v. ek3',len(D),'px:',log)
    st=[(X,Y) for Y in range(33,51) for X in range(18,30) if o[Y,X] in (1,10,11,12,13,14,15)]
    print('   steen',len(st),'gloed',sum(o[y,x] in (13,14,15) for x,y in st),'geel',sum(o[y,x]==15 for x,y in st))
    q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(p); q.save(U+'sneeuwmonster2_ek4%s.png'%v,transparency=0)
    q.convert('RGBA').resize((512,512),Image.NEAREST).save(U+'sneeuwmonster2_ek4%s_8x.png'%v)
# ---- vel
def op(img,bg):
    arr=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(arr==0,0,255)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(Image.fromarray(rgba)); return b.convert('RGB')
M=Image.open(MODEL).convert('RGB')
def modelcrop(x0,y0,x1,y1,size):
    (a0,b0),(a1,b1)=s2m(x0,y0),s2m(x1,y1); w=Image.new('RGB',(int(round(a1-a0)),int(round(b1-b0))),(255,255,255)); w.paste(M,(-int(round(a0)),-int(round(b0)))); return w.resize(size,Image.LANCZOS)
I={k:Image.open('eindkeuring/%s.png'%k) for k in ('ek3/sneeuwmonster2_ek3A','ek3/sneeuwmonster2_ek3B','ek4/sneeuwmonster2_ek4A','ek4/sneeuwmonster2_ek4B')}
kol=[('ek3 A',I['ek3/sneeuwmonster2_ek3A']),('ek4 A',I['ek4/sneeuwmonster2_ek4A']),('ek3 B',I['ek3/sneeuwmonster2_ek3B']),('ek4 B',I['ek4/sneeuwmonster2_ek4B']),('model',None)]
z=16; SB=(18,32,30,51); OB=(27,17,38,26)
V=Image.new('RGB',(5*(12*z+16)+20,2000),(255,255,255)); d=ImageDraw.Draw(V); y=6
for t,box in (('stenen 16x',SB),('rechteroog 16x',OB)):
    sz=((box[2]-box[0])*z,(box[3]-box[1])*z)
    for i,(n,img) in enumerate(kol):
        x=10+i*(12*z+16); V.paste(op(img,(255,255,255)).crop(box).resize(sz,0) if img else modelcrop(*box,sz),(x,y+16)); d.text((x,y),t+': '+n,fill='black')
    y+=sz[1]+30
s=(V.width-20)//5-10
for i,(n,img) in enumerate(kol):
    x=10+i*(s+10); V.paste(op(img,(255,255,255)).resize((s,s),0) if img else modelcrop(0,0,64,64,(s,s)),(x,y+16)); d.text((x,y),n+' 8x',fill='black')
y+=s+30
rij=kol[:4]+[('fase 1',Image.open('../sneeuwmonster/af/sneeuwmonster.png')),('Skinguin',Image.open('../skinguin/af/skinguin.png'))]
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(V.width,110),bg),(0,y))
    for i,(n,img) in enumerate(rij):
        x=10+i*150; V.paste(op(img,bg),(x,y+20)); 
        if i<4: V.paste(op(img,bg).resize((64,64),0),(x+70,y+20))
        d.text((x,y+90),n,fill=(0,0,0) if j==0 else (230,230,230))
    y+=114
V=V.crop((0,0,V.width,y)); V.save(U+'vel.png'); print('vel',V.size)
