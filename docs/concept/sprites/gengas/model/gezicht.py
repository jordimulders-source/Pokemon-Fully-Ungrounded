# Schets gezichtsposities: ogen en grijns pixel voor pixel uit de Gen 3-Gengar op de kleurgids (64x64).
# Alleen een positieschets; de echte sprite tekent de maker.
from PIL import Image, ImageDraw; import numpy as np
D='docs/concept/sprites/gengas/model/'
g=Image.open('graphics/pokemon/gengar/anim_front.png'); gi=np.array(g)[:64]; pal=np.array(g.getpalette()[:48]).reshape(16,3)
X0,X1,Y0,Y1=16,39,24,41
face={}
FACE={1,2,3,4,5,6,7,14,15}
for y in range(Y0,Y1):
    for x in range(X0,X1):
        v=gi[y,x]
        nb=gi[max(0,y-1):y+2,max(0,x-1):x+2]
        if v in FACE or (v==13 and any(n in {1,2,3,4,5,6,7} for n in nb.flatten())):
            face[(x,y)]=v
REC={14:(70,22,40),13:(96,36,58),15:(24,10,16)}   # Gengar-paars rond ogen/mond -> Gengas-tinten
k=np.asarray(Image.open(D+'kleurgids_64.png').convert('RGB')).astype(int)
R,G,B=k[...,0],k[...,1],k[...,2]
old=((R>200)&(G<140))|((R>200)&(G>200)&(B>200)&(k.min(2)<250))  # rood oog / witte tanden in het model
old[:26]=False; old[46:]=False
ys,xs=np.where(old)
bx0,bx1,by0,by1=xs.min()-1,xs.max()+2,ys.min()-2,ys.max()+2
base=k.copy()
# oud gezicht weg: per rij vullen met de kleur net rechts van het gezicht (schets)
for y in range(by0,by1):
    c=k[y,bx1+1]; xl=next(x for x in range(64) if k[y,x].min()<235)   # buitenrand van de bol
    for x in range(max(bx0,xl+1),bx1): base[y,x]=c
print('oud gezicht',bx0,bx1,by0,by1)
def plak(dx,dy):
    o=base.copy()
    for (x,y),v in face.items():
        o[y+dy,x+dx]=REC.get(v,pal[v])
    return o
opts={'A: plek uit Gemini':(bx0-X0+1,by0-Y0),'B: 3 px naar het midden':(bx0-X0+4,by0-Y0),'C: 6 px naar het midden':(bx0-X0+7,by0-Y0)}
T=Image.new('RGB',(3*540,600),'white'); d=ImageDraw.Draw(T)
for i,(nm,(dx,dy)) in enumerate(opts.items()):
    im=Image.fromarray(plak(dx,dy).astype('uint8'))
    T.paste(im.resize((512,512),Image.NEAREST),(i*540+10,40)); T.paste(im,(i*540+10,540))
    d.text((i*540+10,12),nm,fill=(0,0,0))
T.save(D+'gezicht_opties.png'); print(opts)
