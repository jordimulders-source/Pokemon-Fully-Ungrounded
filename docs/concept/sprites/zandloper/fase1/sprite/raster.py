# Model met spriteraster erover + sprite ernaast (per regio), om per cel te vergelijken.
import sys; from gemeen import *; from PIL import ImageDraw
SP=sys.argv[1]; i0,j0,i1,j1=map(int,sys.argv[2].split(',')); OUT=sys.argv[3]; Z=28
S=np.array(Image.open(SP)) if SP.endswith('.png') else np.load(SP)
M=Image.open('../model.png').convert('RGB')
x0,y0=s2m(i0,j0); x1,y1=s2m(i1,j1)
m=M.crop((int(x0),int(y0),int(x1),int(y1))).resize(((i1-i0)*Z,(j1-j0)*Z),Image.NEAREST)
d=ImageDraw.Draw(m)
for i in range(i1-i0+1): d.line([(i*Z,0),(i*Z,m.height)],fill=(255,0,0))
for j in range(j1-j0+1): d.line([(0,j*Z),(m.width,j*Z)],fill=(255,0,0))
for i in range(i1-i0): d.text((i*Z+2,2),str((i0+i)%100),fill=(255,0,0))
for j in range(j1-j0): d.text((2,j*Z+12),str(j0+j),fill=(255,0,0))
s=rgba(S[j0:j1,i0:i1],(255,255,255,255)).convert('RGB').resize(m.size,0); d2=ImageDraw.Draw(s)
for i in range(i1-i0+1): d2.line([(i*Z,0),(i*Z,m.height)],fill=(200,200,200))
for j in range(j1-j0+1): d2.line([(0,j*Z),(m.width,j*Z)],fill=(200,200,200))
im=Image.new('RGB',(m.width*2+10,m.height),'white'); im.paste(m,(0,0)); im.paste(s,(m.width+10,0)); im.save(OUT)
