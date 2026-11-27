import numpy as np; from PIL import Image; import maak_r11 as m11, kijk
from lever_r6 import png, tekst
from lever_r10 import uit, mod, rij
R='r11/'
A=m11.bouw(); log=dict(m11.LOG); im=png(A,R+'zandloper_fase3.png')
B=m11.biceps(A); logb={k:v for k,v in m11.LOG.items() if k=='biceps-variant'}; bi=png(B,R+'biceps.png')
open(R+'log.txt','w').write('\n'.join('%s %d %s'%(k,len(v),v) for k,v in {**log,**logb}.items()))
R9=m11.R9
print(len(np.unique(A)),'kleuren; diff r9:',int((A!=R9).sum()),'| biceps',len(np.unique(B)),'kleuren; diff r11:',int((B!=A).sum()))
for k,v in log.items(): print(' ',k,len(v))
print('  biceps-variant',len(logb.get('biceps-variant',[])))
r9=Image.open('r9/zandloper_fase3.png'); r10=Image.open('r10/zandloper_fase3.png')
mo=Image.open('../gemini/r5.webp').convert('RGB').resize((512,512),Image.LANCZOS)
top=rij([(kijk.op_wit(im,8),'r11'),(kijk.op_wit(r9,8),'r9'),(kijk.op_wit(r10,8),'r10'),(mo,'model r5')],None)
een=Image.new('RGB',(4*150,90),'white')
for i,(x,t) in enumerate([(im,'r11 1x'),(r9,'r9'),(r10,'r10'),(bi,'biceps')]):
    for j,bg in enumerate([(255,255,255),(40,44,52)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); een.paste(b.convert('RGB'),(i*150+j*70,20))
    tekst(een,(i*150,4),t)
HB=(18,3,42,24); AB=(6,12,28,37)
hoofd=rij([(uit(im,12,HB),'r11 hoofd 12x'),(uit(r9,12,HB),'r9')],None)
arm=rij([(uit(im,12,AB),'r11 linkerarm/handen 12x'),(uit(r9,12,AB),'r9'),(mod(12,AB),'model')],None)
bic=rij([(uit(bi,12,AB),'variant biceps 12x'),(uit(im,12,AB),'r11'),(mod(12,AB),'model')],None)
bic8=rij([(kijk.op_wit(bi,8),'variant biceps 8x'),(kijk.op_wit(im,8),'r11')],None)
delen=[top,een,hoofd,arm,bic,bic8]
W=max(d.width for d in delen); H=sum(d.height+10 for d in delen)
c=Image.new('RGB',(W,H),'white'); y=0
for d in delen: c.paste(d,(0,y)); y+=d.height+10
c.save(R+'vel.png')
