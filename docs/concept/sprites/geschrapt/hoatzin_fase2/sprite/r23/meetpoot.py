# per spritepixel in het pootgebied: achtergrondfractie (0-9) en gemiddelde L van de figuurpixels, uit MODEL.png (1024)
import numpy as np; from PIL import Image
from geom import model_box
m=np.asarray(Image.open('../../MODEL.png').convert('RGB')).astype(float); L=m@[.299,.587,.114]; bg=m.min(2)>215
def meet(x,y):
    a,b,c,d=[int(round(v)) for v in model_box(x,y,x+1,y+1)]
    s=(slice(b,d),slice(a,c)); f=bg[s].mean(); l=L[s][~bg[s]]
    return f,(l.mean() if l.size else 0), m[s][~bg[s]].mean(0) if l.size else np.zeros(3)
if __name__=='__main__':
    for y in range(49,64):
        r1='';r2=''
        for x in range(14,40):
            f,l,_=meet(x,y); r1+=str(min(9,int(f*10))); r2+=' ' if f>0.6 else ('#' if l<45 else ('+' if l<70 else ('-' if l<95 else 'o')))
        print('%2d %s   %s'%(y,r1,r2))
