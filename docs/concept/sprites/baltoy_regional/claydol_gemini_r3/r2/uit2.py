# Opslaan r2 + diff-bewijs + vel.
import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r2')
from PIL import Image, ImageDraw
import bouw
from bouw2 import S, G3, ZONE, log
from cc import label
from kaal3 import kaal
bouw.P3[12]=(190,92,84)          # 4. lichtrood: naar de modeltint (model gemiddeld 186,89,80); donkerrood 13 blijft
used=bouw.opslaan(S,'r2/claydol_g3r2.png'); rgb=bouw.rgb
rgb(S).resize((512,512),0).save('r2/claydol_g3r2_8x.png')
# --- diff-bewijs: elke gewijzigde pixel ligt in een benoemde zone
diff=S!=G3; Z=np.zeros((64,64),bool)
for m in ZONE.values(): Z|=m
print('kleuren',len(used),'| pixels gewijzigd',diff.sum(),'| buiten de zones',(diff&~Z).sum())
from collections import Counter
print('per zone',Counter(z for z,*_ in log))
# tinten per groep
comp,n=label(S>0,diag=True); print('componenten (8-buur)',n,[int((comp==i).sum()) for i in range(1,n+1)])
big=np.bincount(comp.ravel())[1:].argmax()+1; Q=np.argwhere(comp==big)
for i in range(1,n+1):
    if i!=big: P=np.argwhere(comp==i); print(' staf',i,'min Chebyshev-afstand',np.abs(P[:,None,:]-Q[None]).max(2).min())
from creme import cremeMasker
M=cremeMasker(S)
print('tinten in creme-objecten',dict(Counter(S[M].tolist())),'| steen (hoofd, buiten creme)',dict(Counter(S[(comp==big)&~M].tolist())))
for v in (4,5,6,7,8):
    Lv,_=label(S==v); sz=np.bincount(Lv.ravel())[1:]; print(' tint',v,'clusters<3 (4-buur):',int((sz<3).sum()),end=';')
print()
# --- vel
S0,A,*_=kaal(); M8=Image.fromarray(A.astype('uint8'))
G=Image.new('RGB',(1600,1500),(236,236,236)); d=ImageDraw.Draw(G)
G3img=rgb(G3,(255,255,255)); bouw.P3[12]=(220,90,86); G3img=rgb(G3); bouw.P3[12]=(190,92,84)
for i,(t,im) in enumerate([('r2 (8x)',rgb(S)),('g3 (8x)',G3img),('model r3 geschrapt (8x)',M8)]):
    d.text((10+i*530,5),t,fill=(0,0,0)); G.paste(im.resize((512,512),0),(10+i*530,20))
def zm(Sx,y0,y1,x0,x1,s,img=None):
    im=img if img is not None else rgb(Sx,(200,220,200)); return im.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),0)
y=545; d.text((10,y),'onderkop 12x: r2 | g3 | model',fill=(0,0,0))
for i,im in enumerate([zm(S,29,40,8,50,12),zm(G3,29,40,8,50,12,G3img),zm(None,29,40,8,50,12,M8)]): G.paste(im,(10,y+15+i*140))
y2=y+15+3*140+10; d.text((10,y2),'rechterstaf kop 12x: r2 | g3 | model',fill=(0,0,0))
for i,im in enumerate([zm(S,32,50,46,64,12),zm(G3,32,50,46,64,12,G3img),zm(None,32,50,46,64,12,M8)]): G.paste(im,(10+i*230,y2+15))
d.text((720,y2),'1x licht / donker',fill=(0,0,0))
Image.open('r2/claydol_g3r2.png').save('/tmp/_r2.png'); sp=Image.open('/tmp/_r2.png').convert('RGBA')
for i,bg in enumerate([(255,255,255),(48,48,56)]):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(sp); G.paste(b.convert('RGB'),(720+i*80,y2+15))
G=G.crop((0,0,1600,y2+15+18*12+10)); G.save('r2/vel.png'); print(G.size)
