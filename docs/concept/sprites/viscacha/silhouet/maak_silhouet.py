"""Silhouet viscacha: masker uit de Gemini-bron (r6), snorharen weg (opening), verkleind naar 64x64."""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
src=Image.open(D+'referenties/gemini_gekozen_ronde6.png').convert('RGB')
im=np.array(src).astype(int)
m=np.abs(im-255).sum(2)>60
m=nd.binary_fill_holes(m)
mo=nd.binary_opening(m,structure=np.ones((7,7)))
d=m&~mo; lab,n=nd.label(d,structure=np.ones((3,3)))
sat=im.max(2)-im.min(2)
for i in range(1,n+1):   # dunne delen terug als ze gekleurd zijn (pluimpunten, oorranden); grijze snorharen blijven weg
    z=lab==i
    if (sat[z]>90).sum()>=4 and z.sum()<3000: mo|=z
m=mo   # snorharen (2-3 px) weg
lab,n=nd.label(m); sz=nd.sum(m,lab,range(1,n+1)); m=lab==(1+np.argmax(sz))
ys,xs=np.nonzero(m); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
print('bron-bbox',x0,x1,y0,y1)
S=(x1-x0)/62.0          # breedte 62 px in het frame
w=int(round((x1-x0)/S)); h=int(round((y1-y0)/S))
ox=(64-w)//2; oy=64-h-1  # voeten op rij 62
print('schaal 1:%.2f, dier %dx%d, offset %d,%d'%(S,w,h,ox,oy))
crop=Image.fromarray((m[y0:y1,x0:x1]*255).astype(np.uint8))
small=np.array(crop.resize((w,h),Image.BOX))>=128
sil=np.zeros((64,64),bool); sil[oy:oy+h,ox:ox+w]=small
np.save(D+'silhouet/meta.npy',np.array([x0,y0,S,ox,oy]))
Image.fromarray((sil*255).astype(np.uint8)).save(D+'silhouet/silhouet_auto.png')
open(D+'silhouet/silhouet_auto.txt','w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in sil)+'\n')
