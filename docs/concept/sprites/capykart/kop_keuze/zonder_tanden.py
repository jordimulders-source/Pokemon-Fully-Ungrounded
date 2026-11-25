# Jordi 25 nov: "haal ze maar helemaal weg" (tanden) + morrillo "amper te zien, weet niet of dat klopt zo"
# Tandzone (x15-26, y30-33) terug naar de kale reductie (sprite/r17/kaal16.png), helderheid -> vachtramp van d.
from PIL import Image, ImageDraw
import numpy as np
d=Image.open('eindkeuring_dc/capykart_d.png'); P=d.getpalette(); D=np.array(d)
K=np.array(Image.open('sprite/r17/kaal16.png').convert('RGBA'))
lut=[(40,1),(85,2),(110,3),(128,4),(145,5),(999,6)]
def idx(l):
    for t,i in lut:
        if l<t: return i
A=D.copy()
for y in range(30,34):
    for x in range(15,27):
        if K[y,x,3]==0: A[y,x]=0
        else: A[y,x]=idx(int(K[y,x,:3].mean()))
# dubbele zwarte rij onder de kin: binnenste zwart -> donkerste bruin (1 px lijn blijft)
for y in range(31,34):
    for x in range(15,27):
        if A[y,x]==1 and A[y-1,x]==1 and A[y+1,x]!=0 and A[y,x-1]!=0: A[y,x]=2
var={}
# M1: morrillo duidelijker (lichtgrijs hart, donkergrijze rand), zelfde plek
M1=A.copy()
for (x,y),v in {(22,16):8,(23,16):7,(24,16):8,(21,17):8,(22,17):7,(23,17):7,(24,17):8}.items(): M1[y,x]=v
var['M1_morrillo_duidelijk']=M1
# M0: zonder morrillo (kale reductie terug)
M0=A.copy()
for y in (16,17):
    for x in range(20,26):
        if M0[y,x] in (7,8): M0[y,x]=idx(int(K[y,x,:3].mean()))
var['M0_zonder_morrillo']=M0
var['M_nu']=A
for k,B in var.items():
    im=Image.fromarray(B.astype('uint8'),'P'); im.putpalette(P); im.save(f'kop_keuze/{k}.png',transparency=0)
box=(8,9,40,38);W=14;w=(box[2]-box[0])*W;h=(box[3]-box[1])*W
vel=Image.new('RGBA',(len(var)*(w+12),h+150),(225,225,225,255)); dr=ImageDraw.Draw(vel)
for i,k in enumerate(var):
    im=Image.open(f'kop_keuze/{k}.png').convert('RGBA'); x=i*(w+12)
    cr=im.crop(box).resize((w,h),Image.NEAREST); vel.paste(cr,(x,16),cr); dr.text((x,2),k,fill=(0,0,0,255))
    one=im.resize((128,128),Image.NEAREST); vel.paste(one,(x,h+20),one)
vel.save('kop_keuze/zonder_tanden_vel.png')
