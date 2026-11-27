# vel_keuze.png: 3 kleurschema's x 3 snavels op 6x, daaronder alles op 1x naast fase 2 v8, Spearow en Taillow
import numpy as np; from PIL import Image, ImageDraw
def rgbaP(pad,k,crop=None):
    im=Image.open(pad); a=np.array(im)[:64]; pal=im.getpalette(); o=np.zeros((64,64,4),'uint8')
    for i in set(a.ravel()):
        if i==0: continue
        o[a==i,:3]=pal[3*i:3*i+3]; o[a==i,3]=255
    im=Image.fromarray(o,'RGBA')
    if crop: im=im.crop(crop)
    return im.resize((im.width*k,im.height*k),Image.NEAREST)
k=6; C=(6,14,58,64); w=(C[2]-C[0])*k; h=(C[3]-C[1])*k
SN={'a':'a: oker steen','b':'b: a + facetranden','c':'c: VOORSTEL vuursteen + facetten'}
SC={'M':'modelkleuren','sA':'sA antraciet','sD':'sD roest'}
vel=Image.new('RGBA',(3*(w+10)+130,3*(h+24)+40+150),(236,236,236,255)); d=ImageDraw.Draw(vel)
for j,sn in enumerate(SN): d.text((130+j*(w+10),4),SN[sn],fill=(0,0,0))
for i,sc in enumerate(SC):
    d.text((4,24+i*(h+24)+h//2),SC[sc],fill=(0,0,0))
    for j,sn in enumerate(SN):
        vel.alpha_composite(rgbaP('kuiken_r2_%s_%s.png'%(sc,sn),k,C),(130+j*(w+10),20+i*(h+24)))
y=20+3*(h+24)+10; x=10
R='../../../../../../graphics/pokemon/'
for sc in SC:
    for sn in SN:
        vel.alpha_composite(rgbaP('kuiken_r2_%s_%s.png'%(sc,sn),1),(x,y)); x+=66
x+=14
for pad,nm in (('../../fase2/swaps_r1/v8.png','fase 2 v8'),(R+'spearow/anim_front_gba.png','Spearow'),(R+'taillow/anim_front_gba.png','Taillow')):
    vel.alpha_composite(rgbaP(pad,1),(x,y)); d.text((x,y+66),nm,fill=(0,0,0)); x+=70
d.text((10,y+66),'1x: M a b c | sA a b c | sD a b c',fill=(0,0,0))
vel.save('vel_keuze.png'); print(vel.size)
