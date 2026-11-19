# r10 vel: A | B | r9 op 8x; kop-close-ups 12x naast het model; 1x/2x licht/donker. Schrijft ook sprite.png (A), sprite_zonder.png (B), A_8x.png, B_8x.png.
import numpy as np; from PIL import Image, ImageDraw
from reduce2 import PAL, save
OY,OX=1,17
M=Image.open('../../referenties/model.png').convert('RGB')
F,MX,MY=2.4,76.6,14.6
f=lambda v,o:(o+F*v)*5.12-0.42
def to64(a,path):
    c=np.zeros((64,64),'uint8'); c[OY:OY+a.shape[0],OX:OX+a.shape[1]]=a; save(c,path)
    return Image.open(path).convert('RGBA')   # opnieuw geopend: index 0 transparant
A=np.load('sprite_A.npy'); B=np.load('sprite_B.npy'); R=np.load('sprite_overlay.npy')
iA=to64(A,'sprite.png'); iB=to64(B,'sprite_zonder.png'); iR=to64(R,'_r9_tmp.png')
def x8(im,path):
    bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im); bg.convert('RGB').resize((512,512),Image.NEAREST).save(path)
x8(iA,'A_8x.png'); x8(iB,'B_8x.png')
def rgb(a,r0,r1,c0,c1,Z,bg=(255,255,255)):
    x=PAL[a[r0:r1,c0:c1]].astype('uint8'); x[a[r0:r1,c0:c1]==0]=bg
    return Image.fromarray(x).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST)
def mod(r0,r1,c0,c1,Z):
    return M.crop((round(f(c0,MX)),round(f(r0,MY)),round(f(c1,MX)),round(f(r1,MY)))).resize(((c1-c0)*Z,(r1-r0)*Z),Image.LANCZOS)
H,W=A.shape
row1=[rgb(A,0,H,0,W,8),rgb(B,0,H,0,W,8),rgb(R,0,H,0,W,8)]
caps1=['A r10 8x','B r10 (zonder krullen) 8x','r9 8x']
k=(2,16,12,30)
row2=[rgb(A,*k,12),mod(*k,12),rgb(B,*k,12),rgb(R,*k,12)]
caps2=['kop A 12x','model','kop B 12x','kop r9 12x']
def onbg(im,col,Z):
    bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im); return bg.convert('RGB').resize((64*Z,64*Z),Image.NEAREST)
row3=[onbg(iA,(255,255,255),1),onbg(iA,(40,40,48),1),onbg(iB,(255,255,255),1),onbg(iB,(40,40,48),1),M.resize((64,64),Image.LANCZOS),
      onbg(iA,(248,248,240),2),onbg(iA,(40,40,48),2),onbg(iB,(248,248,240),2),onbg(iB,(40,40,48),2)]
caps3=['A 1x','A 1x','B 1x','B 1x','model','A 2x','A 2x','B 2x','B 2x']
rows=[(row1,caps1),(row2,caps2),(row3,caps3)]
Wt=max(sum(t.width+12 for t in r) for r,_ in rows)+12; Ht=sum(max(t.height for t in r)+30 for r,_ in rows)+12
V=Image.new('RGB',(Wt,Ht),(225,225,225)); d=ImageDraw.Draw(V); y=8
for r,caps in rows:
    x=12
    for t,cp in zip(r,caps):
        d.text((x,y),cp,fill=(0,0,0)); V.paste(t,(x,y+14)); x+=t.width+12
    y+=max(t.height for t in r)+30
V.save('vel.png'); print(V.size)
