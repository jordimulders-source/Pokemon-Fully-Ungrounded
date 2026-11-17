# Close-up: modeluitsnede met spriteraster | sprite, op 12x. gebruik: rooster.py sprite.png x0 y0 x1 y1 uit.png
import sys; from PIL import Image, ImageDraw
sp=Image.open(sys.argv[1]).convert('RGBA'); x0,y0,x1,y1=map(int,sys.argv[2:6]); Z=int(sys.argv[7]) if len(sys.argv)>7 else 12
M=Image.open('../../referenties/model_v14.png').convert('RGB')
mc=M.crop((106+x0*12,120+y0*12,106+x1*12,120+y1*12)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
d=ImageDraw.Draw(mc)
for i in range(x1-x0+1): d.line([(i*Z,0),(i*Z,mc.size[1])],fill=(120,120,120))
for j in range(y1-y0+1): d.line([(0,j*Z),(mc.size[0],j*Z)],fill=(120,120,120))
bg=Image.new('RGBA',sp.size,(255,255,255,255)); bg.alpha_composite(sp)
sc=bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST); d2=ImageDraw.Draw(sc)
for i in range(x1-x0+1): d2.line([(i*Z,0),(i*Z,sc.size[1])],fill=(200,200,200))
for j in range(y1-y0+1): d2.line([(0,j*Z),(sc.size[0],j*Z)],fill=(200,200,200))
for i in range(0,x1-x0,2): d2.text((i*Z+1,0),str(x0+i),fill=(0,0,255))
for j in range(0,y1-y0,2): d2.text((0,j*Z+1),str(y0+j),fill=(0,0,255))
out=Image.new('RGB',(mc.size[0]*2+8,mc.size[1]),(255,255,255)); out.paste(mc,(0,0)); out.paste(sc.convert('RGB'),(mc.size[0]+8,0)); out.save(sys.argv[6])
