# vel_keuze.png: 3 lijfschema's x (2 gezichten x 2 snavels) op 6x, gezichtszone-overlay, 1x naast fase 2 r4, Spearow, Taillow
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
KOL=[('i','a'),('i','c'),('ii','a'),('ii','c')]
KN={'i':'gezicht i: warm lichtbruin (model)','ii':'gezicht ii: roest-tan (fase 2)','a':'snavel a oker','c':'snavel c VOORSTEL vuursteen'}
SC={'M':'lijf M','sA':'lijf sA antraciet','sD':'lijf sD roest'}
W=4*(w+10)+100; vel=Image.new('RGBA',(W+w+20,3*(h+24)+40+110),(236,236,236,255)); d=ImageDraw.Draw(vel)
for j,(gz,sn) in enumerate(KOL): d.text((100+j*(w+10),4),KN[gz],fill=(0,0,0)); d.text((100+j*(w+10),14),KN[sn],fill=(0,0,0))
for i,sc in enumerate(SC):
    d.text((4,30+i*(h+24)+h//2),SC[sc],fill=(0,0,0))
    for j,(gz,sn) in enumerate(KOL):
        vel.alpha_composite(rgbaP('kuiken_r3_%s_%s_%s.png'%(sc,gz,sn),k,C),(100+j*(w+10),30+i*(h+24)))
# overlay gezichtszone
F=np.load('face.npy'); base=rgbaP('kuiken_r3_M_i_a.png',k,C); ov=np.zeros((64,64,4),'uint8'); ov[F]=(0,200,255,150)
ovi=Image.fromarray(ov,'RGBA').crop(C).resize((w,h),Image.NEAREST); base.alpha_composite(ovi)
vel.alpha_composite(base,(W,30)); d.text((W,4),'gezichtszone (blauw) = eigen groep',fill=(0,0,0))
y=30+3*(h+24)+10; x=10; R='../../../../../../graphics/pokemon/'
for sc in SC:
    for gz,sn in KOL:
        vel.alpha_composite(rgbaP('kuiken_r3_%s_%s_%s.png'%(sc,gz,sn),1),(x,y)); x+=64
    x+=10
for pad,nm in (('../../fase2/sprite_bijl_r4/terreurvogel_bijl_r4.png','fase 2 r4'),(R+'spearow/anim_front_gba.png','Spearow'),(R+'taillow/anim_front_gba.png','Taillow')):
    vel.alpha_composite(rgbaP(pad,1),(x,y)); d.text((x,y+66),nm,fill=(0,0,0)); x+=70
d.text((10,y+66),'1x per rij: i-a i-c ii-a ii-c (M | sA | sD)',fill=(0,0,0))
vel.save('vel_keuze.png'); print(vel.size)
