# vel.py: A | B | model (BOX 4x4) op 4x; daaronder 1x op licht en donker: A, B, model, Magikarp, Feebas
import numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
LG=(214,222,214); DG=(40,44,52)
def rgba(p,c): b=Image.new('RGBA',(64,64),c+(255,)); b.alpha_composite(p.convert('RGBA')); return b.convert('RGB')
n=Image.open('natief.png').convert('RGB'); nx=OX+4*(xmin-x0); ny=OY+4*(ymin-y0)
big=Image.new('RGBA',(256+abs(nx)+4,256+abs(ny)+4),(0,0,0,0)); na=np.asarray(n.convert('RGBA')).copy(); na[np.asarray(n).min(2)>=215]=0
big.paste(Image.fromarray(na),(max(0,-nx),max(0,-ny))); bx,by=max(0,nx),max(0,ny)
mod=big.crop((bx,by,bx+256,by+256)).resize((64,64),Image.BOX)
def gen3(nm):
    p=Image.open(f'../../../../../graphics/pokemon/{nm}/anim_front_gba.png'); p=p.crop((0,0,64,64)); return p.convert('RGBA') if p.mode=='RGBA' else Image.fromarray(np.dstack([np.asarray(p.convert('RGB')),(np.asarray(p)!=0)*255]).astype('uint8'),'RGBA')
A=Image.open('blobfish_r5A.png'); B=Image.open('blobfish_r5B.png')
z=4; W=64*z
v=Image.new('RGB',(3*(W+10)+10,W+40+2*74+20),'white'); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate(((A,'A = r4 + (17,32)'),(B,'B = A + lichtronde'),(mod,'model (BOX 4x4)'))):
    v.paste(rgba(im,LG).resize((W,W),Image.NEAREST),(10+k*(W+10),24)); d.text((10+k*(W+10),8),t+' 4x',fill='black')
yy=W+44; d.text((10,yy-14),'1x: A | B | model | Magikarp | Feebas  (licht / donker)',fill='black')
for k,im in enumerate((A,B,mod,gen3('magikarp'),gen3('feebas'))):
    v.paste(rgba(im,LG),(10+k*70,yy)); v.paste(rgba(im,DG),(10+k*70,yy+70))
v.save('vel.png'); print(v.size)
