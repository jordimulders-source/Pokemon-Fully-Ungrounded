# Alleen om de spritegrootte te kiezen: kale reductie van het natieve model op drie breedtes (geen sprite).
import numpy as np
from PIL import Image
n=Image.open('sprite_r1/natief.png').convert('RGB')
a=np.array(n).astype(int)
bg=(a.min(-1)>235)
ys,xs=np.where(~bg); box=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
crop=n.crop(box); W,H=crop.size
cols=[]
for w in (42,50,60):
    h=round(H*w/W)
    small=crop.resize((w,h),Image.BOX)
    pal=crop.quantize(16,method=Image.MEDIANCUT)
    q=small.quantize(palette=pal,dither=Image.NONE).convert('RGB')
    m=np.array(crop.convert('L').point(lambda v:255 if v<235 else 0).resize((w,h),Image.BOX))>110
    qa=np.array(q); qa[~m]=255
    tile=Image.new('RGB',(64,64),'white'); tile.paste(Image.fromarray(qa.astype('uint8')),((64-w)//2,64-h-2))
    cols.append((w,int(m.sum()),tile))
S=8
vel=Image.new('RGB',(64*S*3+40,64*S+30),'white')
from PIL import ImageDraw
d=ImageDraw.Draw(vel)
for i,(w,area,t) in enumerate(cols):
    vel.paste(t.resize((64*S,64*S),Image.NEAREST),(i*(64*S+20),30))
    d.text((i*(64*S+20)+4,8),f'{w} px breed, {area} px oppervlak (64x64-kader)',fill='black')
vel.save('maat/maten.png'); print([(w,a) for w,a,_ in cols], W,H)
