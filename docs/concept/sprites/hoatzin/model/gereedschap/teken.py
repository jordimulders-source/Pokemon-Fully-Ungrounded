from PIL import Image, ImageDraw
import numpy as np
from PIL import ImageFilter
def binary_dilation(m,iterations=1):
    im=Image.fromarray((m*255).astype('uint8'))
    for _ in range(iterations): im=im.filter(ImageFilter.MaxFilter(3))
    return np.array(im)>0
P=120
base=np.array(Image.open('comb_s1.1.png').convert('RGB')).astype(int)
x0,x1,y0,y1=335,511,478+P,658+P
reg=base[y0:y1,x0:x1].copy()
r,g,b=reg[...,0],reg[...,1],reg[...,2]
M=(g>110)&(r>90)&(b<130)&(g-b>50)
Mclr=binary_dilation((g-b>18)&(g>60)|M,iterations=3)
clean=reg.astype(float).copy()
known=~Mclr
clean[Mclr]=np.array([50,52,48])
for _ in range(400):
    pad=np.pad(clean,((1,1),(1,1),(0,0)),mode='edge')
    avg=(pad[:-2,1:-1]+pad[2:,1:-1]+pad[1:-1,:-2]+pad[1:-1,2:])/4
    clean[Mclr]=avg[Mclr]
cleaned=base.copy(); cleaned[y0:y1,x0:x1]=clean.round()
Mfull=np.zeros(base.shape[:2],bool); Mfull[y0:y1,x0:x1]=Mclr
Mp=binary_dilation(M,iterations=1)
tc=Image.fromarray(reg.astype('uint8')); tm=Image.fromarray((Mp*255).astype('uint8'))
cx,cy=(x0+x1)//2,(y0+y1)//2
vars=[('A_smal',0.75,0,-6),('B_smal_draai_links',0.75,15,-6),('C_smal_draai_rechts',0.75,-15,-6),('D_smaller',0.6,0,-10)]
outs=[]; zooms=[]
bodymask=(base.min(axis=2)<235)
for name,k,rot,dx in vars:
    w,h=tc.size; nw=int(w*k)
    c=tc.resize((nw,h),Image.NEAREST).rotate(rot,resample=Image.NEAREST,expand=True)
    m=tm.resize((nw,h),Image.NEAREST).rotate(rot,resample=Image.NEAREST,expand=True)
    im=Image.fromarray(cleaned.astype('uint8'))
    px,py=cx+dx-c.size[0]//2, cy-c.size[1]//2
    mm=np.array(m)>0
    mm=mm&bodymask[py:py+mm.shape[0],px:px+mm.shape[1]]
    im.paste(c,(px,py),Image.fromarray((mm*255).astype('uint8')))
    im.save('teken_%s.png'%name)
    t=im.resize((400,446),Image.LANCZOS); d=ImageDraw.Draw(t); d.text((8,8),name,fill=(0,0,0)); outs.append(t)
    zooms.append(im.crop((300,560,540,800)).resize((300,300),Image.NEAREST))
W=Image.new('RGB',(1600,746),'white')
for i,o in enumerate(outs): W.paste(o,(i*400,0)); W.paste(zooms[i],(i*400+50,446))
W.save('teken_vel.png')
