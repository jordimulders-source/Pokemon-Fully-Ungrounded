# controle.py: technische controles op gengas_r2.png (alleen meten)
import sys,math,numpy as np; sys.path.insert(0,'.')
from PIL import Image
from gezicht_px import face
from pal import PAL,CH
im=Image.open('gengas_r2.png'); a=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3)
H,W=a.shape
print('kleuren gebruikt (incl. 0):',len(set(a.flatten())),'| paletgrootte',len(PAL))
# 1) gezicht exact Gengar
G=np.array(Image.open('../../../../../graphics/pokemon/gengar/anim_front.png'))[:64]; gp=np.array(Image.open('../../../../../graphics/pokemon/gengar/anim_front.png').getpalette()[:48]).reshape(16,3)
f=face(); fout=0; n=0
for (x,y),v in f.items():
    if v in (1,2,3,5,6,7):
        n+=1
        if tuple(pal[a[y,x]])!=tuple(gp[v]): fout+=1; print('  gezicht wijkt af',x,y,'gengar',v,'sprite',a[y,x])
print(f'gezicht rood/wit/grijs: {n} px, afwijkend {fout}')
gez={(x,y) for (x,y),v in f.items() if v in (1,2,3,5,6,7)}
extra=[(x,y) for y in range(H) for x in range(W) if a[y,x] in (7,8,9,10,11,12) and (x,y) not in gez]
print('rood/tandkleur buiten het Gengar-gezicht:',extra)
# 2) vlakjes < 3 px per kleur (8-samenhang, randpixels/selout niet meegeteld), behalve omlijning 1, gezicht, glans
N8=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
def rand(x,y): return any(0<=Y<H and 0<=X<W and a[Y,X]==0 for Y,X in((y+1,x),(y-1,x),(y,x+1),(y,x-1))) or x in(0,W-1) or y in(0,H-1)
def comps(mask):
    seen=np.zeros_like(mask); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=1; c=[]
                while st:
                    yy,xx=st.pop(); c.append((xx,yy))
                    for dy,dx in N8:
                        Y,X=yy+dy,xx+dx
                        if 0<=Y<H and 0<=X<W and mask[Y,X] and not seen[Y,X]: seen[Y,X]=1; st.append((Y,X))
                out.append(c)
    return out
klein=[]
for k in range(2,16):
    if k in (7,8,9,10,11,12): continue
    for c in comps((a==k)&~np.array([[rand(x,y) for x in range(W)] for y in range(H)])):
        if len(c)<3 and not all(p in f for p in c): klein.append((CH[k],c))
print('vlakjes < 3 px (kleur, pixels):'); [print('  ',k,c) for k,c in klein]
# 3) losse omlijningspixels: index 1 zonder buur-1 (8-buren) 
los=[]
for y in range(H):
    for x in range(W):
        if a[y,x]==1:
            nb=[a[Y,X] for Y in range(max(0,y-1),min(H,y+2)) for X in range(max(0,x-1),min(W,x+2)) if (Y,X)!=(y,x)]
            if nb.count(1)==0: los.append((x,y))
            # omlijning die nergens aan transparant grenst en niet aan ander vlak: binnen een egaal vlak
            n4=[a[Y,X] for Y,X in((y+1,x),(y-1,x),(y,x+1),(y,x-1)) if 0<=Y<H and 0<=X<W]
            if 0 not in n4 and len(set(n4)-{1})==1 and n4.count(1)<=1 and (x,y) not in f: los.append(('in-vlak',x,y))
print('losse omlijningspixels:',los)
# lichte kleur op de buitenrand
licht=[(x,y,CH[a[y,x]]) for y in range(H) for x in range(W) if a[y,x] in (5,6,13) and any(0<=Y<H and 0<=X<W and a[Y,X]==0 for Y,X in((y+1,x),(y-1,x),(y,x+1),(y,x-1)))]
print('lichte tint aan de buitenrand:',licht)
# 4) rondheid bol: buitenrand-pixels van het silhouet in de zones zonder oren/ledematen
pts=[]
for y in range(23,58):
    xs=np.where(a[y]!=0)[0]
    for x in range(W):
        if a[y,x]!=0 and (x==0 or a[y,x-1]==0 or x==W-1 or a[y,x+1]==0 or a[y-1,x]==0 or (y+1<H and a[y+1,x]==0)):
            if 8<=x<=52 and not (x<=12 and 41<=y<=51) and not (x>=41 and y>=50) and not (x>=50 and y<=31): pts.append((x,y))
P=np.array(pts,float)
# cirkelfit (algebraisch)
A=np.c_[2*P[:,0],2*P[:,1],np.ones(len(P))]; b=(P**2).sum(1); cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; r=math.sqrt(c+cx*cx+cy*cy)
d=np.sqrt(((P-[cx,cy])**2).sum(1))-r
print(f'bol: cirkelfit middelpunt ({cx:.2f},{cy:.2f}) r {r:.2f}; randpunten {len(P)}; afwijking max {abs(d).max():.2f} px, gem {abs(d).mean():.2f} px')
