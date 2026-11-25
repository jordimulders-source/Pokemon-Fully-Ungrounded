# Jordi 25 nov: "de morrillo is te klein toch? als je hem zou draaien zou die alleen links van de neus zitten, klopt toch niet?"
# Morrillo als groter ovaal midden op de neusrug (boven de snuitplaat, tussen neus en oog), op basis van M0 (zonder oude morrillo).
from PIL import Image, ImageDraw
import numpy as np
b=Image.open('kop_keuze/M0_zonder_morrillo.png'); P=b.getpalette(); B=np.array(b)
vars={
 'N1_ovaal_5x3': {(20,19):8,(21,19):8,(22,19):8,(19,20):8,(20,20):7,(21,20):7,(22,20):8,(23,20):8,(20,21):8,(21,21):8,(22,21):8},
 'N2_ovaal_6x3': {(19,19):8,(20,19):8,(21,19):8,(22,19):8,(18,20):8,(19,20):7,(20,20):7,(21,20):7,(22,20):8,(23,20):8,(19,21):8,(20,21):8,(21,21):8,(22,21):8},
 'N3_donker_6x3': {(19,19):8,(20,19):8,(21,19):8,(22,19):8,(18,20):8,(19,20):8,(20,20):8,(21,20):8,(22,20):8,(23,20):8,(19,21):8,(20,21):8,(21,21):8,(22,21):8},
}
for k,px in vars.items():
    A=B.copy()
    for (x,y),v in px.items(): A[y,x]=v
    im=Image.fromarray(A.astype('uint8'),'P'); im.putpalette(P); im.save(f'kop_keuze/{k}.png',transparency=0)
box=(8,9,40,38);W=14;w=(box[2]-box[0])*W;h=(box[3]-box[1])*W
ks=list(vars)
vel=Image.new('RGBA',(len(ks)*(w+12),h+150),(225,225,225,255)); dr=ImageDraw.Draw(vel)
for i,k in enumerate(ks):
    im=Image.open(f'kop_keuze/{k}.png').convert('RGBA'); x=i*(w+12)
    cr=im.crop(box).resize((w,h),Image.NEAREST); vel.paste(cr,(x,16),cr); dr.text((x,2),k,fill=(0,0,0,255))
    one=im.resize((128,128),Image.NEAREST); vel.paste(one,(x,h+20),one)
vel.save('kop_keuze/morrillo_vel.png')
