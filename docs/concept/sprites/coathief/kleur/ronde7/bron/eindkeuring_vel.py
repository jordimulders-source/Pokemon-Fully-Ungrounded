from PIL import Image, ImageDraw
import sys
R='/home/user/Pokemon-Fully-Ungrounded/'
C=R+'docs/concept/sprites/coathief/'
sp=Image.open(C+'kleur/ronde7/coathief.png').convert('RGBA')
ol=Image.open(R+'docs/concept/sprites/olinguito_v2/af/olinguito.png').convert('RGBA')
names=['linoone','zigzagoon','mightyena','poochyena','zangoose','sandslash','raticate','furret','persian','houndoom','absol','sneasel','ninetales']
refs=[]
for n in names:
    src=Image.open(R+f'graphics/pokemon/{n}/anim_front.png').crop((0,0,64,64))
    im=src.convert('RGBA')
    if src.mode=='P':
        px=src.load(); a=Image.new('L',(64,64))
        ap=a.load()
        for yy in range(64):
            for xx in range(64): ap[xx,yy]=0 if px[xx,yy]==0 else 255
        im.putalpha(a)
    refs.append((n,im))
LB=(152,208,160,255); DB=(40,40,48,255)
def comp(im,bg,z):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.resize((im.width*z,im.height*z),Image.NEAREST)
W=1400; Hh=1450
V=Image.new('RGBA',(W,Hh),(235,235,235,255)); d=ImageDraw.Draw(V)
d.text((10,8),'Coathief kleur ronde 7 - verse eindkeuring: 8x / 3x / 1x op licht en donker',fill=(0,0,0,255))
V.paste(comp(sp,LB,8),(10,30)); V.paste(comp(sp,DB,8),(540,30))
x=1070
V.paste(comp(sp,LB,3),(x,30)); V.paste(comp(sp,DB,3),(x,230))
V.paste(comp(sp,LB,1),(x+200,30)); V.paste(comp(sp,DB,1),(x+200,100))
V.paste(comp(ol,LB,1),(x+200,170)); d.text((x+200,240),'olinguito 1x',fill=(0,0,0,255))
# row 3x: coathief + olinguito + refs on light
y=580; d.text((10,y),'3x op licht: coathief, olinguito, 13 Gen 3-sprites',fill=(0,0,0,255)); y+=16
allx=[('coathief',sp),('olinguito',ol)]+refs
for i,(n,im) in enumerate(allx):
    cx=10+(i%7)*198; cy=y+(i//7)*215
    V.paste(comp(im,LB,3),(cx,cy)); d.text((cx,cy+194),n,fill=(0,0,0,255))
y=y+3*215
d.text((10,y),'1x op licht en donker (zelfde volgorde)',fill=(0,0,0,255)); y+=16
for i,(n,im) in enumerate(allx):
    V.paste(comp(im,LB,1),(10+i*70,y)); V.paste(comp(im,DB,1),(10+i*70,y+70))
V.save(C+'kleur/ronde7/eindkeuring_vel.png')
# uitsnede met FAIL-zones (8x), licht en donker
V2=Image.new('RGBA',(W,Hh+260),(235,235,235,255)); V2.paste(V,(0,0)); d2=ImageDraw.Draw(V2)
y0=Hh-35; d2.text((10,y0-14),'Uitsnede x 12-56, y 44-63 op 8x. Rood: open randen (schaduwtint 6 onder de buik). Oranje: glans c op de buitenrand van de klauwen. Geel: rechte buitenranden hangende klauwen.',fill=(0,0,0,255))
box=(12,44,56,64)
for k,bg in enumerate([LB,DB]):
    c=comp(sp.crop(box),bg,8); ox=10+k*(c.width+20); V2.paste(c,(ox,y0))
    def mark(px,col):
        for (x,y) in px:
            X=ox+(x-box[0])*8; Y=y0+(y-box[1])*8; d2.rectangle([X,Y,X+7,Y+7],outline=col,width=2)
    mark([(32,47),(33,47),(43,51),(44,51)],(230,0,0,255))
    mark([(25,59),(25,61)],(255,140,0,255))
    mark([(19,54),(18,55),(18,56),(17,57),(17,58),(16,59),(16,60),(21,55),(21,56),(21,57),(20,58),(20,59),(20,60)],(255,230,0,255))
V2.save(C+'kleur/ronde7/eindkeuring_vel.png')
