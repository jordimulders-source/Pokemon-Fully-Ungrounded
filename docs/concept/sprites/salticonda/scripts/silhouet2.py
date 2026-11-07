"""Salticonda silhouet ronde 2: bulkiere zoutkegel vanaf variant A (ronde 1).
Kop van A bevroren (HEAD uit silhouet1.py, alleen verschoven).
Kegel = één gladde, licht bolle omhullende; elke winding bolt aan de rand iets uit
en zakt aan de onderkant in (ligt óp de winding eronder) -> kleine inkeping.
De onderkant is een ronde boog (geen lange platte grondlijn), de staart komt
rechtsonder onder de onderste winding vandaan."""
import math, sys
sys.path.insert(0, '/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
from silhouet1 import head, save, raster
OUT='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/silhouet2/'

def edge_d(y, bands, W, tuck, rise, bulge, top_round):
    """Inspringing van de rand op rij y voor één kant van de kegel."""
    n=len(bands)
    i=n-1
    for j,(a,b) in enumerate(bands):
        if a<=y<=b: i=j; break
    a,b=bands[i]
    h=b-a+1; t=(y-a+0.5)/h
    d=-bulge*math.sin(math.pi*t)           # winding bolt aan de rand uit
    if i>0 and t<0.5:                      # bovenkant: komt onder de winding erboven vandaan
        d+=tuck*0.75*(1-t/0.5)**1.6
    if i<n-1 and t>0.5:                    # onderkant: rond afgerond, ligt op de volgende
        u=(t-0.5)/0.5
        d+=tuck*(1-math.sqrt(max(0,1-u*u)))
    if i==0 and top_round:                 # bovenste winding: koepel onder de kop
        t=1-(y-a)/(b-a+1)
        d+=W*top_round*(max(0,t)**2.2)
    return d

def cone(yt, yb, wt, wb, bands, cx, p=1.6, tuck=3.0, rise=3, top_round=0.55, bulge=1.2,
         bot_h=7, bot_in=0.55, lean=0.0, spiral=3):
    """Gladde kegel/heuvel: halve breedte W(y) volgt een superellips (p=1 rechte
    kegel, p=2 koepel). Windingen als spiraal: de gleuven liggen rechts 'spiral'
    rijen hoger dan links, zodat het een opgerolde slang is en geen traptreden."""
    pts=set(); H=yb-yt
    bandsR=[(max(yt,a-spiral) if i>0 else a, b-spiral if i<len(bands)-1 else b) for i,(a,b) in enumerate(bands)]
    for y in range(yt, yb+1):
        s=(y-yt)/H
        W=wt+(wb-wt)*(1-(1-s)**p)**(1/p)
        # midden glijdend tussen de windingmiddens (geen sprong op de gleuf)
        mids=[(a+b)/2 for a,b in bands]
        if y<=mids[0]: c=cx[0]
        elif y>=mids[-1]: c=cx[-1]
        else:
            for j in range(len(mids)-1):
                if mids[j]<=y<=mids[j+1]:
                    f=(y-mids[j])/(mids[j+1]-mids[j]); c=cx[j]+(cx[j+1]-cx[j])*f
        c+=lean*s
        wl=W-edge_d(y,bands,W,tuck,rise,bulge,top_round)
        wr=W-edge_d(y,bandsR,W,tuck,rise,bulge,top_round)
        if y>yb-bot_h:                     # onderkant: ronde boog naar de grond
            u=(y-(yb-bot_h))/bot_h
            k=W*bot_in*(1-math.sqrt(max(0,1-u*u))); wl-=k; wr-=k
        for x in range(int(c-wl-1), int(c+wr+2)):
            if c-wl<=x+0.5<=c+wr: pts.add((x,y))
    return pts

def build(spec):
    pts=cone(**spec['cone'])
    pts|=head(*spec['head'])
    for y,edge,segs in spec.get('rows',[]):
        for x in range(edge+1,64): pts.discard((x,y))
        for a,b in segs:
            for x in range(a,b+1): pts.add((x,y))
    for p in spec.get('notch',[]): pts.discard(p)
    for p in spec.get('add',[]): pts.add(p)
    return {(x,y) for (x,y) in pts if 0<=x<64 and 0<=y<64}

V={
 # 4 windingen, steilere kegel (kop hoger, flanken schuiner)
 'D': dict(cone=dict(yt=19,yb=60,wt=14.5,wb=28.5,bot_h=11,bot_in=0.75,bands=[(19,28),(29,38),(39,49),(50,60)],
                     cx=[30.5,29,30.5,28.5],p=1.45,bulge=1.4,tuck=3.6),
           head=(9,6),
           # staartspits rechtsonder: komt onder de onderste winding vandaan, gleuf erboven (Sandaconda-idee)
           rows=[(47,64,[(61,62)]),(48,64,[(60,62)]),(49,64,[(59,62)]),(50,64,[(58,61)]),(51,64,[(58,60)]),
                 (52,64,[(57,60)]),(53,64,[(56,59)]),(54,64,[(55,58)]),(55,64,[(54,57)]),(56,64,[(52,55)]),(57,64,[(50,51)])],
           notch=[(48,24)]),
 # 3 dikke windingen op dezelfde kegel als D (zelfde omhullende, minder en dikkere ringen)
 'E': dict(cone=dict(yt=19,yb=60,wt=14.5,wb=28,bot_h=11,bot_in=0.75,bands=[(19,32),(33,46),(47,60)],
                     cx=[30.5,29.5,28.5],p=1.45,bulge=1.8,tuck=4.0,spiral=4),
           head=(9,6),
           rows=[(47,64,[(61,62)]),(48,64,[(60,62)]),(49,64,[(59,62)]),(50,64,[(58,61)]),(51,64,[(58,60)]),
                 (52,64,[(57,60)]),(53,64,[(56,59)]),(54,64,[(55,58)]),(55,64,[(54,57)]),(56,64,[(52,55)]),(57,64,[(50,51)])]),
}

def staart(spec, edge_shift=0):
    pass

if __name__=='__main__':
    for k,s in V.items():
        p=build(s); save_to=OUT+'variant_'+k
        from PIL import Image
        im=Image.new('P',(64,64),0); im.putpalette([0,0,0,48,40,48]+[0]*762)
        for q in p: im.putpixel(q,1)
        im.save(save_to+'.png',transparency=0)
        open(save_to+'_raster.txt','w').write(raster(p)+'\n')
        xs=[q[0] for q in p]; ys=[q[1] for q in p]
        print(k,len(p),'breed',max(xs)-min(xs)+1,'hoog',max(ys)-min(ys)+1)
