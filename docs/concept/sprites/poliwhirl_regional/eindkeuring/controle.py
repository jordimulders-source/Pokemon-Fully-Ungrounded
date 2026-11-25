import numpy as np
from PIL import Image
from zones import *
im,a=laad(); b=np.array(Image.open('poliwhirl_regional_ek.png'))
F=bevroren(a)
assert Image.open('poliwhirl_regional_ek.png').getpalette()[:48]==im.getpalette()[:48]
print('alpha-diff', int(((a==0)!=(b==0)).sum()))
print('bevroren zone diff', int((F&(a!=b)).sum()), 'van', int(F.sum()), 'px')
mat=lambda v: np.select([np.isin(v,YEL),np.isin(v,ICE),np.isin(v,DARK),np.isin(v,RED),v==1],[1,2,3,4,5],0)
ch=(a!=b); ma,mb=mat(a),mat(b)
ok=(ma==mb)|((ma==5)&np.isin(mb,[1,2]))   # lijnpixel -> outline base eigen materiaal (geel 7 = mat1, ijs b = mat2)
print('materiaalwissels buiten lijn->outline base:', int((ch&~ok).sum()))
print('gewijzigd totaal', int(ch.sum()))
for z,(y0,y1) in {'kop (r12-29)':(12,30),'romp/armen (r30-42)':(30,43),'benen/voeten (r43-58)':(43,59)}.items():
    print(' ',z, int(ch[y0:y1].sum()))
for (p,q),n in sorted({(int(x),int(y)):0 for x,y in zip(a[ch],b[ch])}.items()):
    print('  %x->%x: %d'%(p,q,int(((a==p)&(b==q)).sum())))
print('kleuren gebruikt (incl. transparant):', len(np.unique(b)), '/ palet 16')
print('zwart (1):', int((a==1).sum()),'->',int((b==1).sum()), 'van', int((b>0).sum()))
for k,v in ((5,'geel licht'),(6,'geel'),(7,'geel donker')):
    print(' %s: %d -> %d'%(v,(a==k).sum(),(b==k).sum()))
def clusters(m):
    seen=np.zeros(m.shape,bool); out=[]
    for y,x in np.argwhere(m):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            j,i=st.pop(); c.append((i,j))
            for dj,di in ((1,0),(-1,0),(0,1),(0,-1)):
                J,I=j+dj,i+di
                if 0<=J<64 and 0<=I<64 and m[J,I] and not seen[J,I]: seen[J,I]=True; st.append((J,I))
        out.append(c)
    return out
print('7-clusters <3 px (x,y):', [c for c in clusters(b==7) if len(c)<3])
