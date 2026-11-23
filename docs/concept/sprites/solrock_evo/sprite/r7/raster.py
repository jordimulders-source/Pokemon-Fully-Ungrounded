# Hulpvel: model (origineel 1024) met het spritegrid erover + sprite met grid, zelfde schaal, coordinaten.
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../r6'); from toon_gezicht import PAL, rgba, S, X0, Y0
def vel(o,fn,box=(14,21,37,47),z=24):
    x0,y0,x1,y1=box; m=Image.open('../../referenties/model.png').convert('RGB')
    mm=m.crop((int(round(X0+x0*S)),int(round(Y0+y0*S)),int(round(X0+x1*S)),int(round(Y0+y1*S)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
    sp=rgba(o).convert('RGB').crop(box).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    out=Image.new('RGB',(mm.width*2+30,mm.height+30),(255,255,255))
    for k,im in enumerate([sp,mm]):
        d=ImageDraw.Draw(im)
        for i in range(x1-x0+1): d.line([(i*z,0),(i*z,im.height)],fill=(0,160,255) if (x0+i)%5 else (255,0,255))
        for j in range(y1-y0+1): d.line([(0,j*z),(im.width,j*z)],fill=(0,160,255) if (y0+j)%5 else (255,0,255))
        out.paste(im,(30+k*(mm.width),30))
    d=ImageDraw.Draw(out)
    for i in range(x1-x0):
        for k in range(2): d.text((30+k*mm.width+i*z+4,10),str(x0+i),fill=(0,0,0))
    for j in range(y1-y0): d.text((4,30+j*z+6),str(y0+j),fill=(0,0,0))
    out.save(fn)
if __name__=='__main__': vel(np.load(sys.argv[1]),sys.argv[2])
