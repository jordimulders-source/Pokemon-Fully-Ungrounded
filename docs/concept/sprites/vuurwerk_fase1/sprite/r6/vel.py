# vel.png r5: r5 8x | r4 8x | model verkleind 8x | model 8x; close-ups 12x kop, handjes, pijl naast het model; 1x en 2x licht/donker.
import numpy as np; from PIL import Image, ImageDraw
from reduce2 import PAL, save
OY,OX=1,17
M=Image.open('../../referenties/model.png').convert('RGB')
F,MX,MY=2.4,76.6,14.6
f=lambda v,o:(o+F*v)*5.12-0.42
def to64(a,path):
    c=np.zeros((64,64),'uint8'); c[OY:OY+a.shape[0],OX:OX+a.shape[1]]=a; save(c,path)
    return Image.open(path).convert('RGBA')   # opnieuw geopend: index 0 transparant
A=np.load('sprite_A.npy'); R3=np.load('../r5/sprite_A.npy')
PAL5=PAL.copy(); PAL5[4]=[0xbe,0x30,0x7a]; PAL5[7]=[0xc2,0xb4,0x8e]
iA=to64(A,'sprite.png')
def rgb(a,r0,r1,c0,c1,Z,bg=(255,255,255),P=None):
    x=(PAL if P is None else P)[a[r0:r1,c0:c1]].astype('uint8'); x[a[r0:r1,c0:c1]==0]=bg
    return Image.fromarray(x).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
def mod(r0,r1,c0,c1,Z):
    return M.crop((round(f(c0,MX)),round(f(r0,MY)),round(f(c1,MX)),round(f(r1,MY)))).resize(((c1-c0)*Z,(r1-r0)*Z),Image.LANCZOS)
def modbox(r0,r1,c0,c1,Z):
    return M.crop((round(f(c0,MX)),round(f(r0,MY)),round(f(c1,MX)),round(f(r1,MY)))).resize((c1-c0,r1-r0),Image.BOX).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
H,W=A.shape
PAL3=PAL.copy(); PAL3[6]=[0xf0,0x76,0xa8]; PAL3[11]=[0xdc,0xa6,0x95]   # r3 had l=f076a8, t=dca695
def rgb3(a,r0,r1,c0,c1,Z):
    x=PAL3[a[r0:r1,c0:c1]].astype('uint8'); x[a[r0:r1,c0:c1]==0]=255
    return Image.fromarray(x).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
row1=[rgb(A,0,H,0,W,8),rgb(R3,0,H,0,W,8,P=PAL5),modbox(0,H,0,W,8),mod(0,H,0,W,8)]
caps1=['r6 8x','r5 8x','model verkleind (box) 8x','model 8x']
row2=[rgb(A,3,23,12,30,12),mod(3,23,12,30,12),rgb(R3,3,23,12,30,12,P=PAL5),rgb(A,12,22,0,18,12),mod(12,22,0,18,12),rgb(R3,12,22,0,18,12,P=PAL5)]
caps2=['kop r6 12x','model','r5','handjes r6 12x','model','r5']
row3=[rgb(A,36,62,2,19,10),mod(36,62,2,19,10),rgb(R3,36,62,2,19,10,P=PAL5),rgb(A,18,42,0,18,8),mod(18,42,0,18,8)]
caps3=['lus+staart r6 10x','model','r5','pijl 8x','model']
def onbg(im,col,Z):
    bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB').resize((64*Z,64*Z),Image.NEAREST)
row4=[onbg(iA,(255,255,255),1),onbg(iA,(40,40,48),1),M.resize((64,64),Image.LANCZOS),onbg(iA,(248,248,240),2),onbg(iA,(40,40,48),2)]
caps4=['1x','1x','model 1x','2x','2x']
rows=[(row1,caps1),(row2,caps2),(row3,caps3),(row4,caps4)]
Wt=max(sum(t.width+12 for t in r) for r,_ in rows)+12; Ht=sum(max(t.height for t in r)+30 for r,_ in rows)+12
V=Image.new('RGB',(Wt,Ht),(225,225,225)); d=ImageDraw.Draw(V); y=8
for r,caps in rows:
    x=12
    for t,cp in zip(r,caps):
        d.text((x,y),cp,fill=(0,0,0)); V.paste(t,(x,y+14)); x+=t.width+12
    y+=max(t.height for t in r)+30
V.save('vel.png'); print(V.size)
