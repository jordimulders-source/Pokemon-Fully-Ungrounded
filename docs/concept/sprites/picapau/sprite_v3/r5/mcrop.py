# modeluitsnede op spriteraster: python3 mcrop.py x0 y0 x1 y1 uit  (sprite-coordinaten, 24 px per spritepixel)
import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); S=24
im=Image.open('../../gemini/r5_verbeter.png').convert('RGB')
c=lambda s:4.13+(1+3*s)*5.12
cr=im.crop((int(c(x0)),int(c(y0)),int(c(x1)),int(c(y1)))).resize(((x1-x0)*S,(y1-y0)*S),0)
d=ImageDraw.Draw(cr)
for i in range(x1-x0+1): d.line([(i*S,0),(i*S,cr.height)],fill=(0,160,255))
for j in range(y1-y0+1): d.line([(0,j*S),(cr.width,j*S)],fill=(0,160,255))
for i in range(x1-x0): d.text((i*S+2,1),str((x0+i)%100),fill=(255,0,0))
for j in range(y1-y0): d.text((1,j*S+12),str(y0+j),fill=(0,0,255))
cr.save(sys.argv[5])
