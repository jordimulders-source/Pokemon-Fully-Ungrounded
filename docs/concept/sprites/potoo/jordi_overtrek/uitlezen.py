"""Jordi's overtrek (overtrek_v1.webp, getekend op tekenbasis/leidraad_gespiegeld_spritepixelraster.png) letterlijk uitlezen.
Registratie: rasterpixel = J/1.25 + (181,185); spritevak (1 vak = 1 pixel) = J/22.5 + (10.06,10.28).
Lijn = pixels die in J donker zijn en in de leidraadfoto niet (zonder rasterlijnen). De halslijn loopt over donkere veren
en is met de hand afgelezen op 3-4x vergrotingen van zijn lijn (punten hieronder, J-coördinaten). Het oog komt van de fotopositie."""
import json, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy import ndimage as nd
J=np.array(Image.open('overtrek_v1.webp').convert('L')).astype(float); h,w=J.shape
P=ImageOps.mirror(Image.open('../tekenbasis/leidraad_origineel_zonder_raster.png').convert('L'))
Pc=np.array(P.transform((w,h),Image.AFFINE,(1/2.5,0,90.5,0,1/2.5,92.5),resample=Image.BILINEAR)).astype(float)
X=np.arange(w); Y=np.arange(h)
dc=np.abs(((X-21+11.25)%22.5)-11.25); dr=np.abs(((Y-17.5+11.25)%22.5)-11.25)
grid=(dc[None,:]<=1.5)|(dr[:,None]<=1.5)
c=(J<110)&(Pc-J>40)&~grid; c[:33]=False; c[936:]=False
D=nd.binary_dilation(c,iterations=4); lab,n=nd.label(D); sz=nd.sum(c,lab,range(1,n+1))
c&=np.isin(lab,1+np.where(sz>=15)[0])
# zijn oog-cirkel eruit (oog komt van de foto)
OOG_J=((261.67*2-181)*1.25,(223.33*2-185)*1.25,29*2.5,27*2.5)
ox,oy,rx,ry=OOG_J
eye=((X[None,:]-ox)/(rx+22))**2+((Y[:,None]-oy)/(ry+22))**2<=1
c&=~eye
c[:75,:300]=False; c[:75,720:]=False
HALS=[(735,416),(735,476),(734,530),(733,553),(727,575),(702,622),(674,669),(654,695),(642,710),(631,725),(621,740),(594,770),
      (585,780),(567,802),(547,827),(536,841),(523,856),(510,863),(470,897),(427,912),(383,912),(360,912)]
# onderkaak en punt lopen over donkere ondergrond: met de hand afgelezen op 3x (zoom 280-600 x 780-948)
KAAK_BUITEN=[(260,842),(280,865),(313,895),(360,925)]
BEK_RECHTS=[(433,780),(423,800),(400,818),(380,835),(363,867),(360,890),(360,925)]
im=Image.fromarray(np.where(c,255,0).astype(np.uint8)); dd=ImageDraw.Draw(im)
for L in (HALS,KAAK_BUITEN,BEK_RECHTS): dd.line(L,fill=255,width=2)
c=np.array(im)>0
from skimage.morphology import skeletonize
# gaatjes (rasterkruisingen, donkere ondergrond) dichten en terug naar een dunne lijn
c=skeletonize(nd.binary_closing(nd.binary_dilation(c,iterations=3),structure=np.ones((13,13))))
lab,n=nd.label(c,structure=np.ones((3,3))); sz=nd.sum(c,lab,range(1,n+1)); c&=np.isin(lab,1+np.where(sz>=40)[0])
ys,xs=np.nonzero(c)
cx=np.floor(xs/22.5+10.06).astype(int); cy=np.floor(ys/22.5+10.28).astype(int)
from collections import Counter
cnt=Counter(zip(cx.tolist(),cy.tolist()))
cells=set(k for k,v in cnt.items() if v>=1)
# 1 pixel dik: een vak weg als zijn buren via een hoek al verbonden zijn (alleen hoekvakken van trapjes)
def nb(p): return [(p[0]+dx,p[1]+dy) for dx in (-1,0,1) for dy in (-1,0,1) if (dx,dy)!=(0,0)]
for p in sorted(cells):
    x,y=p
    for a,b in (((x+1,y),(x,y+1)),((x-1,y),(x,y+1)),((x+1,y),(x,y-1)),((x-1,y),(x,y-1))):
        if a in cells and b in cells and (a[0]-x,b[1]-y) and (a[0],b[1]) not in cells:
            if p in cells and sum(q in cells for q in nb(p))==2: cells.discard(p)
cells=sorted(cells)
eyec=[(x,y) for y in range(0,64) for x in range(0,72) if ((x+.5-(ox/22.5+10.06))/(rx/22.5))**2+((y+.5-(oy/22.5+10.28))/(ry/22.5))**2<=1]
json.dump({'lijn':cells,'oog':eyec,'hals_J':HALS},open('omtrek_cellen.json','w'))
np.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/2279c649-e9c9-5a14-bfd8-565dc593363d/scratchpad/c_final.npy',c)
# vel: links zijn afbeelding met mijn uitlezing in rood, rechts de spritepixels
A=np.array(Image.open('overtrek_v1.webp').convert('RGB')); A=(A*0.5+127).astype(np.uint8); A[nd.binary_dilation(c)]=[220,0,0]
A=Image.fromarray(A); ImageDraw.Draw(A).ellipse([ox-rx,oy-ry,ox+rx,oy+ry],outline=(0,90,255),width=3)
R=Image.open('../tekenbasis/leidraad_gespiegeld_spritepixelraster.png').convert('RGB')
x0,y0,x1,y1=10,10,63,53
B=R.crop((x0*18,y0*18,x1*18,y1*18)); B=Image.blend(B,Image.new('RGB',B.size,(255,255,255)),0.6); d=ImageDraw.Draw(B)
for x,y in eyec: d.rectangle([(x-x0)*18+1,(y-y0)*18+1,(x-x0)*18+17,(y-y0)*18+17],fill=(0,0,0))
for x,y in cells: d.rectangle([(x-x0)*18+1,(y-y0)*18+1,(x-x0)*18+17,(y-y0)*18+17],fill=(200,0,0))
B=B.resize((int(B.size[0]*A.size[1]/B.size[1]),A.size[1]),Image.NEAREST)
W=Image.new('RGB',(A.size[0]+B.size[0]+20,A.size[1]+40),(255,255,255)); W.paste(A,(0,40)); W.paste(B,(A.size[0]+20,40))
d=ImageDraw.Draw(W); d.text((10,12),'jouw lijn zoals ik hem uitlees (rood); oog = fotopositie (blauw)',fill=(0,0,0))
d.text((A.size[0]+30,12),'dezelfde lijn in spritepixels (1 vak = 1 pixel), zwart = oog op fotopositie',fill=(0,0,0))
W.save('omtrek_check.png'); print(len(cells),'lijnpixels',len(eyec),'oogpixels')
