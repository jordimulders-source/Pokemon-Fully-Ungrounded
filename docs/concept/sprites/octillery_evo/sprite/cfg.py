# gedeelde instellingen: model, schaal, palet, raster <-> png
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/octillery_evo/'
MODEL=D+'referenties/ontwerp_gekozen.png'
X0,X1,Y0,Y1=149,1003,40,597          # inhoud model
W=62; S=(X1-X0)/W; H=int(np.ceil((Y1-Y0)/S)); TOP=64-H+1; LEFT=1
CH='.123456789abcdef'
PAL=[(255,0,255),
 (36,12,14),    #1 omlijning
 (112,26,34),   #2 donkerrood (achterste delen)
 (152,40,44),   #3 rood schaduw
 (190,62,56),   #4 rood mid
 (222,98,84),   #5 rood licht
 (246,152,128), #6 rood hooglicht
 (146,74,80),   #7 roze donker / ribbel
 (190,112,108), #8 roze mid
 (226,158,146), #9 roze licht
 (176,128,32),  #a geel donker
 (232,196,64),  #b geel mid
 (252,240,160), #c geel licht
 (128,116,116), #d grijs licht
 (64,56,58),    #e grijs donker
 (76,16,24)]    #f binnenlijn rood

def model():
    return np.asarray(Image.open(MODEL).convert('RGB')).astype(int)
def cell(x,y):
    """modelpixels-slices voor spritepixel x,y"""
    bx=X0+(x-LEFT)*S; by=Y0+(y-TOP)*S
    return slice(int(round(by)),int(round(by+S))),slice(int(round(bx)),int(round(bx+S)))
def fgmask(c):
    lum=c.mean(2); sat=c.max(2)-c.min(2); return (lum<235)|(sat>20)
def read(p):
    R=[l.rstrip('\n') for l in open(p)]
    return np.array([[CH.index(ch) for ch in r.ljust(64,'.')[:64]] for r in R[:64]])
def write(a,p):
    open(p,'w').write('\n'.join(''.join(CH[v] for v in r) for r in a)+'\n')
def topng(a,p):
    im=Image.fromarray(a.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; im.putpalette(pal+[0]*(768-len(pal)))
    im.info['transparency']=0; im.save(p,transparency=0)
def rgba(a,bg=None):
    o=np.zeros((64,64,4),'uint8')
    for i,c in enumerate(PAL):
        o[a==i,:3]=c; o[a==i,3]=255
    o[a==0,3]=0
    im=Image.fromarray(o)
    if bg: b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im); return b.convert('RGB')
    return im
def model64():
    """model BOX-verkleind naar 64x64 op dezelfde plek"""
    src=Image.open(MODEL).convert('RGB')
    big=Image.new('RGB',(int(64*S)+40,int(64*S)+40),(254,254,254))
    ox=int(X0-LEFT*S); oy=int(Y0-TOP*S)
    big.paste(src,(-ox,-oy))
    return big.crop((0,0,int(round(64*S)),int(round(64*S)))).resize((64,64),Image.BOX)
