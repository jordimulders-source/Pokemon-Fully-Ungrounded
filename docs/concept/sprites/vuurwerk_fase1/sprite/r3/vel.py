# vel.png: A 8x | B 8x | model verkleind 8x; close-ups 16x (kop, handjes, onderkant A/B) naast het model; 1x en 2x op licht en donker.
import numpy as np; from PIL import Image, ImageDraw
from reduce2 import PAL, save
OY,OX=1,17   # plaats in het 64x64-kader
M=Image.open('../../referenties/model.png').convert('RGB')
F,MX,MY=2.4,76.6,14.6
f=lambda v,o:(o+F*v)*5.12-0.42
def to64(a,path):
    c=np.zeros((64,64),'uint8'); c[OY:OY+a.shape[0],OX:OX+a.shape[1]]=a; save(c,path)
    im=Image.open(path); im=Image.open(path).convert('RGBA'); return im   # opnieuw geopend: index 0 transparant
A=np.load('sprite_A.npy'); B=np.load('sprite_B.npy')
iA=to64(A,'sprite.png'); iB=to64(B,'sprite_B.png')
def rgb(a,r0,r1,c0,c1,Z,bg=(255,255,255)):
    x=PAL[a[r0:r1,c0:c1]].astype('uint8'); x[a[r0:r1,c0:c1]==0]=bg
    return Image.fromarray(x).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
def mod(r0,r1,c0,c1,Z):
    return M.crop((round(f(c0,MX)),round(f(r0,MY)),round(f(c1,MX)),round(f(r1,MY)))).resize(((c1-c0)*Z,(r1-r0)*Z),Image.LANCZOS)
H,W=A.shape
tiles=[]
def modbox(r0,r1,c0,c1,Z):
    return M.crop((round(f(c0,MX)),round(f(r0,MY)),round(f(c1,MX)),round(f(r1,MY)))).resize((c1-c0,r1-r0),Image.BOX).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
row1=[rgb(A,0,H,0,W,8),rgb(B,0,H,0,W,8),modbox(0,H,0,W,8),mod(0,H,0,W,8)]
caps1=['A (vlam = bocht) 8x','B (compacte bocht) 8x','model verkleind (box) 8x','model 8x']
row2=[rgb(A,3,23,12,30,12),mod(3,23,12,30,12),rgb(A,11,22,0,16,12),mod(11,22,0,16,12)]
caps2=['kop 12x','model','handjes 12x','model']
row3=[rgb(A,44,62,3,15,12),rgb(B,44,62,3,15,12),mod(44,62,3,15,12),rgb(A,17,27,10,20,12),mod(17,27,10,20,12)]
caps3=['onderkant A','onderkant B','model','rechterarm (lijn weg)','model']
def onbg(im,col,Z):
    bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB').resize((64*Z,64*Z),Image.NEAREST)
row4=[onbg(iA,(255,255,255),1),onbg(iA,(40,40,48),1),onbg(iB,(255,255,255),1),onbg(iB,(40,40,48),1),onbg(iA,(248,248,240),2),onbg(iA,(40,40,48),2),onbg(iB,(248,248,240),2)]
caps4=['A 1x','A 1x','B 1x','B 1x','A 2x','A 2x','B 2x']
rows=[(row1,caps1),(row2,caps2),(row3,caps3),(row4,caps4)]
Wt=max(sum(t.width+12 for t in r) for r,_ in rows)+12; Ht=sum(max(t.height for t in r)+30 for r,_ in rows)+12
V=Image.new('RGB',(Wt,Ht),(225,225,225)); d=ImageDraw.Draw(V); y=8
for r,caps in rows:
    x=12
    for t,cp in zip(r,caps):
        d.text((x,y),cp,fill=(0,0,0)); V.paste(t,(x,y+14)); x+=t.width+12
    y+=max(t.height for t in r)+30
V.save('vel.png'); print(V.size)
