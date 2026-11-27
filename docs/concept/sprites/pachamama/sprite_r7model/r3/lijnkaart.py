# meet: per spritecel (vergroot gezicht) in het hi-res model: aandeel lijnpixels (donker t.o.v. omgeving) en mediane helderheid vlak
import numpy as np; from PIL import Image; from PIL import ImageFilter
im=np.asarray(Image.open('../../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float)
L=im@np.array([.299,.587,.114]); med=np.asarray(Image.fromarray(L.astype('uint8')).filter(ImageFilter.MedianFilter(21))).astype(float)
lijn=(L<med-18)&(L<115)
PX,FX,PY,FY=5.704,5.16,5.692,3.088
fx=lambda sx: FX+(63+(3*sx-64)/1.2)*PX; fy=lambda sy: FY+(22+(3*sy-37)/1.28)*PY
def blok(y,x): return (slice(int(round(fy(y))),int(round(fy(y+1)))),slice(int(round(fx(x))),int(round(fx(x+1)))))
if __name__=='__main__':
  y0,y1,x0,x1=13,32,20,38
  print('lijnaandeel x10 per cel'); print('   '+''.join(str(x%10) for x in range(x0,x1)))
  for y in range(y0,y1):
    print('%2d '%y+''.join(str(min(9,int(lijn[blok(y,x)].mean()*10))) for x in range(x0,x1)))
  print('mediaan helderheid vlak (zonder lijn) /10'); print('   '+''.join(('%3d'%x) for x in range(x0,x1)))
  for y in range(y0,y1):
    s=''
    for x in range(x0,x1):
      b=blok(y,x); v=L[b][~lijn[b]]; s+='%3d'%(np.median(v)//1 if len(v) else 0)
    print('%2d '%y+s)
