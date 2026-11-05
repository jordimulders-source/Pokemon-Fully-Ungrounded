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

# Kop met de hand (anaconda-foto's: lange platte kop, brede ronde stompe snuit,
# oog en neusgat hoog bovenop; Sandaconda: langere snuit met neusbult aan de punt;
# Silicobra-Uyuni: zoutkuif achter het oog). Kijkt naar links-voor.
HEAD = """
..............######.......
...........###########.....
.........##############....
........################...
.......##################..
..###.####################.
.##########################
###########################
###########################
##########################.
#########################..
.########################..
..######################...
....####################...
.......##################..
"""
def head(hx,hy):
    p=set()
    for y,row in enumerate(HEAD.strip('\n').split('\n')):
        for x,c in enumerate(row):
            if c=='#': p.add((x+hx,y+hy))
    return p

def cone(yt, yb, wt, wb, bands, cx_list, notch=3.4, conv=0.75, base_round=4, top_round=0):
    """Afgeronde zoutkegel: gladde omhullende (bol, zwaar) met per winding een
    afgeronde rand en een kleine gleuf tussen de windingen."""
    pts=set(); n=len(bands)
    for y in range(yt, yb+1):
        s=(y-yt)/(yb-yt)
        W=wt+(wb-wt)*(s**conv)
        # in welke winding zitten we
        for i,(a,b) in enumerate(bands):
            if a<=y<=b: break
        mid=(a+b)/2; hb=(b-a)/2+0.5
        t=min(1,abs(y+0.5-mid-0.5)/hb)
        d=notch*(1-math.sqrt(max(0,1-t*t)))
        if i==n-1 and y>mid:  # onderste winding: rond tegen de grond
            d=base_round*(1-math.sqrt(max(0,1-t*t)))*1.0+ (W*0.5*(t**3))
        if i==0 and y<mid and top_round:  # bovenste winding: koepel, geen platte bovenkant
            d=notch*(1-math.sqrt(max(0,1-t*t)))+W*top_round*(t**2.5)
        cx=cx_list[i]
        w=W-d
        for x in range(int(cx-w-1), int(cx+w+2)):
            if abs(x+0.5-cx)<=w: pts.add((x,y))
    return pts

def build(spec):
    pts=set()
    if 'cone' in spec: pts|=cone(**spec['cone'])
    for c in spec.get('coils',[]): pts|=coil(*c)
    pts|=head(*spec['head'])
    for seg in spec['tail']:
        pl,wl=line(*seg); pts|=spike(pl,wl)
    for (x,y) in spec.get('notch',[]): pts.discard((x,y))
    if 'rows' in spec:  # handgetekende rechterkant per rij: (y, rand van winding, [staartstukken])
        for y,edge,segs in spec['rows']:
            for x in range(edge+1,64): pts.discard((x,y))
            for a,b in segs:
                for x in range(a,b+1): pts.add((x,y))
    for (x,y) in spec.get('add',[]): pts.add((x,y))
    return {(x,y) for (x,y) in pts if 0<=x<64 and 0<=y<=58}

# coils: (cx, cy, halve breedte, halve hoogte)
V={
 'A': dict(  # 4 windingen, kop recht bovenop de kegel (kuif = top), staartspits rechtsonder
   cone=dict(yt=26,yb=58,wt=13,wb=29,bands=[(26,33),(34,41),(42,49),(50,58)],cx_list=[32.5,30.5,31.5,29.5],notch=4),
   head=(9,11), tail=[],
   # staart komt onder de onderste winding vandaan en loopt als spits naar rechtsboven (Sandaconda-idee)
   rows=[(49,55,[]),(50,54,[(61,62)]),(51,54,[(58,62)]),(52,54,[(56,61)]),(53,54,[(55,60)]),(54,53,[(54,59)]),
         (55,53,[(54,57)]),(56,52,[(53,55)]),(57,50,[]),(58,47,[])]),
 'B': dict(  # 3 dikke windingen; kop ligt plat vooraan op de middelste winding en hangt links-voor over de rand (opgerolde anaconda-foto); de kegeltop is de bovenste winding
   cone=dict(yt=21,yb=58,wt=11,wb=30,bands=[(21,32),(33,45),(46,58)],cx_list=[40,36,32],notch=5,conv=0.6,top_round=0.6),
   head=(1,22), tail=[],
   rows=[(48,56,[]),(49,56,[]),(50,55,[(61,62)]),(51,55,[(58,62)]),(52,55,[(57,61)]),(53,55,[(56,60)]),(54,54,[(55,59)]),
         (55,54,[(55,58)]),(56,53,[(54,56)]),(57,51,[]),(58,48,[])]),
 'C': dict(  # 4 windingen, staart als spits langs rechts omhoog (Ekans-houding, Sandaconda-spits)
   cone=dict(yt=25,yb=58,wt=13,wb=29,bands=[(25,32),(33,40),(41,49),(50,58)],cx_list=[33.5,31.5,33,31.5],notch=4),
   head=(10,11), tail=[((50,51),(56,41),3.4,1.8),((56,41),(58,31),1.8,0.4)],
   notch=[(58,42)]),
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
