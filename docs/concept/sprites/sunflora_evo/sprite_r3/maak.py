# r3: lijf (kale verkleining, evt. met gedraaide voeten) + technisch opschonen + r1-hoofd ervoor.
# Opschonen (regels, geen handwerk): (1) groene vlekjes <3 px -> meest voorkomende groene buur;
# (2) groene randpixels (grenzen aan transparant): alleen boven/links open -> donkergroen (selout), anders zwart;
# (3) losse zwarte pixels zonder groene buur -> weg (resten van de r12-kopomlijning).
import sys, numpy as np; from PIL import Image; from scipy import ndimage; from pal import PAL
L0=np.load(sys.argv[1]); OUT=sys.argv[2]
kop=np.load('../sprite_r2/kop_r1.npy'); L=L0.copy(); log={}
def add(k,n): log[k]=log.get(k,0)+n
for y,x in zip(*np.where(L==1)):
    nb=L[max(0,y-1):y+2,max(0,x-1):x+2]
    if not np.isin(nb,[11,12,13]).any(): L[y,x]=0; add('losse zwarte pixel weg',1)
for it in range(3):
    for k in (11,12,13):
        lab,n=ndimage.label(L==k)
        for l in range(1,n+1):
            ys,xs=np.where(lab==l)
            if len(ys)>=3: continue
            for y,x in zip(ys,xs):
                nb=[L[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<64 and 0<=xx<64 and L[yy,xx] in (11,12,13) and L[yy,xx]!=k]
                if nb: L[y,x]=max(set(nb),key=nb.count); add('groen vlekje <3 px samengevoegd',1)
vis=lambda y,x: 0<=y<64 and 0<=x<64 and L[y,x]==0 and kop[y,x]==0
for y,x in zip(*np.where(np.isin(L,[12,13]))):
    up,lf,dn,rt=vis(y-1,x),vis(y,x-1),vis(y+1,x),vis(y,x+1)
    if dn or rt: L[y,x]=1; add('groene rand -> zwart (schaduwkant)',1)
    elif up or lf: L[y,x]=11; add('groene rand -> donkergroen (lichtkant)',1)
C=np.where(kop>0,kop,L)
np.save(OUT+'.npy',C); np.save(OUT+'_lijf.npy',L)
im=Image.fromarray(C,'P'); im.putpalette([v for c in PAL for v in c]); im.save(OUT+'.png',transparency=0)
Image.open(OUT+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(OUT+'_8x.png')
zicht=(L>0)&(kop==0); zicht0=(L0>0)&(kop==0)
print(OUT,log,'| zichtbare lijfpixels',zicht.sum(),'afwijkend van kaal (zichtbaar):',int(((L!=L0)&(zicht|zicht0)).sum()))
