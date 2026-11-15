# diff_r1.py: bewijst dat lijf en gezicht buiten de opdrachtzones gelijk zijn aan ronde 1 (RGB-diff per pixel)
import numpy as np
from PIL import Image
a=np.asarray(Image.open('gengas_r2.png').convert('RGB')).astype(int); b=np.asarray(Image.open('../sprite_r1/gengas_r1.png').convert('RGB')).astype(int)
ta=np.array(Image.open('gengas_r2.png'))==0; tb=np.array(Image.open('../sprite_r1/gengas_r1.png'))==0
Z={'hand boven':(23,0,38,11),'voet rechtsboven':(50,20,63,32),'voet linksonder':(0,40,13,52),'hand rechtsonder':(40,49,56,63),'wervel':(33,32,47,39)}
m=np.zeros((64,64),bool)
for x0,y0,x1,y1 in Z.values(): m[y0:y1+1,x0:x1+1]=True
d=((a!=b).any(2)|(ta!=tb))
print('pixels anders dan r1 buiten de zones:',int((d&~m).sum()))
for k,(x0,y0,x1,y1) in Z.items(): print(f'  {k}: {int(d[y0:y1+1,x0:x1+1].sum())} px gewijzigd')
ys,xs=np.where(d&~m); print(list(zip(xs,ys))[:20])
