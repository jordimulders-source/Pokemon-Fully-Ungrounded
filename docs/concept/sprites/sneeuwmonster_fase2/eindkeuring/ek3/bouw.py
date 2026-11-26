# Sneeuwmonster fase 2, eindkeuring ronde ek3: alleen de stenen (ooglid = ek2). Palet ongewijzigd.
# A: binnen de huidige steenomtrek; gloed alleen in de 1 px scheur van het model + dunne rand rechtsonder (~26 %), geel 1 px per steen in de heetste scheur.
# B: als A + hoekige omtrek: een paar vachtpixels direct naast de steen worden steen (max 6 per steen), volgens de modelbrok.
# Gebruik: cd sneeuwmonster_fase2 && python3 eindkeuring/ek3/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import s2m, MODEL
U='eindkeuring/ek3/'
im=Image.open('eindkeuring/ek2/sneeuwmonster2_ek2.png'); base=np.asarray(im).astype(int); p=im.getpalette()[:48]
PAL=[tuple(p[3*i:3*i+3]) for i in range(16)]
T={'K':1,'c':12,'g':10,'G':11,'r':13,'o':14,'y':15}
STEEN={1,10,11,12,13,14,15}
# Steen per rij: (x van de eerste pixel, tekens). K = zwarte rand / diepste schaduw, c = steen, g = licht facet, G = lichte facetrand, r/o/y = gloed.
# Boven (model: lichte facetten linksboven x23-25 r35-36, middengrijs facet onder de scheur x23-24 r38, scheur r37 x23-26 met geel op x24 en
#   doorlopend naar de rechterrand bij (27,35); gloedrand rechts x27-28 r35-39 en onder r40-41)
BOVEN_A={34:(23,'KKK'),35:(22,'KgGgcr'),36:(21,'KgggcoK'),37:(21,'KcryocKo'),38:(21,'KcggcKKo'),39:(21,'KcccKKr'),40:(22,'KcKKr'),41:(23,'rrr')}
# Onder (model: lichte facetten links x21-23 r44-46, scheur van (22,44) via geel (23,45) naar (25,46), gloedrand rechts x26-27 r44-48 en onder x24-25 r49)
ONDER_A={43:(22,'KKKK'),44:(21,'KrGgcr'),45:(20,'KggyocKo'),46:(20,'KcgccrKo'),47:(21,'KcccKKr'),48:(21,'KKcKKo'),49:(23,'Krr')}
# B: hoekige omtrek (model): boven vlakke top tot x26, rechte rechterflank x28 r36-39, scherpe hoek linksonder; onder rechte linkerflank x20 r45-47,
#   vlakke onderkant x22-25 r49, vierkante hoek rechtsonder (27,48).
BOVEN_B={34:(23,'KKKK'),35:(22,'KgGgcr'),36:(21,'KgggcoKr'),37:(21,'KcryocKo'),38:(21,'KcggcKKo'),39:(21,'KcccKKrr'),40:(21,'KKcKKr'),41:(23,'rrr')}
ONDER_B={43:(22,'KKKK'),44:(21,'KrGgcr'),45:(20,'KggyocKo'),46:(20,'KcgccrKo'),47:(20,'KKcccKKr'),48:(21,'KKcKKoo'),49:(22,'KKrr')}
def bouw(*stenen):
    o=base.copy()
    for st in stenen:
        for Y,(x0,s) in st.items():
            for i,ch in enumerate(s): o[Y,x0+i]=T[ch]
    return o
def zones(o):
    return [(X,Y) for Y in range(64) for X in range(64) if o[Y,X]!=base[Y,X]]
oA=bouw(BOVEN_A,ONDER_A); oB=bouw(BOVEN_B,ONDER_B)
# ---- asserts
OOG_MOND_EMMER=lambda X,Y: Y<=26
for naam,o,maxnieuw in (('A',oA,0),('B',oB,6)):
    assert ((base>0)==(o>0)).all(),'silhouet'
    D=zones(o)
    assert all(33<=Y<=50 and 19<=X<=29 for X,Y in D),(naam,'buiten de steenzone')
    nieuw=[(X,Y) for X,Y in D if base[Y,X] not in STEEN]                     # vacht -> steen
    weg=[(X,Y) for X,Y in D if o[Y,X] not in STEEN]                           # steen -> vacht
    for lo,hi in ((33,42),(42,51)):
        n=len([q for q in nieuw+weg if lo<=q[1]<hi]); assert n<=maxnieuw,(naam,n)
    # de vacht buiten de direct aangrenzende pixels blijft gelijk
    for X,Y in nieuw: assert any(base[Y+dy,X+dx] in STEEN for dy in (-1,0,1) for dx in (-1,0,1)),(naam,X,Y)
    assert not [q for q in D if OOG_MOND_EMMER(*q)]
    vacht_rest=[(X,Y) for X,Y in D if base[Y,X] not in STEEN and (X,Y) not in nieuw]; assert not vacht_rest
    st=[(X,Y) for Y in range(33,51) for X in range(18,30) if o[Y,X] in STEEN]
    gl=[q for q in st if o[q[1],q[0]] in (13,14,15)]
    print('%s: %d px gewijzigd t.o.v. ek2 (vacht->steen %s); steen %d px, gloed %d (%.0f %%), geel %d, K %d, steen %d, g %d, G %d'%(naam,len(D),nieuw,len(st),len(gl),100*len(gl)/len(st),
        sum(o[y,x]==15 for x,y in st),sum(o[y,x]==1 for x,y in st),sum(o[y,x]==12 for x,y in st),sum(o[y,x]==10 for x,y in st),sum(o[y,x]==11 for x,y in st)))
    q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette([v for c in PAL for v in c]); q.save(U+'sneeuwmonster2_ek3%s.png'%naam,transparency=0)
    q.convert('RGBA').resize((512,512),Image.NEAREST).save(U+'sneeuwmonster2_ek3%s_8x.png'%naam)
st0=[(X,Y) for Y in range(33,51) for X in range(18,30) if base[Y,X] in STEEN]
print('ek2: steen %d px, gloed %d'%(len(st0),sum(base[y,x] in (13,14,15) for x,y in st0)))
# ---- vel: rij 1 stenen 16x (ek2 | A | B | model), rij 2 hele sprite 8x, rij 3-4 1x/2x op licht en donker
def op(img,bg):
    arr=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(arr==0,0,255)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(Image.fromarray(rgba)); return b.convert('RGB')
M=Image.open(MODEL).convert('RGB')
def modelcrop(x0,y0,x1,y1,size):
    (a0,b0),(a1,b1)=s2m(x0,y0),s2m(x1,y1); w=Image.new('RGB',(int(round(a1-a0)),int(round(b1-b0))),(255,255,255)); w.paste(M,(-int(round(a0)),-int(round(b0)))); return w.resize(size,Image.LANCZOS)
ims=[('ek2',im),('A',Image.open(U+'sneeuwmonster2_ek3A.png')),('B',Image.open(U+'sneeuwmonster2_ek3B.png'))]
box=(18,32,30,51); z=16; sz=((box[2]-box[0])*z,(box[3]-box[1])*z)
W=4*(sz[0]+20)+20; V=Image.new('RGB',(max(W,3*532+20),24+sz[1]+40+512+30+2*150),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,img) in enumerate(ims+[('model',None)]):
    x=10+i*(sz[0]+20); V.paste(op(img,(255,255,255)).crop(box).resize(sz,0) if img else modelcrop(*box,sz),(x,24)); d.text((x,6),'stenen 16x: '+t,fill='black')
y=24+sz[1]+40
for i,(t,img) in enumerate(ims+[('model',None)]):
    x=10+i*(min(512,(V.width-20)//4)); s=min(512,(V.width-20)//4-10)
    V.paste(op(img,(255,255,255)).resize((s,s),0) if img else modelcrop(0,0,64,64,(s,s)),(x,y)); d.text((x,y-14),t+' 8x',fill='black'); hs=s
y+=hs+20
rij=ims+[('fase 1',Image.open('../sneeuwmonster/af/sneeuwmonster.png')),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Zapacha',Image.open('../viscacha/af/viscacha.png'))]
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(V.width,146),bg),(0,y))
    for i,(t,img) in enumerate(rij):
        x=10+i*212 if i<3 else 10+3*212+(i-3)*90; V.paste(op(img,bg),(x,y+40))
        if i<3: V.paste(op(img,bg).resize((128,128),0),(x+70,y+8))
        d.text((x,y+110),t,fill=(0,0,0) if j==0 else (230,230,230))
    y+=150
V=V.crop((0,0,V.width,y)); V.save(U+'vel.png'); print('vel',V.size)
