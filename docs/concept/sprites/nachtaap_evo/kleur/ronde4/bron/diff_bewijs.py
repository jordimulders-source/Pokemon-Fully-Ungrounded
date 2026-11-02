# ronde3 t.o.v. ronde2: diff buiten zone (x4-24, y36-46) moet 0 zijn; maan nagemeten tegen de onderlaag
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
a=np.array(Image.open(os.path.join(H,'../../ronde3/nachtaap.png'))); b=np.array(Image.open(os.path.join(H,'../nachtaap.png')))
z=np.zeros((64,64),bool); z[36:49,4:25]=True
print('palet gelijk:',Image.open(os.path.join(H,'../../ronde3/nachtaap.png')).getpalette()[:48]==Image.open(os.path.join(H,'../nachtaap.png')).getpalette()[:48])
print('diff buiten zone:',int(((a!=b)&~z).sum()),'| gewijzigd in zone:',int(((a!=b)&z).sum()))
on=np.array(Image.open(os.path.join(H,'../../../silhouet/onderlaag_256.png')).convert('RGB'))
wit=(on.min(axis=2)>235).reshape(64,4,64,4).sum(axis=(1,3))>=8
S=np.array([[c=='#' for c in l.rstrip('\n')] for l in open(os.path.join(H,'../../../silhouet/silhouet_bevroren.txt'))][:64])
k=np.zeros((64,64),bool); k[34:50,2:28]=True; wit&=S&k
for n,im in (('ronde2',a),('ronde3',b)):
    m=((im==8)|(im==7))&k
    col=[int(m[36:47,x].sum()) for x in (12,13,14)]
    print(n,'maan w+n:',int(m.sum()),'overlap onderlaag:',int((m&wit).sum()),'| maandikte midden x12-14:',col)
print('onderlaag wit:',int(wit.sum()),'| dikte midden x12-14:',[int(wit[36:47,x].sum()) for x in (12,13,14)])
