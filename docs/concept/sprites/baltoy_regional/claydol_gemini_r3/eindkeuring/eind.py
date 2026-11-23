# Eindkeuring (Dragonfly Cave) claydol_g3r4 -> claydol_eind: alleen uitvoeringspixels, silhouet en palet ongewijzigd.
import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r4')
from PIL import Image, ImageDraw
from cc import label
src=Image.open('r4/claydol_g3r4.png'); R4=np.array(src); S=R4.copy(); PAL=src.getpalette()
FIX=[ # (x,y,nieuw,reden)
 (35,6,7,'punt rechterrand: enige niet-zwarte pixel in de schaduwlijn'),
 (13,12,6+1,'krans-bolletje onderrand open in 6 -> zwart zoals de rest van de onderkant'),
 (9,13,5,'bolletje bovenrand: zwart midden in de lichte bovenlijn (7-6-7), model 121 -> 5'),
 (6,19,7,'bolletje linksonder: 7-6-7 om en om -> zwart'),
 (9,46,7,'linkerstaf rechterrand (schaduwkant): rood door de zwarte lijn, model zwart'),
 (9,47,7,'idem'),
 (53,52,6,'rechterstaf: lichtrood op de buitenrand -> lijntint 6 zoals de andere bandrijen'),
 (10,54,7,'linkerstaf: gat (5) in de zwarte linkerlijn'),
]+[(x,y,4,'linkerstaf-steel eentonig 5 -> lichte zijde 4 (model 133), zoals de rechterstaf') for x,y in [(9,51),(10,52),(10,53),(11,54),(11,55),(11,56),(12,57)]]
for x,y,v,r in FIX: S[y,x]=v
assert ((S>0)==(R4>0)).all() and set(np.unique(S))<=set(np.unique(R4))
_,n=label(S>0,diag=True); print('componenten (8-buur):',n)
d=np.argwhere(S!=R4); print('gewijzigd:',len(d))
def save(A,fn):
    im=Image.fromarray(A.astype('uint8'),'P'); im.putpalette(PAL); im.save(fn,transparency=0); return im
save(S,'eindkeuring/claydol_eind.png')
rgb=lambda A:Image.fromarray(np.array(PAL[:48],'uint8').reshape(16,3)[A])
rgb(S).resize((512,512),0).save('eindkeuring/claydol_eind_8x.png')
M=Image.open('gemini/../natief.png') if False else None
# vel: eind | r4 | model (8x), 1x licht/donker, diff
import os
NAT=Image.open('natief.png').convert('RGB'); nb=NAT.getbbox() if False else None
from natcoord import NY,NX,NAT as NA
Mm=np.full((64,64,3),255,'uint8'); ok=(NY>=0)&(S>0); Mm[ok]=NA[NY[ok],NX[ok]]
V=Image.new('RGB',(1600,760),(236,236,236)); dr=ImageDraw.Draw(V)
for i,(t,im) in enumerate([('eind',rgb(S)),('r4',rgb(R4)),('model per spritepixel',Image.fromarray(Mm))]):
    dr.text((10+i*530,5),t+' (8x)',fill=(0,0,0)); V.paste(im.resize((512,512),0),(10+i*530,20))
y=545; dr.text((10,y),'1x licht / donker: eind, r4',fill=(0,0,0))
for j,A in enumerate([S,R4]):
    sp=rgb(A).convert('RGBA'); sp.putalpha(Image.fromarray(((A>0)*255).astype('uint8')))
    for i,bg in enumerate([(255,255,255),(48,48,56)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(sp); V.paste(b.convert('RGB'),(10+j*160+i*72,y+15))
D=rgb(S).convert('L').point(lambda v:v//3+150).convert('RGB'); Dp=D.load()
for yy,xx in d: Dp[int(xx),int(yy)]=(220,0,0)
dr.text((340,y),'diff eind vs r4 (rood, 3x)',fill=(0,0,0)); V.paste(D.resize((192,192),0),(340,y+15))
V.save('eindkeuring/vel.png')
