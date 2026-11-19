import sys; from PIL import Image
sys.path.insert(0,'.'); from pal import P
def load(f): return [l.rstrip('\n') for l in open(f) if l.strip()]
def img(g):
    w=max(len(r) for r in g); im=Image.new('RGB',(w,len(g)),P['.'][1])
    for y,r in enumerate(g):
        for x,c in enumerate(r): im.putpixel((x,y),P[c][1])
    return im
if __name__=='__main__':
    ims=[img(load(f)) for f in sys.argv[2:]]
    W=sum(i.width+2 for i in ims); H=max(i.height for i in ims)
    out=Image.new('RGB',(W,H),(152,208,160)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width+2
    out.resize((W*16,H*16),Image.NEAREST).save(sys.argv[1])
