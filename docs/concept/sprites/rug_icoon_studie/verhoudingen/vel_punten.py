"""Controlevel: per soort front (4x) en icoon (8x, zodat 1 icoonpixel = 2 frontpixels: dezelfde schaal na halvering) met de punten.
Kader = kop (zonder oren), kruis = oog, rode streep = oortop, blauw = romp + buiklijn, groen = onderkant voor-/achterpoot, oranje kader = staart.
python3 vel_punten.py uit.png [soort ...]"""
import sys,numpy as np
from PIL import Image,ImageDraw
from punten import P
from laad import front,icoon
def teken(a,d,Z):
    bg=Image.new('RGB',(a.shape[1]*Z,a.shape[0]*Z),(150,210,180)); im=Image.fromarray(a).resize(bg.size,Image.NEAREST); bg.paste(im,(0,0),im)
    g=ImageDraw.Draw(bg); X=lambda v:(v+.5)*Z
    k=d['kop']; g.rectangle([k[0]*Z,k[1]*Z,(k[2]+1)*Z-1,(k[3]+1)*Z-1],outline=(255,0,255),width=2)
    o=d['oog']; ox,oy=X(o[0]),X(o[1]); g.line([ox-2*Z,oy,ox+2*Z,oy],fill=(255,0,0),width=2); g.line([ox,oy-2*Z,ox,oy+2*Z],fill=(255,0,0),width=2)
    if d['oor'] is not None: g.line([k[0]*Z,d['oor']*Z,(k[2]+1)*Z,d['oor']*Z],fill=(255,60,60),width=1)
    if d['romp']: g.line([d['romp'][0]*Z,(d['buik']+1)*Z if d['buik'] else 0,(d['romp'][1]+1)*Z,(d['buik']+1)*Z if d['buik'] else 0],fill=(0,0,255),width=2)
    for key,c in (('vp',(0,160,0)),('ap',(0,90,0))):
        if d[key] is not None: g.line([0,(d[key]+1)*Z,bg.width,(d[key]+1)*Z],fill=c,width=1)
    s=d['staart']
    if s: g.rectangle([s[0]*Z,s[1]*Z,(s[2]+1)*Z-1,(s[3]+1)*Z-1],outline=(255,140,0),width=2)
    return bg
sps=sys.argv[2:] or list(P)
C=3; cw=256+256+30; ch=256+22
img=Image.new('RGB',(C*cw,((len(sps)+C-1)//C)*ch),(255,255,255)); d=ImageDraw.Draw(img)
for n,sp in enumerate(sps):
    x,y=(n%C)*cw,(n//C)*ch; d.text((x+4,y+3),sp+(' (posewissel)' if P[sp].get('posewissel') else '')+(' (frontaal)' if P[sp].get('frontaal') else ''),fill=0)
    img.paste(teken(front(sp),P[sp]['f'],4),(x+4,y+18)); img.paste(teken(icoon(sp),P[sp]['i'],8),(x+4+256+10,y+18))
img.save(sys.argv[1])
