# vel.png r2: r2 (geel A) | r1 | model op 8x ; r2 geel B 8x ; 1x/2x licht en donker ; poten 12x naast de 4 Oricorio-vormen (Gen 3, frame 1)
import numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/'
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
rgba=lambda p: Image.open(p).convert('RGBA')
A=rgba('samba_A.png'); B=rgba('samba_B.png'); R1=rgba('../sprite_r1/samba.png')
nat=Image.open('natief.png').convert('RGB'); pad=Image.new('RGB',(nat.width+80,nat.height+80),'white'); pad.paste(nat,(40,40))
NY,NX,PY,PX=13,67,9,4
mod=pad.crop((40+NX-2*PX,40+NY-2*PY,40+NX-2*PX+128,40+NY-2*PY+128)).resize((512,512),Image.NEAREST)
W=Image.new('RGB',(3*522,30+512+30+512+30+260),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(A,'white',8),'r2, gele veren optie A (onderste veren, waar het model al geel heeft)'),(op(R1,'white',8),'r1'),(mod,'model gemini_r6, zelfde schaal')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,8),t,fill='black')
y=30+512+8; d.text((4,y),'r2 optie B (om en om bovenin: veer links en rechts achter de kuif + middelste rechts)',fill='black'); d.text((526,y),'1x en 2x, licht/donker: A boven, B onder',fill='black'); y+=22
W.paste(op(B,'white',8),(0,y))
for j,im in enumerate((A,B)):
    yy=y+j*150
    W.paste(op(im,(255,255,255),1),(530,yy)); W.paste(op(im,(40,40,48),1),(600,yy))
    W.paste(op(im,(255,255,255),2),(680,yy)); W.paste(op(im,(40,40,48),2),(820,yy))
y+=512+8; d.text((4,y),'poten 12x: samba r2 | Baile | Pom-Pom | Pa\'u | Sensu (standvoet samba = zwart klontje rij 60-61)',fill='black'); y+=22
crops=[(A,(12,46,36,63)),(rgba(G+'anim_front.png'),(16,45,40,62)),(rgba(G+'pom_pom/anim_front.png'),(24,44,48,61)),(rgba(G+'pau/anim_front.png'),(18,45,42,62)),(rgba(G+'sensu/anim_front.png'),(26,44,50,61))]
x=0
for im,b in crops:
    c=op(im.crop(b),(153,211,165),12); c=c.resize((c.width*2//3,c.height*2//3),Image.NEAREST); W.paste(c,(x,y)); x+=c.width+10
W.save('vel.png'); print(W.size)
