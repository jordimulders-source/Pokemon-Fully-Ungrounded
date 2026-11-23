# zoom.py SPRITE y0 y1 x0 x1 UIT : sprite-uitsnede (64x64-coord.) op 16x naast model in dezelfde uitsnede
import sys; from PIL import Image, ImageDraw
SP,y0,y1,x0,x1,OUT=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
Z=16
sp=Image.open(SP).convert('RGBA').crop((x0,y0,x1,y1)); w,h=sp.size
bg=Image.new('RGB',(w,h),(200,230,200)); bg.paste(sp,(0,0),sp); a=bg.resize((w*Z,h*Z),Image.NEAREST)
m=Image.open('../r12.png').convert('RGB'); pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
p=10.24; ph=10.25; s=88/63
def X(c): return 200+ph+(12+(c-10)*s)*p
def Y(r): return 200+ph+(5+r*s)*p
b=pad.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).resize((w*Z,h*Z),Image.LANCZOS)
o=Image.new('RGB',(2*w*Z+10,h*Z+14),(255,255,255)); o.paste(a,(0,14)); o.paste(b,(w*Z+10,14)); d=ImageDraw.Draw(o)
for i in range(x0,x1,2): d.text(((i-x0)*Z+2,1),str(i),fill=(255,0,0))
for j in range(y0,y1,2): d.text((w*Z+1,14+(j-y0)*Z),str(j),fill=(255,0,0))
for k in range(w+1): d.line([(k*Z,14),(k*Z,14+h*Z)],fill=(170,170,220))
for k in range(h+1): d.line([(0,14+k*Z),(w*Z,14+k*Z)],fill=(170,170,220))
o.save(OUT)
