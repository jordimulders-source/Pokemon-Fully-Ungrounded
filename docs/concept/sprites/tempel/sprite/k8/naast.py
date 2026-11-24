import sys
from PIL import Image, ImageDraw
M=Image.open('../../referenties/model.webp').convert('RGB'); s=(983-46)/62
def mcrop(x0,y0,x1,y1,z):
    return M.crop((int(46+(x0-1)*s),int(57+(y0-3)*s),int(46+(x1-1)*s),int(57+(y1-3)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def op(p,box,z):
    im=Image.open(p).convert('RGBA').crop(box); b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im)
    return b.convert('RGB').resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
p=sys.argv[1]; box=tuple(int(v) for v in sys.argv[2].split(',')); z=int(sys.argv[3])
A=op(p,box,z); B=mcrop(*box,z)
V=Image.new('RGB',(A.size[0]*2+40,A.size[1]+30),(255,255,255)); V.paste(A,(20,30)); V.paste(B,(A.size[0]+40,30)); d=ImageDraw.Draw(V)
for x in range(box[0],box[2],2):
    for o in (20,A.size[0]+40): d.text((o+(x-box[0])*z,2+(x%4)*3),str(x),fill=(0,0,255))
for y in range(box[1],box[3],2): d.text((0,30+(y-box[1])*z),str(y),fill=(255,0,0))
# raster over model
for x in range(box[0],box[2]+1,2): d.line([(A.size[0]+40+(x-box[0])*z,30),(A.size[0]+40+(x-box[0])*z,30+A.size[1])],fill=(255,0,0) if x%10==0 else (255,180,180))
for y in range(box[1],box[3]+1,2): d.line([(A.size[0]+40,30+(y-box[1])*z),(A.size[0]*2+40,30+(y-box[1])*z)],fill=(255,0,0) if y%10==0 else (255,180,180))
V.save(sys.argv[4])
