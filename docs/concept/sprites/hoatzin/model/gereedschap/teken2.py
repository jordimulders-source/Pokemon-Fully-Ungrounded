exec(open('teken.py').read().split("vars=[")[0])
import math
bodymask=(base.min(axis=2)<235)
from PIL import ImageFilter
ol=Image.fromarray(((cleaned.max(axis=2)<50)*255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
outline=(np.array(Image.fromarray(((base.max(axis=2)<50)&~Mfull).astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0)
nx,ny=0.778,-0.628
def inside(X,Y): return (X-335)*nx+(Y-P-575)*ny>4
vars=[('E_rand_20',0.75,0,20,False),('F_rand_35',0.75,0,35,False),('G_rand_35_gebogen',0.75,0,35,True)]
outs=[];zooms=[]
for name,k,rot,sh,cyl in vars:
    w,h=tc.size; nw=int(w*k)
    c=np.array(tc.resize((nw,h),Image.NEAREST)); m=np.array(tm.resize((nw,h),Image.NEAREST))>0
    if cyl:
        # far (links) helft sterker samengedrukt: x' = nw*(1-cos(t))... eenvoudige kromming
        xs=np.arange(nw); u=xs/(nw-1)  # 0 links .. 1 rechts
        src=(np.sin(u*math.pi/2))*(nw-1)  # links samengedrukt
        idx=np.clip(src.round().astype(int),0,nw-1)
        c=c[:,idx]; m=m[:,idx]
    im=Image.fromarray(cleaned.astype('uint8'))
    cx2=cx-6-nx*sh; cy2=cy-ny*sh
    px,py=int(cx2-nw/2),int(cy2-h/2)
    mm=m.copy()
    for yy in range(h):
        for xx in range(nw):
            if mm[yy,xx] and not (inside(px+xx,py+yy) and bodymask[py+yy,px+xx] and not outline[py+yy,px+xx]): mm[yy,xx]=False
    im.paste(Image.fromarray(c.astype('uint8')),(px,py),Image.fromarray((mm*255).astype('uint8')))
    im.save('teken_%s.png'%name)
    t=im.resize((400,446),Image.LANCZOS); d=ImageDraw.Draw(t); d.text((8,8),name,fill=(0,0,0)); outs.append(t)
    zooms.append(im.crop((300,560,540,800)).resize((300,300),Image.NEAREST))
W=Image.new('RGB',(1200,746),'white')
for i,o in enumerate(outs): W.paste(o,(i*400,0)); W.paste(zooms[i],(i*400+50,446))
W.save('teken_vel2.png')
