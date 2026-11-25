# Jordi 25 nov: "tanden moeten verder naar links" -> tandenblok (x17-23, y30-33) 1 en 2 px naar links, varianten L1/L2
from PIL import Image
import numpy as np
d=Image.open('eindkeuring_dc/capykart_d.png'); P=d.getpalette(); D=np.array(d)
for s in (1,2):
    A=D.copy(); blk=D[30:34,17:24].copy()
    # vrijgekomen rechts: kin/nek
    A[30,24-s:24]=4; A[31:34,24-s:24]=3
    A[30:34,17-s:24-s]=blk
    # buitenlijn links van de tanden dicht
    for y in range(31,34):
        if A[y,16-s]==0: A[y,16-s]=0
    A[34,15-s+1:17]=np.where(A[34,15-s+1:17]==0,1,A[34,15-s+1:17])
    im=Image.fromarray(A.astype('uint8'),'P'); im.putpalette(P); im.save(f'kop_keuze/tanden_L{s}.png',transparency=0)
    Image.open(f'kop_keuze/tanden_L{s}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'kop_keuze/tanden_L{s}_8x.png')
# vel
from PIL import ImageDraw
box=(8,14,34,40);W=14;w=(box[2]-box[0])*W;h=(box[3]-box[1])*W
names=[('d','eindkeuring_dc/capykart_d.png'),('L1','kop_keuze/tanden_L1.png'),('L2','kop_keuze/tanden_L2.png')]
vel=Image.new('RGBA',(3*(w+12),h+150),(225,225,225,255)); dr=ImageDraw.Draw(vel)
for i,(k,f) in enumerate(names):
    im=Image.open(f).convert('RGBA'); x=i*(w+12)
    cr=im.crop(box).resize((w,h),Image.NEAREST); vel.paste(cr,(x,16),cr); dr.text((x,2),k,fill=(0,0,0,255))
    one=im.resize((128,128),Image.NEAREST); vel.paste(one,(x,h+20),one)
vel.save('kop_keuze/tanden_vel.png')
