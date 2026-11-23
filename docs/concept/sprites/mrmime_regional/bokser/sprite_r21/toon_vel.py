# r21: studie_v.png (echte sprites 8x), v_varianten_16x.png (r20 | A | B | C, rode stip = punt (30,33)) + studie-uitsneden,
# bokser_8x.png, vel.png
from PIL import Image, ImageDraw
import os
G='../../../../../../graphics/pokemon/'
bg=(200,230,200,255)
def L(p):
    if not os.path.exists(p): p=p.replace('anim_front_gba','anim_front')
    return Image.open(p).convert('RGBA').crop((0,0,64,64))
def Z(i,z): return i.resize((i.width*z,i.height*z),Image.NEAREST)
def rij(ims,lab,z,pad=8):
    ims=[Z(i,z) for i in ims]; H=max(i.height for i in ims)
    W=Image.new('RGBA',(sum(i.width+pad for i in ims),H+14),bg); d=ImageDraw.Draw(W); X=0
    for i,t in zip(ims,lab): W.paste(i,(X,0),i); d.text((X+3,H+2),t,fill=(0,0,0,255)); X+=i.width+pad
    return W
ST=[('throh',(12,14,52,54),'Throh: verre baan kort/steil, nabije lang/flauw'),('sawk',(14,12,54,52),'Sawk: kraag 2 px, punt onder gezicht'),
    ('blaziken',(12,6,52,46),'Blaziken: gevulde V-borst'),('swellow',(12,8,52,48),'Swellow: gevulde V-keel')]
studie=[L(G+n+'/anim_front_gba.png').crop(c) for n,c,_ in ST]
rij(studie,[t for *_,t in ST],8).save('studie_v.png')
C=(16,18,46,38)
vs=[('../sprite_r20/bokser.png','r20'),('bokser.png','A gevuld (hoofd)'),('var/v_B_banen.png','B banen'),('var/v_C_steil.png','C steil')]
ims=[]
for p,t in vs:
    i=Z(L(p).crop(C),16); d=ImageDraw.Draw(i); x=(30-C[0])*16+8; y=(33-C[1])*16+8; d.rectangle((x-8,y-8,x+7,y+7),outline=(220,0,0,255)); ims.append(i)
top=rij([i.resize((i.width//16,i.height//16),Image.NEAREST) for i in ims],[t for _,t in vs],16)
# rode stip terugzetten op de 16x-rij
d=ImageDraw.Draw(top); X=0
for i in ims: x=X+(30-C[0])*16+8; y=(33-C[1])*16+8; d.rectangle((x-8,y-8,x+7,y+7),outline=(220,0,0,255)); X+=i.width+8
onder=rij([s.crop((0,0,40,40)) for s in studie],[n for n,*_ in ST],8)
W=Image.new('RGBA',(max(top.width,onder.width),top.height+onder.height+8),bg); W.paste(top,(0,0)); W.paste(onder,(0,top.height+8)); W.save('v_varianten_16x.png')
Z(L('bokser.png'),8).save('bokser_8x.png')
rij([L('bokser.png'),L('var/v_B_banen.png'),L('var/v_C_steil.png'),L('../sprite_r20/bokser.png'),L('../sprite_r18/bokser.png'),L(G+'mr_mime/anim_front_gba.png'),L(G+'mr_mime/galar/front.png')],
    ['r21 A','r21 B','r21 C','r20','r18','Mr. Mime','Galar'],5).save('vel.png')
