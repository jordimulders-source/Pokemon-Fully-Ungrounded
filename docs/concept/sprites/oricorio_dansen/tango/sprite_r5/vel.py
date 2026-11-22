# vel.png: r5 (A_donker) | model op dezelfde schaal | r5 B_lichter (8x); kop 12x naast Pom-Pom; poten 12x naast Baile-bronpoot en model; 1x op licht/donker/gevechtsgroen
import numpy as np; from PIL import Image, ImageDraw
G=(152,208,160)
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
A=rgba('tango.png'); B=rgba('tango_B_lichter.png')
# model op spriteschaal: kunstpixel = 1024/120 px -> 8x sprite = schaal 8/8.533; uitgelijnd op de bbox
m=Image.open('../model/gemini_r7.png').convert('RGB'); ma=np.asarray(m); ys,xs=np.where(ma.min(2)<200)
mc=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); o=np.asarray(A)[:,:,3]>0; sy,sx=np.where(o)
mc=mc.resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1)*8),Image.LANCZOS)
M=Image.new('RGB',(512,512),'white'); M.paste(mc,(sx.min()*8,sy.min()*8))
W=Image.new('RGB',(3*522,30+512+30+340+30+140),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(A,'white',8),'r5 tango.png (palet A_donker)'),(M,'model gemini_r7 (zelfde schaal en plek)'),(op(B,'white',8),'r5 variant B_lichter')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,10),t,fill='black')
y=572; d.text((4,y),'kop 12x: r5 | Pom-Pom (bron oog+snavel)',fill='black')
pom=rgba('../../../../../../graphics/pokemon/oricorio/pom_pom/anim_front.png').crop((0,0,64,64))
W.paste(op(A.crop((18,5,40,25)),'white',12),(0,y+20)); W.paste(op(pom.crop((21,11,43,31)),'white',12),(272,y+20))
d.text((560,y),'poten 12x: r5 | Baile frame 1 (bronvoet, rechts gespiegeld) | model',fill='black')
bai=rgba('../../../../../../graphics/pokemon/oricorio/anim_front.png').crop((0,0,64,64))
W.paste(op(A.crop((22,46,52,62)),'white',10),(560,y+20)); W.paste(op(bai.crop((18,46,34,62)),'white',10),(870,y+20))
mp=M.crop((22*8,46*8,52*8,62*8)).resize((300,160),Image.LANCZOS); W.paste(mp,(1040,y+20))
y=y+370; d.text((4,y),'1x: A op wit / donker / gevechtsgroen ; B op wit / donker / gevechtsgroen',fill='black')
for i,(im,bg) in enumerate([(A,'white'),(A,(40,40,48)),(A,G),(B,'white'),(B,(40,40,48)),(B,G)]):
    W.paste(op(im,bg,1),(i*80+(40 if i>2 else 0),y+20)); W.paste(op(im,bg,2),(560+i*140,y))
W.save('vel.png'); print(W.size)
