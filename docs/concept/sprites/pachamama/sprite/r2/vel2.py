# vel r2: r2 | r1 | model op 8x; gezicht+kap 12x naast het model (met raster); ogen: model natief 30x met spriteraster
# en de lichte iris omlijnd (cyaan), naast het spriteoog op dezelfde schaal.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image, ImageDraw
M=Image.open('../../referenties/gemini_gekozen_r4c.png').convert('RGB')
pad=Image.new('RGB',(1100,1100),'white'); pad.paste(M,(38,60))
def mcrop(y0,x0,y1,x1,size):
  f=lambda n:4.25+5.12*n
  b=(f(3*x0+3)+38,f(3*y0-9)+60,f(3*x1+3)+38,f(3*y1-9)+60)
  return pad.crop(tuple(int(round(v)) for v in b)).resize(size,Image.LANCZOS)
def op(fn):
  s=Image.open(fn).convert('RGBA'); b=Image.new('RGBA',(64,64),(232,240,232,255)); b.alpha_composite(s); return b.convert('RGB')
r2=op('pachamama_r2.png'); r1=op('../r1/pachamama_r1.png')
def raster(img,z,x0,y0):
  d=ImageDraw.Draw(img)
  for k in range(img.size[0]//z+1): d.line([(k*z,0),(k*z,img.size[1])],fill=(255,0,0) if (x0+k)%5==0 else (150,150,150))
  for k in range(img.size[1]//z+1): d.line([(0,k*z),(img.size[0],k*z)],fill=(255,0,0) if (y0+k)%5==0 else (150,150,150))
  return img
W=512*3+40; vel=Image.new('RGB',(W,2000),'white'); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((r2,'r2'),(r1,'r1'))): vel.paste(im.resize((512,512),Image.NEAREST),(i*532,0)); d.text((i*532+4,514),t+' 8x',fill=(0,0,0))
vel.paste(mcrop(0,0,64,64,(512,512)),(1064,0)); d.text((1068,514),'model',fill=(0,0,0))
y=540; y0,y1,x0,x1=8,30,18,44; Z=12; w=(x1-x0)*Z; h=(y1-y0)*Z
vel.paste(raster(r2.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),Z,x0,y0),(0,y))
vel.paste(raster(r1.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),Z,x0,y0),(w+15,y))
vel.paste(raster(mcrop(y0,x0,y1,x1,(w,h)),Z,x0,y0),(2*w+30,y))
d.text((4,y+h+2),'kap + gezicht 12x: r2 | r1 | model (raster = spritepixels, rood elke 5)',fill=(0,0,0)); y+=h+25
# ogen
nat=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); L=lum(nat)
ey0,ey1,ex0,ex1=17,21,23,33; Z2=30
cr=nat[3*ey0-9:3*ey1-9,3*ex0+3:3*ex1+3]; Lc=L[3*ey0-9:3*ey1-9,3*ex0+3:3*ex1+3]
img=Image.fromarray(cr.astype('uint8')).resize((cr.shape[1]*Z2//3*3//3*1,cr.shape[0]*Z2//3*3//3),Image.NEAREST) if False else Image.fromarray(cr.astype('uint8')).resize((cr.shape[1]*10,cr.shape[0]*10),Image.NEAREST)
dd=ImageDraw.Draw(img)
# lichte iris: modelpixels L 95-175 die binnen de oogwit-rij liggen (rij 48-50 natief) tussen wit in
for yy in range(cr.shape[0]):
  for xx in range(cr.shape[1]):
    ny,nx=3*ey0-9+yy,3*ex0+3+xx
    if 95<=L[ny,nx]<=175 and 47<=ny<=50 and ((L[ny,nx-3:nx]>225).any() or (L[ny,nx+1:nx+4]>225).any()) and ((75<=nx<=80) or (90<=nx<=99)):
      dd.rectangle([xx*10,yy*10,xx*10+9,yy*10+9],outline=(0,255,255),width=2)
for k in range(ex1-ex0+1): dd.line([(k*30,0),(k*30,img.size[1])],fill=(255,0,0))
for k in range(ey1-ey0+1): dd.line([(0,k*30),(img.size[0],k*30)],fill=(255,0,0))
sp=raster(r2.crop((ex0,ey0,ex1,ey1)).resize(((ex1-ex0)*30,(ey1-ey0)*30),Image.NEAREST),30,ex0,ey0)
vel.paste(sp,(0,y)); vel.paste(img,(sp.size[0]+15,y))
d.text((4,y+img.size[1]+2),'ogen 30x (rijen %d-%d, kolommen %d-%d): r2 | model natief; rood = spritepixel, cyaan = lichte iris van het model'%(ey0,ey1-1,ex0,ex1-1),fill=(0,0,0)); y+=img.size[1]+25
vel.paste(r2,(0,y)); vel.paste(r2.resize((128,128),Image.NEAREST),(80,y))
dk=Image.open('pachamama_r2.png').convert('RGBA'); b=Image.new('RGBA',(64,64),(40,44,56,255)); b.alpha_composite(dk)
vel.paste(b.convert('RGB'),(230,y)); vel.paste(b.convert('RGB').resize((128,128),Image.NEAREST),(310,y))
d.text((4,y+132),'1x en 2x op licht en donker',fill=(0,0,0)); y+=150
vel.crop((0,0,W,y)).save('vel.png'); print('vel.png',W,y)
