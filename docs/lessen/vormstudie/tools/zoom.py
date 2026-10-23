import sys;sys.path.insert(0,'.')
from lib import *
from PIL import ImageDraw
def zoom(names,out,s=5,cols=5,crop=True,paths=None):
    ims=[]
    for n in names:
        im=load(None,p=paths[n]) if paths and n in paths else load(n,True)
        m=metrics(im)
        if crop: im=im.crop((max(0,m['x0']-2),max(0,m['y0']-2),min(64,m['x1']+3),min(64,m['y1']+3)))
        ims.append((n,im,m))
    W=max(i.size[0] for _,i,_ in ims)*s+8; H=max(i.size[1] for _,i,_ in ims)*s+14
    rows=(len(ims)+cols-1)//cols
    sh=Image.new('RGB',(cols*W,rows*H),(225,230,225)); dr=ImageDraw.Draw(sh)
    for k,(n,im,m) in enumerate(ims):
        x,y=(k%cols)*W,(k//cols)*H
        big=im.resize((im.size[0]*s,im.size[1]*s),Image.NEAREST)
        # grid every 8px
        for gx in range(0,im.size[0]*s,s*4): dr.line([x+4+gx,y+2,x+4+gx,y+2+im.size[1]*s],fill=(210,214,210))
        sh.paste(big,(x+4,y+2),big)
        dr.text((x+4,y+H-12),f"{n} {m['w']}x{m['h']} A{m['A']}",fill=(0,0,0))
    sh.save(out)
if __name__=='__main__':
    zoom(sys.argv[2].split(','),sys.argv[1],int(sys.argv[3]) if len(sys.argv)>3 else 5)
