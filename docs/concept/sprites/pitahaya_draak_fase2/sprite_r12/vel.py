# vel.py: eind | r12 op 8x naast Lairon en Swampert (Gen 3, frame 1, 8x); daaronder 1x/2x op licht en donker.
from PIL import Image, ImageDraw
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'; G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def sp(f,bg):
    im=Image.open(f).crop((0,0,64,64)); p=im.getpalette(); t=tuple(p[:3]); im=im.convert('RGBA'); px=im.load()
    for y in range(64):
        for x in range(64):
            if px[x,y][:3]==t: px[x,y]=(0,0,0,0)
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
L=(232,234,238); D=(40,40,48)
F=[(B+'eind/pitahaya2_eind_plaatlicht.png','eind'),(B+'sprite_r12/pitahaya2_r12.png','r12'),(G+'lairon/anim_front.png','Lairon'),(G+'swampert/anim_front.png','Swampert')]
rows=[[sp(f,L).resize((512,512),Image.NEAREST) for f,_ in F[:2]],[sp(f,L).resize((512,512),Image.NEAREST) for f,_ in F[2:]]]
labels=[[n+' 8x' for _,n in F[:2]],[n+' 8x' for _,n in F[2:]]]
for bg,t in ((L,'licht'),(D,'donker')):
    r=[];l=[]
    for f,n in F: im=sp(f,bg); r+=[im,im.resize((128,128),Image.NEAREST)]; l+=[n+' 1x '+t,'2x']
    rows.append(r); labels.append(l)
W=max(sum(i.width+12 for i in r) for r in rows); H=sum(max(i.height for i in r)+26 for r in rows)
V=Image.new('RGB',(W,H),(250,250,250)); d=ImageDraw.Draw(V); y=0
for r,l in zip(rows,labels):
    x=0
    for im,t in zip(r,l): d.text((x+2,y+2),t,fill=(0,0,0)); V.paste(im,(x,y+14)); x+=im.width+12
    y+=max(i.height for i in r)+26
V.save(B+'sprite_r12/vel.png')
