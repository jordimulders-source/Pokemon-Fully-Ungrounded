"""Salticonda silhouet ronde 1: opgerolde zoutkegel op Ekans als skelet.
Windingen = superellipsen (rijen met eigen linker-/rechterrand), kop+kraag uit de
goedgekeurde Uyuni-Silicobra (rijen 13-37), staart als spits (Sandaconda-idee).
Daarna handmatige pixel-correcties per variant (lijst FIX)."""
from PIL import Image, ImageDraw
import math, os
R='/home/user/Pokemon-Fully-Ungrounded/'
OUT=R+'docs/concept/sprites/salticonda/silhouet1/'
SIL=[l.rstrip('\n') for l in open(R+'docs/concept/sprites/silicobra_uyuni/af/silicobra_uyuni_raster.txt')]

def head_mask(y0, y1):
    pts=set()
    for y in range(y0, y1+1):
        for x,c in enumerate(SIL[y]):
            if c!='.' and x<46: pts.add((x,y))
    return pts

def coil(cx, cy, hw, hh, e=2.6):
    pts=set()
    for y in range(int(cy-hh)-1, int(cy+hh)+2):
        t=(y+0.5-cy)/hh
        if abs(t)>=1: continue
        w=hw*(1-abs(t)**e)**(1/e)
        for x in range(int(cx-w-1), int(cx+w+2)):
            if abs(x+0.5-cx)<=w: pts.add((x,y))
    return pts

def spike(pts_line, widths):
    """staart: lijst middenpunten met halve dikte."""
    s=set()
    for (x,y),w in zip(pts_line,widths):
        for dx in range(-int(w)-1,int(w)+2):
            for dy in range(-int(w)-1,int(w)+2):
                if dx*dx+dy*dy<=w*w+0.3: s.add((int(round(x+dx)),int(round(y+dy))))
    return s

def line(p0,p1,w0,w1,n=24):
    pl=[];wl=[]
    for i in range(n+1):
        t=i/n; pl.append((p0[0]+(p1[0]-p0[0])*t, p0[1]+(p1[1]-p0[1])*t)); wl.append(w0+(w1-w0)*t)
    return pl,wl

def head(hx,hy):
    """Eigen kop: schedel + zoutkuif (Silicobra-Uyuni) + langere, platte snuit
    met neusgatbult (Sandaconda-idee). Kijkt naar links-voor."""
    p=set()
    p|=coil(hx+17,hy+10,9.5,8,2.2)        # schedel
    p|=coil(hx+16,hy+3.5,6.5,3.6,2.0)     # zoutkuif (koepel)
    p|=coil(hx+7.5,hy+11,8,4.6,3.2)       # snuit: plat boven, rond aan de punt
    p|=coil(hx+3,hy+6.6,2.2,1.3,2)        # neusgatbult bovenop de snuitpunt
    return p

def build(spec):
    pts=set()
    for c in spec['coils']: pts|=coil(*c)
    pts|=head(*spec['head'])
    for seg in spec['tail']:
        pl,wl=line(*seg); pts|=spike(pl,wl)
    for (x,y) in spec.get('notch',[]): pts.discard((x,y))
    for (x,y) in spec.get('add',[]): pts.add((x,y))
    return {(x,y) for (x,y) in pts if 0<=x<64 and 0<=y<64}

# coils: (cx, cy, halve breedte, halve hoogte)
V={
 'A': dict(  # 4 windingen, kop recht bovenop de kegel, staartspits rechtsonder
   coils=[(32,52,27,6.5,2.3),(33.5,43,22.5,5.2,2.3),(31.5,35.5,18,4.8,2.3),(33.5,28.5,13.5,4.3,2.3)],
   head=(14,8), tail=[((50,54),(62,49),3.2,0.6)]),
 'B': dict(  # 3 windingen, lager en breder, kop hangt naar links-voor over de rand
   coils=[(34,51.5,27.5,7,2.3),(35,41,23,5.8,2.3),(36,32,17.5,5,2.3)],
   head=(8,13), tail=[((52,53),(63,49),3.4,0.6)]),
 'C': dict(  # 4 windingen, staart als spits langs rechts omhoog (Ekans-houding, Sandaconda-spits)
   coils=[(31,52.5,26,6.5,2.3),(32.5,43.5,22,5.2,2.3),(31,36,18,4.8,2.3),(32.5,29,13.5,4.3,2.3)],
   head=(13,8.5), tail=[((49,50),(56,40),3.4,1.8),((56,40),(58,30),1.8,0.4)]),
}

def save(pts,name):
    im=Image.new('P',(64,64),0)
    im.putpalette([0,0,0, 48,40,48]+[0]*762)
    for p in pts: im.putpixel(p,1)
    im.save(OUT+name+'.png',transparency=0)
    return im

def raster(pts):
    return '\n'.join(''.join('#' if (x,y) in pts else '.' for x in range(64)) for y in range(64))

if __name__=='__main__':
    for k,s in V.items():
        p=build(s); save(p,'variant_'+k)
        open(OUT+'variant_%s_raster.txt'%k,'w').write(raster(p)+'\n')
        print(k,len(p))
