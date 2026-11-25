# Kopvarianten op eindkeuring_dc/capykart_c.png: snuit-philtrum en oog (E1 r7/V2, E2 model, E3 Capybarrel af)
from PIL import Image
import numpy as np
c=Image.open('eindkeuring_dc/capykart_c.png'); P=c.getpalette(); C=np.array(c)
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/a7fe546e-3d30-5931-9ef7-2a50828a120c/scratchpad/'
base=C.copy()
# snuit: philtrum rood (3) -> donkerste bruin (2)
for y in range(24,30):
    if base[y,18]==3: base[y,18]=2
# oogzone leegmaken: donkere tinten in x28-33,y15-22 -> gezicht midden (5), behalve buitenlijn
alpha=C>0
for y in range(15,23):
    for x in range(28,34):
        nb=[alpha[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if base[y,x] in (1,2,3) and all(nb): base[y,x]=5
def put(A,y0,x0,rows):
    for dy,r in enumerate(rows):
        for dx,v in enumerate(r):
            if v is not None: A[y0+dy,x0+dx]=v
var={}
# E1: oog + wenkbrauw van r7 (door Jordi gekozen V2), r7-kleuren 4->4, 3->5
E1=base.copy(); put(E1,16,29,[[4,4,4],[4,4,5],[1,1,1],[4,1,1],[5,1,1]]); var['E1_r7']=E1
# E2: modeloog (amandel, glanspixel)
E2=base.copy(); put(E2,18,29,[[4,4,4,None],[3,1,1,3],[1,9,1,3],[None,1,3,None]]); var['E2_model']=E2
# E3: Capybarrel-af-oog exact (rijen 32-36, x22-26 van capybarrel), kleuren omgezet
cb=np.array(Image.open('../capybarrel/af/capybarrel.png'))
mp={1:1,2:2,3:6,4:5,5:4}
blk=[[mp.get(int(cb[y,x])) if int(cb[y,x]) in (1,2) else None for x in range(22,27)] for y in range(32,37)]
E3=base.copy(); put(E3,16,28,blk); var['E3_capybarrel']=E3
out={}
for k,A in var.items():
    im=Image.fromarray(A.astype('uint8'),'P'); im.putpalette(P); im.save(f'kop_keuze/{k}.png',transparency=0); out[k]=im
# vel
m=Image.open(S+'model64.png').convert('RGBA')
box=(10,9,42,34);W=12;w=(box[2]-box[0])*W;h=(box[3]-box[1])*W
items=[('model',m)]+[(k,Image.open(f'kop_keuze/{k}.png').convert('RGBA')) for k,v in out.items()]+[('c (nu)',c.convert('RGBA'))]
vel=Image.new('RGBA',(len(items)*(w+12),h+150),(225,225,225,255))
from PIL import ImageDraw
d=ImageDraw.Draw(vel)
for i,(k,im) in enumerate(items):
    x=i*(w+12); cr=im.crop(box).resize((w,h),Image.NEAREST); vel.paste(cr,(x,18),cr); d.text((x,2),k,fill=(0,0,0,255))
    one=im.resize((128,128),Image.NEAREST); vel.paste(one,(x,h+20),one)
vel.save('kop_keuze/vel.png')
