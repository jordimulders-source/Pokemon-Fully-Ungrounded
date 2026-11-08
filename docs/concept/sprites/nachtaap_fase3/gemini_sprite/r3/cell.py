import sys,numpy as np
from PIL import Image
from tools import P,CH
a=np.array(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/gemini/gekozen_r4.png').convert('RGB')).astype(int)
Pa=np.array(P)
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('   '+''.join(str(x%10) for x in range(x0,x1))+'    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    r1='';r2=''
    for x in range(x0,x1):
        b=a[16*y-1+3:16*y+15-3,16*x-2+3:16*x+14-3].reshape(-1,3)
        bg=(b.min(1)>247)
        if bg.mean()>0.5: r1+='.'; r2+='.'; continue
        b=b[~bg]; lum=b.mean(1)
        dk=(lum<45).mean()
        m=np.median(b,0)
        d=((Pa[1:]-m)**2).sum(1); r1+=CH[1+d.argmin()]
        r2+= '#' if dk>0.5 else ('+' if dk>0.2 else ' ')
    print('%2d '%y+r1+'    '+r2)
