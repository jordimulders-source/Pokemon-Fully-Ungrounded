# Gnomad r9: snoromlijning rechts van donkerroze (6) naar de snor-selout e; alleen de snorzone, rest diff 0 t.o.v. r8.
from PIL import Image, ImageDraw
import sys
E=0xe
PIX=[(23,32),(26,32),(27,33),(28,33),(29,34),(29,35),(30,36),(31,36),(32,36),(32,37),(31,38),
     (26,38),(21,38),(20,37),(19,36),(18,37)]+[(x,39) for x in range(22,31)]
BLACK=[]  # eventueel terug naar zwart
BOX=(18,32,33,39)
im=Image.open('../sprite_r8/gnomad.png'); a=im.load(); out=im.copy(); o=out.load()
for x,y in PIX: assert a[x,y]==6,(x,y,a[x,y]); o[x,y]=E
for x,y in BLACK: o[x,y]=1
out.save('gnomad.png')
ch=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=o[x,y]]
assert all(BOX[0]<=x<=BOX[2] and BOX[1]<=y<=BOX[3] for x,y in ch)
op=[p for p in ((x,y) for y in range(64) for x in range(64)) if a[p]]
assert all(o[p] for p in op) and sum(1 for y in range(64) for x in range(64) if o[x,y])==len(op)
b=sum(o[p]==1 for p in op)
print(len(ch),'gewijzigd, alles binnen snorzone',BOX,'; zwart %d/%d=%.1f%%'%(b,len(op),100*b/len(op)))
k=8; A=im.convert('RGB').resize((512,512),0); R=out.convert('RGB').resize((512,512),0); D=R.copy(); d=ImageDraw.Draw(D)
for x,y in ch: d.rectangle([x*k,y*k,x*k+k-1,y*k+k-1],outline=(0,255,255),width=2)
V=Image.new('RGB',(1568,512),'white'); V.paste(A,(0,0)); V.paste(R,(528,0)); V.paste(D,(1056,0)); V.save('vergelijk_8x.png')
