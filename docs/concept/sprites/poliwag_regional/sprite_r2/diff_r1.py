# Bewijs: r2 wijkt alleen binnen de opdrachtzones af van r1 (spiraal, ver oog, nabij oog)
import numpy as np
from PIL import Image
r1=np.load('r1.npy'); r2=np.load('r2.npy')
Z={'spiraal (x3-16,y19-32)':(3,16,19,32),'ver oog (x2-7,y7-14)':(2,7,7,14),'nabij oog (x13-20,y7-14)':(13,20,7,14)}
d=r1!=r2; buiten=d.copy()
for n,(x0,x1,y0,y1) in Z.items():
    m=np.zeros_like(d); m[y0:y1+1,x0:x1+1]=True
    print('%-26s %3d px gewijzigd'%(n,(d&m).sum())); buiten&=~m
print('buiten de zones gewijzigd:',buiten.sum(), [(int(x),int(y)) for y,x in np.argwhere(buiten)])
a=np.array(Image.open('poliwag_regional_r2.png')); b=np.array(Image.open('../sprite_r1/poliwag_regional_r1.png'))
print('png 64x64 verschil totaal',(a!=b).sum(),'| palet gelijk:',Image.open('poliwag_regional_r2.png').getpalette()[:48]==Image.open('../sprite_r1/poliwag_regional_r1.png').getpalette()[:48])
