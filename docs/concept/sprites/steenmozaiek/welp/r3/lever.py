# Leveren: 64x64 indexed PNG's, 8x, vel.png, diff-telling per zone t.o.v. r2
import numpy as np
from PIL import Image, ImageDraw
from toon import big, rgba
FIN=np.load('FIN2.npy')
def png64(a,fn):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in FIN[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(fn,transparency=0); return full
r2=np.load('welp_r2.npy')
for k in ('A','B'):
    a=np.load(f'welp_r3_{k}.npy'); png64(a,f'welp_r3_{k}.png')
    big(a,8,(255,255,255,255)).save(f'welp_r3_{k}_8x.png')
    for sh in (1,2): png64(np.load(f'welp_r3_{k}_oog{sh}.npy'),f'welp_r3_{k}_oog{sh}.png')
    H,W=a.shape; Z=np.full((H,W),'lijf',object)
    for y in range(H):
        for x in range(W):
            if y<=22 and x<=27: Z[y,x]='kop'
            elif x<=12 and 22<y<=30: Z[y,x]='poten'
            elif y>=39 and x<=41: Z[y,x]='poten'
            elif x>=44: Z[y,x]='staart'
    dm=a!=r2; print(k,'t.o.v. r2',{z:int((dm&(Z==z)).sum()) for z in ('kop','lijf','poten','staart')},'som',int(dm.sum()),
          'kleuren',len(set(a.ravel())-{0}),'silhouet-diff',int(((a>0)!=(r2>0)).sum()))
# model verkleind
n=Image.open('natief.png').convert('RGBA'); X0=Y0=2; s=3.3
mod=n.crop((X0,Y0,int(X0+50*s),int(Y0+45*s))).resize((50,45),Image.BOX)
modbig=Image.new('RGBA',(400,360),(235,235,225,255)); modbig.alpha_composite(mod.resize((400,360),Image.NEAREST))
A=np.load('welp_r3_A.npy'); B=np.load('welp_r3_B.npy')
row1=[(big(A,8),'r3 heup A (dij + cremekrul, model)'),(big(B,8),'r3 heup B (dij + spiraal als schouder)'),(big(r2,8),'r2'),(modbig,'model verkleind 50x45, 8x')]
# kop 12x: model + 3 oogvarianten
box=(0,0,26,16)
kmod=n.crop((int(X0+box[0]*s),int(Y0+box[1]*s),int(X0+box[2]*s),int(Y0+box[3]*s))).resize((26*12,16*12),Image.LANCZOS)
row2=[(kmod,'model kop')]
for f,l in (('welp_r3_A.npy','oog huidig (modelplek)'),('welp_r3_A_oog1.npy','oog 1 px links'),('welp_r3_A_oog2.npy','oog 2 px links')):
    row2.append((big(np.load(f)[box[1]:box[3],box[0]:box[2]],12),l))
ones=[]
for arr in (A,B):
    for bg in ((248,248,240,255),(40,44,52,255)):
        im=Image.new('RGBA',(64,64),bg); h,w=arr.shape; im.alpha_composite(rgba(arr),((64-w)//2,63-h)); ones.append(im)
W1=sum(i.width+20 for i,_ in row1); W2=sum(i.width+20 for i,_ in row2)
V=Image.new('RGBA',(max(W1,W2),20+360+40+192+40+64+10),(255,255,255,255)); d=ImageDraw.Draw(V)
x=0
for im,l in row1: V.alpha_composite(im,(x,18)); d.text((x,3),l,fill=(0,0,0)); x+=im.width+20
x=0; y=18+360+30
for im,l in row2: V.alpha_composite(im,(x,y)); d.text((x,y-15),l,fill=(0,0,0)); x+=im.width+20
y+=192+30; d.text((0,y-15),'1x: A licht, A donker, B licht, B donker',fill=(0,0,0))
for k,im in enumerate(ones): V.alpha_composite(im,(k*84,y))
V.save('vel.png'); print(V.size)
