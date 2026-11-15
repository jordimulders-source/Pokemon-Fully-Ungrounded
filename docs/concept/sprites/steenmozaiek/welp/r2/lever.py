# Levert de 64x64 indexed PNG's, 8x-vergrotingen, het vel en de zone-telling.
import numpy as np
from PIL import Image, ImageDraw
from toon import rgba
from reduceer import X0,X1,Y0,Y1
FIN=np.load('FIN2.npy')
def png64(a,fn):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in FIN[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(fn,transparency=0)
    return full
kaal=np.load('kaal_50.npy'); ond=np.load('onderlaag_50.npy'); zon=np.load('welp_r2_zonder_extra.npy'); fin=np.load('welp_r2.npy')
png64(ond,'onderlaag.png'); fz=png64(zon,'welp_r2_zonder_extra.png'); ff=png64(fin,'welp_r2.png')
for fn in ('welp_r2.png','welp_r2_zonder_extra.png'):
    im=Image.open(fn).convert('RGBA'); bg=Image.new('RGBA',(512,512),(255,255,255,255)); bg.alpha_composite(im.resize((512,512),Image.NEAREST)); bg.save(fn.replace('.png','_8x.png'))
# zones
H,W=fin.shape; Z=np.full((H,W),'lijf',object)
for y in range(H):
    for x in range(W):
        if y<=22 and x<=27: Z[y,x]='kop'
        elif x<=12 and 22<y<=30: Z[y,x]='poten'
        elif y>=36 and x<=41: Z[y,x]='poten'
        elif x>=42: Z[y,x]='staart'
for nm,a,b in (('opschonen (kaal->onderlaag)',kaal,ond),('reparaties (onderlaag->zonder_extra)',ond,zon),('totaal zonder_extra vs kaal',kaal,zon),('bovenlaag (zonder_extra->r2)',zon,fin),('totaal r2 vs kaal',kaal,fin)):
    dmask=a!=b; print(nm,{z:int((dmask&(Z==z)).sum()) for z in ('kop','lijf','poten','staart')},'som',int(dmask.sum()))
print('silhouet gelijk aan kale reductie:',((kaal>0)==(fin>0)).all(),' kleuren r2:',len(set(fin.ravel())-{0}),'+ transparant')
# tinten per groep
names='. K d s m l p q r g W c T G'.split()
print('gebruikte kleuren:',[names[v] for v in sorted(set(fin.ravel()))])
# kleine clusters < 3 px binnen bruin
def clusters(a,vals):
    seen=np.zeros_like(a,bool); small=[]
    for j in range(H):
        for i in range(W):
            if seen[j,i] or a[j,i] not in vals: continue
            st=[(j,i)]; seen[j,i]=True; cl=[]
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==a[j,i]: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)<3: small.append((a[j,i],cl))
    return small
print('bruinclusters <3 px in r2:',len(clusters(fin,{3,4,5})),' in zonder_extra:',len(clusters(zon,{3,4,5})))
# vel
S8=8
def big(a,z,bgc=(235,235,225,255)):
    im=rgba(a); o=Image.new('RGBA',(im.width*z,im.height*z),bgc); o.alpha_composite(im.resize(o.size,Image.NEAREST)); return o
n=Image.open('natief.png').convert('RGBA')
mod=n.crop((int(X0),int(Y0),int(X1),int(Y1)))
mod50=mod.resize((50,45),Image.BOX)
modbig=Image.new('RGBA',(400,360),(235,235,225,255)); modbig.alpha_composite(mod50.resize((400,360),Image.NEAREST))
row1=[big(fin,S8),big(zon,S8),modbig]
lab1=['welp_r2 (met extra spiralen)','welp_r2_zonder_extra','model verkleind naar 50x45 (BOX), 8x']
# kop 12x
kopbox=(0,0,27,24); s=(X1-X0)/50
kmod=n.crop((int(X0+kopbox[0]*s),int(Y0+kopbox[1]*s),int(X0+kopbox[2]*s),int(Y0+kopbox[3]*s))).resize((27*12,24*12),Image.LANCZOS)
kspr=big(fin[kopbox[1]:kopbox[3],kopbox[0]:kopbox[2]],12)
row2=[kspr,kmod]; lab2=['kop welp_r2 12x','kop model zelfde uitsnede']
# 1x licht/donker
one=[]
for f in (ff,fz):
    for bgc in ((248,248,240,255),(40,44,52,255)):
        im=Image.new('RGBA',(64,64),bgc); a=f.copy(); im.alpha_composite(rgba(a)); one.append(im)
Wt=max(sum(i.width+20 for i in row1),sum(i.width+20 for i in row2)+4*84)
Ht=360+30+288+30+20
V=Image.new('RGBA',(Wt,Ht),(255,255,255,255)); d=ImageDraw.Draw(V); x=0
for im,l in zip(row1,lab1): V.alpha_composite(im,(x,20)); d.text((x,4),l,fill=(0,0,0)); x+=im.width+20
x=0; y=20+360+30
for im,l in zip(row2,lab2): V.alpha_composite(im,(x,y)); d.text((x,y-16),l,fill=(0,0,0)); x+=im.width+20
d.text((x,y-16),'1x: r2 licht/donker, zonder_extra licht/donker',fill=(0,0,0))
for k,im in enumerate(one): V.alpha_composite(im,(x+k*84,y))
V.save('vel.png'); print('vel',V.size)
