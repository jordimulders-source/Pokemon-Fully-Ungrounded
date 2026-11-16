# r9: kleine geest + schoorsteenrand exact 1-op-1 uit het natieve model (geen duplicaten), incl. de eigen hals van de geest.
# Natieve rijen r6-r18, r20-r25, r28 -> sprite y0-19 (geschrapt: r19 = egale lijfrij, r26 = tweede lip-rij, r27 = halsrij
# schoorsteen); kolommen x -> x-15. Rij 20+ (ketel) en alles buiten deze zone = r8 (bevroren).
from PIL import Image; import numpy as np
n=np.array(Image.open('model/natief.png').convert('RGB')).astype(int)
im=Image.open('sprite_r8/sprite.png'); pal=im.getpalette(); r8=np.array(im)
P=np.array(pal[:14*3]).reshape(14,3)
RIJEN=list(range(6,19))+list(range(20,26))+[28]; DX=-15; NX0,NX1=22,63
IJZER=[1,7,8,9,10,11,12]; GROEN={2,3,4,5,6,13}
# 1) natieve klassen
H=len(RIJEN); Wd=NX1-NX0
k=[['.']*Wd for _ in range(H)]
for j,r in enumerate(RIJEN):
    for i in range(Wd):
        c=n[r,NX0+i]
        if c.min()>235: continue
        if c[1]>c[0]+25:
            k[j][i]='6' if c[1]<150 else ('5' if c[1]<214 else '2')
        elif c.min()>200 and r<=12: k[j][i]='W'           # glimp in het oog
        else:
            d=((P[IJZER]-c)**2).sum(1); k[j][i]='%X'%IJZER[int(np.argmin(d))]
# 2) ruis buiten het gezicht (als r6/r8, natieve coordinaten) en witte gatpixel lijf/arm
def zet(x,r,c):
    if r in RIJEN: k[RIJEN.index(r)][x-NX0]=c
for x,r,c in [(31,17,'5'),(39,18,'5'),(46,20,'6')]: zet(x,r,c)
# vage restpixels voorbij de staartpunt (natief x>=60; staart eindigt op x56-59 met het tikje omhoog)
for j in range(H):
    for i in range(60-NX0,Wd): k[j][i]='.'
# 3) donkergroene buitenlijn: groen naast leeg -> 6 (niet naast schoorsteen)
k0=[row[:] for row in k]
for j in range(H):
    for i in range(Wd):
        if k0[j][i] in '52W':
            for di,dj in((1,0),(-1,0),(0,1),(0,-1)):
                ii,jj=i+di,j+dj
                if not(0<=ii<Wd and 0<=jj<H) or k0[jj][ii]=='.': k[j][i]='6'; break
open('sprite_r9/natief_zone.txt','w').write('\n'.join('%2d '%r+''.join(row) for r,row in zip(RIJEN,k))+'\n')
# 4) plakken
a=r8.copy()
for y in range(0,17):
    for x in range(0,53):   # oude r8-geest (tot staartpunt x52) weg
        if a[y,x] in GROEN: a[y,x]=0
for y in range(14,20):
    for x in range(8,24):
        if a[y,x] in IJZER: a[y,x]=0
for j in range(H):
    for i in range(Wd):
        ch=k[j][i]; x=NX0+i+DX; y=j
        if ch=='.' or not(0<=x<64): continue
        if y>=17 and a[y,x] in GROEN and x>=23: continue     # bevroren wolk wint
        a[y,x]={'6':6,'5':5,'2':2,'W':13}.get(ch) or int(ch,16)
# 5) keuring r8 MOET 3 en 4
F=[(5,38,8),(15,38,8),(2,31,8),(2,38,8),(17,39,8),(20,37,8),(12,41,6),(5,44,2),(7,45,8),(18,30,1),(8,21,9),
   (3,25,9),(13,19,9),(22,17,1),(1,56,1)]
for x,y,v in F:
    if not (14<=y<=19 and 8<=x<=23): a[y,x]=v                 # schoorsteenpixels zijn nu nieuw uit het model
    else: print('MOET-pixel in nieuwe schoorsteen, nu:',(x,y),'%X'%a[y,x])
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r9/sprite.png',transparency=0)
Yg,Xg=np.mgrid[0:64,0:64]; zone=(Yg<=19)&(Xg<=52)
fx=np.zeros((64,64),bool)
for x,y,v in F: fx[y,x]=True
print('diff t.o.v. r8 buiten geest/schoorsteen-zone en MOET-pixels:',int(((a!=r8)&~zone&~fx).sum()))
for y in range(0,21): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in a[y,6:48]))
