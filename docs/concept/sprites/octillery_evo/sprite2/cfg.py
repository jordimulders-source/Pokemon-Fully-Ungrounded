# gedeelde instellingen sprite 2 (model_v4): model, schaal, palet, raster <-> png
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/octillery_evo/'
MODEL=D+'referenties/model_v4.png'
X0,X1,Y0,Y1=147,871,182,837          # inhoud model
W=62; S=(X1-X0)/W; H=int(np.ceil((Y1-Y0)/S)); TOP=64-H; LEFT=1
CH='.123456789abcdef'
PAL=[(255,0,255),
 (32,12,18),    #1 omlijning / opening
 (84,22,36),    #2 binnenlijn + selout donkerrood
 (116,34,50),   #3 rood schaduw
 (156,48,66),   #4 rood mid
 (190,76,88),   #5 rood licht
 (220,120,122), #6 hooglicht
 (136,64,78),   #7 mauve donker (mondkanon/lip)
 (200,130,134), #8 mauve licht
 (164,112,36),  #9 geel donker
 (228,188,84),  #a geel
 (252,236,160), #b geel licht
 (255,255,255),(255,255,255),(255,255,255),(255,255,255)]
def model():
    return np.asarray(Image.open(MODEL).convert('RGB')).astype(int)
def cell(x,y):
    bx=X0+(x-LEFT)*S; by=Y0+(y-TOP)*S
    return slice(int(round(by)),int(round(by+S))),slice(int(round(bx)),int(round(bx+S)))
def fgmask(c):
    lum=c.mean(2); sat=c.max(2)-c.min(2); return (lum<235)|(sat>20)
def read(p):
    R=[l.rstrip('\n') for l in open(p)]
    return np.array([[CH.index(ch) for ch in r.ljust(64,'.')[:64]] for r in R[:64]])
def write(a,p):
    open(p,'w').write('\n'.join(''.join(CH[v] for v in r) for r in a)+'\n')
def topng(a,p,pal=None):
    pal=pal or PAL
    im=Image.fromarray(a.astype('uint8'),'P'); fl=[v for c in pal for v in c]; im.putpalette(fl+[0]*(768-len(fl)))
    im.save(p,transparency=0)
def rgba(a,bg=None,pal=None):
    pal=pal or PAL
    o=np.zeros((64,64,4),'uint8')
    for i,c in enumerate(pal):
        o[a==i,:3]=c; o[a==i,3]=255
    o[a==0,3]=0
    im=Image.fromarray(o)
    if bg: b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im); return b.convert('RGB')
    return im
def model64(method=Image.BOX):
    src=Image.open(MODEL).convert('RGB')
    n=int(round(64*S))
    big=Image.new('RGB',(n,n),(255,255,255))
    ox=int(round(X0-LEFT*S)); oy=int(round(Y0-TOP*S))
    big.paste(src,(-ox,-oy))
    return big.resize((64,64),method)
