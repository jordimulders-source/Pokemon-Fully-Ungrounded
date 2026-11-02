# Pixeldiff ronde2 t.o.v. ronde1 buiten zone A (x2-27,y34-57) en zone B (x2-16,y54-61); en maanpixels tegen de onderlaag.
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
a=np.array(Image.open(os.path.join(H,'../../ronde1/nachtaap.png'))); b=np.array(Image.open(os.path.join(H,'../nachtaap.png')))
m=np.zeros((64,64),bool); m[34:58,2:28]=True; m[54:62,2:17]=True
pa=Image.open(os.path.join(H,'../../ronde1/nachtaap.png')).getpalette()[:45]; pb=Image.open(os.path.join(H,'../nachtaap.png')).getpalette()[:45]
print('palet index 0-14 gelijk:',pa==pb)
print('pixeldiff buiten zones:',int(((a!=b)&~m).sum()),'| binnen zones gewijzigd:',int(((a!=b)&m).sum()))
on=np.array(Image.open(os.path.join(H,'../../../silhouet/onderlaag_256.png')).convert('RGB'))
S=np.array([[c=='#' for c in l.rstrip('\n')] for l in open(os.path.join(H,'../../../silhouet/silhouet_bevroren.txt'))][:64])
wit=(on.min(axis=2)>235).reshape(64,4,64,4).sum(axis=(1,3))>=8
wit&=S; wit[44:,:]=False if False else wit[44:,:]
kz=np.zeros((64,64),bool); kz[34:50,2:28]=True
print('maan onderlaag (4:1, wit):',int((wit&kz).sum()))
for n,im in (('ronde1',a),('ronde2',b)):
    print(n,'wit w:',int(((im==8)&kz).sum()),'w+zilverlila n:',int((((im==8)|(im==7))&kz).sum()))
print('overlap maan ronde2/onderlaag:',int((((b==8)|(b==7))&kz&wit).sum()))
