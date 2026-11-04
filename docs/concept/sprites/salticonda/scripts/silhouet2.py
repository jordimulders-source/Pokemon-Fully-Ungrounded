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

def cone(yt, yb, wt, wb, bands, cx, conv=0.7, bulge=1.6, tuck=3.0, top_round=0.55,
         bot_h=6, bot_lift=4.0, lean=0.0):
    """yt..yb: kegel; wt/wb: halve breedte boven/onder (kegellijn);
    bands: (begin, eind) per winding van boven naar onder; cx: midden per winding;
    bulge: hoeveel een winding midden aan de rand uitbolt; tuck: inkeping onderaan
    een winding (waar hij op de volgende ligt)."""
    pts=set(); n=len(bands)
    for y in range(yt, yb+1):
        s=(y-yt)/(yb-yt)
        W=wt+(wb-wt)*(s**conv)
        for i,(a,b) in enumerate(bands):
            if a<=y<=b: break
        hb=(b-a+1)/2; mid=a+hb-0.5
        t=(y-mid)/hb                      # -1 boven .. +1 onder in de winding
        # bol profiel: midden + bulge, boven zacht afgerond, onder sterker ingestopt
        if t<0: d=-bulge*(1-t*t) + (tuck*0.45)*(1-math.sqrt(max(0,1-t*t)))
        else:   d=-bulge*(1-t*t) + tuck*(1-math.sqrt(max(0,1-t*t)))
        if i==0 and t<0 and top_round:    # bovenste winding: koepel onder de kop
            d+=W*top_round*(abs(t)**2.2)
        w=W-d
        c=cx[i]+lean*s
        if y>yb-bot_h:                    # onderkant: ronde boog naar de grond
            u=(y-(yb-bot_h))/bot_h
            w=w-bot_lift*W/28*(1-math.sqrt(max(0,1-u*u)))*3.2
        for x in range(int(c-w-1), int(c+w+2)):
            if abs(x+0.5-c)<=w: pts.add((x,y))
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
 'D': dict(cone=dict(yt=20,yb=60,wt=14,wb=29.5,bands=[(20,28),(29,38),(39,49),(50,60)],
                     cx=[32,31,32,30.5],conv=0.75),
           head=(10,7)),
 # 3 dikke windingen, lagere en bredere kegel
 'E': dict(cone=dict(yt=23,yb=60,wt=16,wb=30,bands=[(23,33),(34,46),(47,60)],
                     cx=[32.5,31,30.5],conv=0.65,bulge=2.0,tuck=3.4),
           head=(10,10)),
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
