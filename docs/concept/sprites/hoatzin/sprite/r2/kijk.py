# hulp: sprite (npy/png) 8x naast model op schaal 8x, met raster
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from PIL import ImageDraw
def groot(img,f=8,raster=True):
    im=img.resize((img.width*f,img.height*f),0)
    if raster:
        d=ImageDraw.Draw(im)
        for i in range(0,img.width*f,f*8): d.line([(i,0),(i,im.height)],fill=(200,200,255))
        for i in range(0,img.height*f,f*8): d.line([(0,i),(im.width,i)],fill=(200,200,255))
    return im
if __name__=='__main__':
    o=np.load(sys.argv[1]) if sys.argv[1].endswith('.npy') else np.array(Image.open(sys.argv[1]))
    box=[int(v) for v in sys.argv[3].split(',')] if len(sys.argv)>3 else [0,0,64,64]
    f=int(sys.argv[4]) if len(sys.argv)>4 else 8
    sp=rgb(o,(255,255,255)).crop(box); md=model_op_schaal().crop(box)
    a=groot(sp,f); b=groot(md,f)
    out=Image.new('RGB',(a.width*2+8,a.height),(255,255,255)); out.paste(a,(0,0)); out.paste(b,(a.width+8,0)); out.save(sys.argv[2])
