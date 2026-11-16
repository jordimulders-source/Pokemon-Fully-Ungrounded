# Origineel model met het spriteraster erover (K=13,77 modelpx per spritepx; sprite (0,2) = model (102,71)).
import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1,out=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
K=13.77; Z=int(sys.argv[6]) if len(sys.argv)>6 else 24
m=Image.open('model/model.webp').convert('RGB')
mx0=102+x0*K; my0=71+(y0-2)*K
c=m.crop((int(mx0),int(my0),int(mx0+(x1-x0)*K),int(my0+(y1-y0)*K))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
d=ImageDraw.Draw(c)
for i in range(x1-x0+1): d.line([(i*Z,0),(i*Z,c.size[1])],fill=(0,0,255) if (x0+i)%5==0 else (170,170,255),width=1)
for j in range(y1-y0+1): d.line([(0,j*Z),(c.size[0],j*Z)],fill=(0,0,255) if (y0+j)%5==0 else (170,170,255),width=1)
for i in range(x1-x0):
    if (x0+i)%5==0: d.text((i*Z+2,2),str(x0+i),fill=(255,0,0))
for j in range(y1-y0):
    if (y0+j)%5==0: d.text((2,j*Z+2),str(y0+j),fill=(255,0,0))
c.save(out)
