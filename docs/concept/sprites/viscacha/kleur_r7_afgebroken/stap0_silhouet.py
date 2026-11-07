"""Stap 0 r7: silhouet uit het Gemini-masker op r6-schaal (meta.npy), dekking >= 0,35 (r6 nam het lichaam na opening, >= 0,5: daardoor vielen de zwarte buitenlijnen van oren, rug en staart weg).
Dunne delen (snorharen, rafels) als '+' bij dekking >= 0,12. Uitvoer: silhouet_r7.txt"""
import numpy as np
from PIL import Image
from scipy import ndimage as nd
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
im=np.array(Image.open(D+'referenties/gemini_gekozen_ronde6.png').convert('RGB')).astype(int)
m=nd.binary_fill_holes(np.abs(im-255).sum(2)>60)
lab,n=nd.label(m,structure=np.ones((3,3))); sz=nd.sum(m,lab,range(1,n+1)); m=np.isin(lab,1+np.where(sz>40)[0])
body=nd.binary_opening(m,structure=np.ones((5,5)))
lab2,n2=nd.label(body); body=lab2==(1+np.argmax(nd.sum(body,lab2,range(1,n2+1))))
X0,Y0,S,ox,oy=np.load(D+'kleur_r7/meta.npy')
out=[]
for y in range(64):
    s=''
    for x in range(64):
        ys,ye=int(Y0+(y-oy)*S),int(Y0+(y-oy+1)*S); xs,xe=int(X0+(x-ox)*S),int(X0+(x-ox+1)*S)
        if ys<0 or xs<0 or ye>im.shape[0] or xe>im.shape[1] or ye<=ys: s+='.'; continue
        cb=body[ys:ye,xs:xe].mean(); cm=m[ys:ye,xs:xe].mean()
        s+= '#' if cb>=0.35 else ('+' if cm>=0.12 else '.')
    out.append(s)
open(D+'kleur_r7/silhouet_r7.txt','w').write('\n'.join(out)+'\n')
a=[l.rstrip('\n') for l in open(D+'kleur_r7/silhouet_auto.txt')]
print('t.o.v. r6-silhouet: erbij',sum(out[y][x]=='#' and a[y][x]!='#' for y in range(64) for x in range(64)),'weg',sum(out[y][x]!='#' and a[y][x]=='#' for y in range(64) for x in range(64)))
