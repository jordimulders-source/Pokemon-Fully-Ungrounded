exec(open('teken.py').read().split("vars=[")[0])
import math
bodymask=(base.min(axis=2)<235)
from PIL import ImageFilter
ol=Image.fromarray(((cleaned.max(axis=2)<50)*255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
outline=(np.array(Image.fromarray(((base.max(axis=2)<50)&~Mfull).astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0)
nx,ny=0.778,-0.628
def inside(X,Y): return (X-335)*nx+(Y-P-575)*ny>4
outs=[];zooms=[]
for name,k,rot,sh in [('B',0.75,15,0),('H_B_rand_12',0.75,15,12),('I_B_rand_22',0.75,15,22)]:
    w,h=tc.size; nw=int(w*k)
    c=tc.resize((nw,h),Image.NEAREST).rotate(rot,resample=Image.NEAREST,expand=True)
    m=np.array(tm.resize((nw,h),Image.NEAREST).rotate(rot,resample=Image.NEAREST,expand=True))>0
    W2,H2=c.size
    im=Image.fromarray(cleaned.astype('uint8'))
    cx2=cx-6-nx*sh; cy2=cy-ny*sh
    px,py=int(cx2-W2/2),int(cy2-H2/2)
    for yy in range(H2):
        for xx in range(W2):
            if m[yy,xx] and not (inside(px+xx,py+yy) and bodymask[py+yy,px+xx] and not outline[py+yy,px+xx]): m[yy,xx]=False
    im.paste(c,(px,py),Image.fromarray((m*255).astype('uint8')))
    im.save('teken_%s.png'%name)
    t=im.resize((400,446),Image.LANCZOS); d=ImageDraw.Draw(t); d.text((8,8),name,fill=(0,0,0)); outs.append(t)
    zooms.append(im.crop((300,560,540,800)).resize((300,300),Image.NEAREST))
V=Image.new('RGB',(1200,746),'white')
for i,o in enumerate(outs): V.paste(o,(i*400,0)); V.paste(zooms[i],(i*400+50,446))
V.save('teken_vel3.png')
