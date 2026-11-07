# vel.png: eind_r3 8x | eind_r4 8x, daaronder 1x licht/donker. potoo_8x.png: eind_r4 op 8x op wit.
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
z=8; W=64*z
def sp(path,bgc):
    t=Image.open(path).convert('RGBA'); bg=Image.new('RGBA',(64,64),bgc+(255,)); bg.alpha_composite(t); return bg.convert('RGB')
v=Image.new('RGB',(2*W+10,W+90),(255,255,255))
for i,p in enumerate((P+'eind_r3/potoo.png',P+'eind_r4/potoo.png')):
    v.paste(sp(p,(255,255,255)).resize((W,W),Image.NEAREST),(i*(W+10),0))
    v.paste(sp(p,(255,255,255)),(i*(W+10)+10,W+12)); v.paste(sp(p,(40,40,48)),(i*(W+10)+90,W+12))
v.save('vel.png')
sp(P+'eind_r4/potoo.png',(255,255,255)).resize((W,W),Image.NEAREST).save('potoo_8x.png')
