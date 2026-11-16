# vel.py: r9A | r10 | r10_plaatlicht | model op 8x; de bek op 12x (model, r9A, r10); 1x/2x op licht en donker naast Salamence en Lairon (Gen 3, frame 1).
from PIL import Image, ImageDraw
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
nat=Image.open(B+'sprite_r9/natief.png').convert('RGB')
def sp(f,bg):
    im=Image.open(f); im=im.crop((0,0,64,64)).convert('RGBA') if im.mode!='P' else im.crop((0,0,64,64))
    if im.mode=='P':
        p=im.getpalette(); im=im.convert('RGBA'); px=im.load(); t=tuple(p[:3])
        for y in range(64):
            for x in range(64):
                if px[x,y][:3]==t: px[x,y]=(0,0,0,0)
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def model(x0,y0,x1,y1,S):
    return nat.crop((2+3*x0,3*(y0-13),2+3*x1,3*(y1-13))).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS if False else Image.NEAREST)
L=(232,234,238); D=(40,40,48)
F=[(B+'sprite_r9/pitahaya2_r9A.png','r9A'),(B+'sprite_r10/pitahaya2_r10.png','r10'),(B+'sprite_r10/pitahaya2_r10_plaatlicht.png','r10 plaatlicht')]
X0,Y0,X1,Y1=4,28,64,64
r1=[sp(f,L).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*8,(Y1-Y0)*8),Image.NEAREST) for f,_ in F]+[model(X0,Y0,X1,Y1,8)]
l1=[n+' 8x' for _,n in F]+['model (natief, zelfde maat)']
bx0,by0,bx1,by1=4,40,24,58
r2=[model(bx0,by0,bx1,by1,12)]+[sp(f,L).crop((bx0,by0,bx1,by1)).resize(((bx1-bx0)*12,(by1-by0)*12),Image.NEAREST) for f,_ in F[:2]]
l2=['bek model 12x','bek r9A 12x','bek r10 12x']
refs=[(G+'salamence/anim_front.png','Salamence'),(G+'lairon/anim_front.png','Lairon')]
rows=[r1[:2],r1[2:],r2]; labels=[l1[:2],l1[2:],l2]
for bg,t in ((L,'licht'),(D,'donker')):
    r=[];l=[]
    for f,n in F[:2]+[F[2]]+refs: im=sp(f,bg); r+=[im,im.resize((128,128),Image.NEAREST)]; l+=[n+' 1x '+t,'2x']
    rows.append(r); labels.append(l)
W=max(sum(i.width+12 for i in r) for r in rows); H=sum(max(i.height for i in r)+26 for r in rows)
V=Image.new('RGB',(W,H),(250,250,250)); d=ImageDraw.Draw(V); y=0
for r,l in zip(rows,labels):
    x=0
    for im,t in zip(r,l): d.text((x+2,y+2),t,fill=(0,0,0)); V.paste(im,(x,y+14)); x+=im.width+12
    y+=max(i.height for i in r)+26
V.save(B+'sprite_r10/vel.png'); print(V.size)
