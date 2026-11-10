# grid.py in.png out.png [zoom] : 64x64 png vergroot met raster en coordinaten om de 4
import sys
from PIL import Image,ImageDraw
z=int(sys.argv[3]) if len(sys.argv)>3 else 12
im=Image.open(sys.argv[1]).convert('RGBA'); bg=Image.new('RGBA',im.size,(152,208,160,255)); bg.alpha_composite(im)
o=Image.new('RGB',(64*z+30,64*z+30),'white'); o.paste(bg.convert('RGB').resize((64*z,64*z),Image.NEAREST),(30,30))
d=ImageDraw.Draw(o)
for i in range(65):
  col=(255,0,0) if i%8==0 else (200,200,200)
  if i%4==0: d.line([(30+i*z,30),(30+i*z,30+64*z)],fill=col); d.line([(30,30+i*z),(30+64*z,30+i*z)],fill=col)
  if i%4==0 and i<64: d.text((30+i*z+1,10),str(i),fill='black'); d.text((2,30+i*z+1),str(i),fill='black')
o.save(sys.argv[2])
