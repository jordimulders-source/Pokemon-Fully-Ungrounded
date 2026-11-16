# Jordi (16 nov): "beter, ik vind het vuurwerk onderin er mooi uit zien, maar het lijkt nog niet echt een verband te hebben met de rest van de sprite he"
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
src=Image.open('../r18/sprite_2_ook_linksonder_verschoven.png'); a0=np.array(src); pal=src.getpalette()
lab,n=ndimage.label(a0>0); main=np.bincount(lab.ravel())[1:].argmax()+1
bl=np.zeros_like(a0,bool)
for i in range(1,n+1):
    if i==main: continue
    c=lab==i
    if set(np.unique(a0[c]))<={6,7,8} and np.argwhere(c)[:,0].min()>=25: bl|=c
ys,xs=np.where(bl); print('barst bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
def save(a,k):
    im=Image.fromarray(a,'P'); im.putpalette(pal); im.save(f'sprite_{k}.png',transparency=0); return f'sprite_{k}.png'
def verschuif(dx,dy):
    a=a0.copy(); a[bl]=0
    for y,x in zip(ys,xs):
        Y,X=y+dy,x+dx
        if 0<Y<63 and 0<X<63 and a[Y,X]==0: a[Y,X]=a0[y,x]
    return a
outs=[('nu (r18 2)','../r18/sprite_2_ook_linksonder_verschoven.png')]
# A/B: barst omhoog tegen de onderkant van de kop, alsof hij uit de bek/kop knalt (achter de kop langs)
outs.append(('A: barst 6 px omhoog',save(verschuif(1,-6),'A')))
outs.append(('B: barst 10 px omhoog',save(verschuif(2,-10),'B')))
# C: vonkenspoor van het vlamslipje bij de bek naar het midden van de barst
a=a0.copy()
cx,cy=int(round(xs.mean())),int(round(ys.mean()))
spoor=[(7,31),(8,33),(9,35),(10,37)]
for (x,y) in spoor:
    if a[y,x]==0: a[y,x]=8 if (x+y)%2 else 7
outs.append(('C: vonkenspoor bek -> barst',save(a,'C')))
print('midden barst',cx,cy)
S=6; W=Image.new('RGB',(16+len(outs)*(64*S+20),64*S+60+140),(235,235,235)); d=ImageDraw.Draw(W)
for i,(k,f) in enumerate(outs):
    r=Image.open(f).convert('RGBA'); x=16+i*(64*S+20); d.text((x,4),k,fill=(0,0,0))
    for j,c in enumerate([(255,255,255),(40,40,48)]):
        b=Image.new('RGBA',r.size,c+(255,)); b.alpha_composite(r)
        if j==0: W.paste(b.resize((64*S,64*S),Image.NEAREST).convert('RGB'),(x,20))
        W.paste(b.resize((128,128),Image.NEAREST).convert('RGB'),(x+j*140,64*S+40))
W.save('vel.png')
