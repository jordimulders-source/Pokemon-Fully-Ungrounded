import numpy as np; from PIL import Image, ImageDraw; import maak_r10 as m10, kijk
from lever_r6 import png, tekst
from lever_r8 import model_crop
R='r10/'
def grid(a,s,bx):
    a=a.copy(); d=ImageDraw.Draw(a)
    for i in range(bx[2]-bx[0]+1): d.line([(i*s,0),(i*s,a.height)],fill=(255,0,0) if (bx[0]+i)%5==0 else (170,170,170))
    for j in range(bx[3]-bx[1]+1): d.line([(0,j*s),(a.width,j*s)],fill=(255,0,0) if (bx[1]+j)%5==0 else (170,170,170))
    return a
def uit(im,s,bx): return grid(kijk.op_wit(im,s).crop((bx[0]*s,bx[1]*s,bx[2]*s,bx[3]*s)),s,bx)
def mod(s,bx): return grid(model_crop(bx[0],bx[1]-2,bx[2],bx[3]-2,s),s,bx)      # lijf staat sinds r9 2 px lager
def rij(items,pad):
    w=sum(i.width+20 for i,_ in items); h=max(i.height for i,_ in items)+18
    c=Image.new('RGB',(w,h),'white'); x=0
    for i,t in items: c.paste(i,(x,18)); tekst(c,(x,2),t); x+=i.width+20
    if pad: c.save(pad)
    return c
A=m10.bouw(); log=dict(m10.LOG); im=png(A,R+'zandloper_fase3.png')
open(R+'log.txt','w').write('\n'.join('%s %d %s'%(k,len(v),v) for k,v in log.items()))
print(len(np.unique(A)),'kleuren; diff met r9:',int((A!=m10.R9).sum()),'px')
for k,v in log.items(): print(' ',k,len(v))
r9=Image.open('r9/zandloper_fase3.png')
# schoudervarianten
SB=(9,3,25,30)
va=png(m10.bouw((-2,0)),R+'schouder_a.png'); vb=png(m10.bouw((-1,0)),R+'schouder_b.png')
rij([(uit(va,14,SB),'schouder_a: fles 2 px omhoog (= r8-plek)'),(uit(vb,14,SB),'schouder_b: fles 1 px omhoog, buik zakt in de koepel'),
     (uit(r9,14,SB),'r9'),(mod(14,SB),'model r5')],R+'vel_schouder.png')
# ogen
OB=(19,11,37,22)
ov=[(uit(png(m10.bouw(oog=v)),12,OB),t) for v,t in (('a','a: beide pupillen links (hoofdversie)'),('b','b: beide pupillen rechts'),('c','c: linkeroog 1 px smaller'))]
rij(ov+[(uit(r9,12,OB),'r9')],R+'vel_ogen.png')
# overlay schouder
s=24; bx=(9,8,25,30); M=model_crop(bx[0],bx[1]-2,bx[2],bx[3]-2,s); S=kijk.op_wit(im,s).crop((bx[0]*s,bx[1]*s,bx[2]*s,bx[3]*s))
rij([(grid(Image.blend(M,S,.45),s,bx),'r10 over model r5 (24x)'),(grid(M,s,bx),'model r5')],R+'overlay_schouder.png')
# vel
W=3*530; c=Image.new('RGB',(W,560+150),'white')
mo=Image.open('../gemini/r5.webp').convert('RGB').resize((512,512),Image.LANCZOS)
for i,(x,t) in enumerate([(kijk.op_wit(im,8),'r10'),(kijk.op_wit(r9,8),'r9'),(mo,'model r5')]):
    c.paste(x,(i*530,20)); tekst(c,(i*530+4,4),t)
y=545
for i,(x,t) in enumerate([(im,'r10 1x'),(r9,'r9 1x')]):
    for j,bg in enumerate([(255,255,255),(40,44,52)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); c.paste(b.convert('RGB'),(i*170+j*72,y+16))
    tekst(c,(i*170,y),t)
HB=(17,22,29,35)
r1=rij([(uit(im,12,SB),'r10 linkerschouder 12x'),(mod(12,SB),'model')],None)
r2=rij([(uit(im,12,HB),'r10 rechtervuist 12x'),(uit(r9,12,HB),'r9'),(mod(12,HB),'model')],None)
v=Image.new('RGB',(W,c.height+max(r1.height,r2.height)+10),'white'); v.paste(c,(0,0)); v.paste(r1,(0,c.height)); v.paste(r2,(r1.width+30,c.height))
v.save(R+'vel.png')
