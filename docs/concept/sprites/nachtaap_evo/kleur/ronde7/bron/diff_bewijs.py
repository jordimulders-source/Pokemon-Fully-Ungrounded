# ronde6 t.o.v. ronde5: diff per zone, 0 erbuiten
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
a=np.array(Image.open(os.path.join(H,'../../ronde5/nachtaap.png'))); b=np.array(Image.open(os.path.join(H,'../nachtaap.png')))
Z={'F5 kene (x16-47,y26-38)':(16,47,26,38),'handen (x3-27,y55-62)':(3,27,55,62),'achtervoet (x31-42,y56-60)':(31,42,56,60),
   'oor links (x3-6,y37-41)':(3,6,37,41),'oor rechts (x23-26,y37-42)':(23,26,37,42)}
m=np.zeros((64,64),bool)
for n,(x0,x1,y0,y1) in Z.items():
    z=np.zeros((64,64),bool); z[y0:y1+1,x0:x1+1]=True; print(n,int(((a!=b)&z&~m).sum())); m|=z
print('totaal',int((a!=b).sum()),'| buiten de zones',int(((a!=b)&~m).sum()))
print('palet gelijk',Image.open(os.path.join(H,'../../ronde5/nachtaap.png')).getpalette()[:48]==Image.open(os.path.join(H,'../nachtaap.png')).getpalette()[:48])
