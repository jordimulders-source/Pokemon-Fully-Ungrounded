# Model (origineel) op Z px per spritepixel met spriteraster en coordinaten, plus de sprite ernaast.
import sys; from PIL import Image, ImageDraw
sp=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); Z=int(sys.argv[7]); out=sys.argv[6]
M=Image.open('../../referenties/model_v14.png').convert('RGB')
mc=M.crop((106+x0*12,120+y0*12,106+x1*12,120+y1*12)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
S=Image.open(sp).convert('RGBA'); bg=Image.new('RGBA',S.size,(255,255,255,255)); bg.alpha_composite(S)
sc=bg.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=(x1-x0)*Z; im=Image.new('RGB',(W*2+30,(y1-y0)*Z+20),(255,255,255)); im.paste(mc,(20,20)); im.paste(sc,(W+30,20))
d=ImageDraw.Draw(im)
for off in (20,W+30):
    for i in range(x1-x0+1): d.line([(off+i*Z,20),(off+i*Z,20+(y1-y0)*Z)],fill=(90,90,255))
    for j in range(y1-y0+1): d.line([(off,20+j*Z),(off+W,20+j*Z)],fill=(90,90,255))
    for i in range(x1-x0): d.text((off+i*Z+2,4),str(x0+i),fill=(0,0,0))
for j in range(y1-y0): d.text((2,20+j*Z+2),str(y0+j),fill=(0,0,0))
im.save(out)
