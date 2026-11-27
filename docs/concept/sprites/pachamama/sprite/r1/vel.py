# vel.py SPRITE UIT : sprite 8x | model op dezelfde schaal 8x; close-ups gezicht en armen 12x naast het model; 1x licht/donker
import sys; from PIL import Image, ImageDraw
SP=sys.argv[1]; UIT=sys.argv[2]
M=Image.open('../../referenties/gemini_gekozen_r4c.png').convert('RGB')
def mbox(y0,x0,y1,x1):  # spritecoordinaten -> modelpixels
  f=lambda n:4.25+5.12*n
  return (f(3*x0+3),f(3*y0-9),f(3*x1+3),f(3*y1-9))
pad=Image.new('RGB',(1100,1100),'white'); pad.paste(M,(38,60)); 
def mcrop(y0,x0,y1,x1,size):
  b=mbox(y0,x0,y1,x1); b=(b[0]+38,b[1]+60,b[2]+38,b[3]+60)
  return pad.crop(tuple(int(round(v)) for v in b)).resize(size,Image.LANCZOS)
sp=Image.open(SP).convert('RGBA')
def op(bg): b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(sp); return b.convert('RGB')
licht=op((232,240,232)); donker=op((40,44,56))
W=8*64*2+30
close=[('gezicht',12,31,19,41),('linkerarm',28,46,1,23),('rechterarm',25,46,22,50)]
hs=[ (y1-y0)*12 for _,y0,y1,x0,x1 in close]
H=512+20+sum(hs)+20*len(close)+20+64*3+30
vel=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(vel)
vel.paste(licht.resize((512,512),Image.NEAREST),(0,0)); vel.paste(mcrop(0,0,64,64,(512,512)),(542,0))
d.text((4,514),'sprite r1 8x',fill=(0,0,0)); d.text((546,514),'model (zelfde uitsnede en schaal)',fill=(0,0,0))
y=532
for (nm,y0,y1,x0,x1),h in zip(close,hs):
  w=(x1-x0)*12; c=licht.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)
  vel.paste(c,(0,y)); vel.paste(mcrop(y0,x0,y1,x1,(w,h)),(w+20,y)); d.text((4,y+h+2),nm+' 12x',fill=(0,0,0)); y+=h+20
vel.paste(licht,(0,y+10)); vel.paste(donker,(80,y+10))
vel.paste(licht.resize((128,128),Image.NEAREST),(160,y+10)); vel.paste(donker.resize((128,128),Image.NEAREST),(300,y+10))
d.text((4,y+80),'1x licht | 1x donker | 2x',fill=(0,0,0))
vel=vel.crop((0,0,W,y+150)); vel.save(UIT); print(UIT,vel.size)
