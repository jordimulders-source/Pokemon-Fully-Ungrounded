# hulp: uitsnede sprite | model (geschrapt) op schaal s, coordinaten lokaal (geschrapt)
import sys; from PIL import Image
D='docs/concept/sprites/mate_fase2/sprite/'
f,x0,y0,x1,y1,s,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
sp=Image.open(D+f).convert('RGBA'); g=Image.open(D+'r4/geschrapt.png').convert('RGBA')
b=Image.new('RGBA',(64,64),(235,240,235,255)); b.alpha_composite(sp); oy=64-48-1
A=b.crop((x0,y0+oy,x1,y1+oy)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST); B=g.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
o=Image.new('RGB',(A.width*2+8,A.height),(255,255,255)); o.paste(A,(0,0)); o.paste(B,(A.width+8,0)); o.save(out)
