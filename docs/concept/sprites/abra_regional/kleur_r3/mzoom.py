# mzoom.py x0 y0 x1 y1 UIT: het originele Gemini-model op 32 px per spritepixel met spriteraster en nummers
import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); Z=32
m=Image.open('../referenties/gemini_gekozen.png').convert('RGB')
f=lambda x:8*(2*x-1)+7.75; g=lambda y:8*(2*y-14)+7.75
c=m.crop((round(f(x0)),round(g(y0)),round(f(x1)),round(g(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
v=Image.new('RGB',(c.width+30,c.height+30),'white'); v.paste(c,(30,30)); d=ImageDraw.Draw(v)
for x in range(x0,x1+1): d.line([(30+(x-x0)*Z,30),(30+(x-x0)*Z,v.height)],fill=(255,0,0) if x%5==0 else (255,170,170))
for y in range(y0,y1+1): d.line([(30,30+(y-y0)*Z),(v.width,30+(y-y0)*Z)],fill=(255,0,0) if y%5==0 else (255,170,170))
for x in range(x0,x1): d.text((30+(x-x0)*Z+8,8),str(x),fill=(0,0,0))
for y in range(y0,y1): d.text((4,30+(y-y0)*Z+10),str(y),fill=(0,0,0))
v.save(sys.argv[5])
