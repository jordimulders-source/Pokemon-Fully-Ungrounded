import numpy as np; from PIL import Image; import maak_r8 as m8, maak_r6 as m, kijk
from lever_r6 import png, tekst
def model_crop(x0s,y0s,x1s,y1s,s):
    a=Image.open('../gemini/r5.webp').convert('RGB'); x0=(0*3+2)*5.12-0.12; y0=(2*3+2)*5.12-0.12; p=15.36
    return a.crop((int(x0+x0s*p),int(y0+y0s*p),int(x0+x1s*p),int(y0+y1s*p))).resize(((x1s-x0s)*s,(y1s-y0s)*s),Image.LANCZOS)
R='r8/'
A=m8.basis(); log=dict(m.LOG); im=png(A,R+'zandloper_fase3.png')
o1=png(m8.omhoog(A,1),R+'hoofd_op1.png'); o2=png(m8.omhoog(A,2),R+'hoofd_op2.png')
r7=Image.open('r7/zandloper_fase3.png'); R7=np.asarray(r7)
print(len(np.unique(A)),'kleuren; diff met r7:',int((A!=R7).sum()),'px; diff met r5:',int((A!=m.R5).sum()))
Z=np.zeros((64,64),bool); Z[0:23,18:42]=True; Z[15:34,10:26]=True
print('buiten zones t.o.v. r5:',int(((A!=m.R5)&~Z).sum()))
open(R+'log.txt','w').write('\n'.join('%s %d %s'%(k,len(v),v) for k,v in log.items()))
c=Image.new('RGB',(4*520,20+512+110+290),'white')
for i,(x,t) in enumerate([(im,'r8'),(o1,'hoofd 1 px omhoog'),(o2,'hoofd 2 px omhoog'),(r7,'r7')]):
    c.paste(kijk.op_wit(x,8),(i*520,20)); tekst(c,(i*520+4,4),t)
y=545
for i,(x,t) in enumerate([(im,'r8'),(o1,'op1'),(o2,'op2'),(r7,'r7')]):
    for j,bg in enumerate([(255,255,255),(40,44,52)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); c.paste(b.convert('RGB'),(i*160+j*70,y+14))
    tekst(c,(i*160,y),t+' 1x')
y=650
c.paste(kijk.op_wit(im,12).crop((9*12,14*12,27*12,35*12)),(0,y+14)); tekst(c,(0,y),'r8 linkerarm + handen 12x')
c.paste(kijk.op_wit(r7,12).crop((9*12,14*12,27*12,35*12)),(240,y+14)); tekst(c,(240,y),'r7')
c.paste(model_crop(9,14,27,35,12),(480,y+14)); tekst(c,(480,y),'model')
c=c.crop((0,0,c.width,y+14+252+10)); c.save(R+'vel.png')
