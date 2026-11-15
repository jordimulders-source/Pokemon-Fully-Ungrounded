# Vormgereedschap: gevulde schijf (creme ring + lila vulling) met één uitgekerfde spiraalgroef van 1 px (pixel-perfect).
import math
def lijn(punten):
    """Dichte bemonstering -> unieke pixels in volgorde -> L-hoeken weg (pixel-perfect 1 px lijn)."""
    px=[]
    for (x,y) in punten:
        p=(int(math.floor(x)),int(math.floor(y)))
        if not px or px[-1]!=p: px.append(p)
    out=[]
    i=0
    while i<len(px):
        if 0<len(out) and i+1<len(px):
            a=out[-1]; c=px[i+1]
            if abs(a[0]-c[0])==1 and abs(a[1]-c[1])==1: i+=1; continue
        out.append(px[i]); i+=1
    return out
def spiraalgroef(cx,cy,sx,sy,P,t0,t1,rot=0.0,draai=1):
    pts=[]; n=int((t1-t0)*400)
    for k in range(n+1):
        t=t0+(t1-t0)*k/n; r=P*t; a=draai*2*math.pi*(t+rot)
        pts.append((cx+sx*r*math.cos(a),cy+sy*r*math.sin(a)))
    return lijn(pts)
def schijf(cx,cy,sx,sy,R,ring=2.0,rin='C',vul='L',groef=None,open_=None):
    out={}
    for y in range(int(cy-R*sy)-2,int(cy+R*sy)+3):
        for x in range(int(cx-R*sx)-2,int(cx+R*sx)+3):
            dx=(x+.5-cx)/sx; dy=(y+.5-cy)/sy; r=math.hypot(dx,dy)
            if r>R: continue
            out[(x,y)]= rin if r>R-ring else vul
    for p in (groef or []):
        if p in out: out[p]='g'
    return out
def toon(mat,x0,x1,y0,y1):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(mat.get((x,y),'.') for x in range(x0,x1)))
def alsraster(mat,x0,x1,y0,y1):
    return '\n'.join(''.join(mat.get((x,y),'.') for x in range(x0,x1)) for y in range(y0,y1))
def tweearm(cx,cy,sx,sy,R,P,a='C',b='L',rot=0.0,draai=1,split=0.5,kern=None):
    """Twee in elkaar gedraaide gevulde armen (a en b) zonder groef: spiraal als ingekleurd vlak."""
    out={}
    for y in range(int(cy-R*sy)-2,int(cy+R*sy)+3):
        for x in range(int(cx-R*sx)-2,int(cx+R*sx)+3):
            dx=(x+.5-cx)/sx; dy=(y+.5-cy)/sy; r=math.hypot(dx,dy)
            if r>R: continue
            t=(draai*math.atan2(dy,dx)/(2*math.pi)+rot)%1.0
            u=r/P-t; f=u-math.floor(u)
            out[(x,y)]= a if f<split else b
            if kern and r<kern: out[(x,y)]='g'
    return out
def ringspiraal(cx,cy,sx,sy,R,ring,P,rin='C',arm='L',tus='g',rot=0.0,draai=1,split=0.55,open_=None):
    """Model-opbouw: buitenring (rin) + binnen een gevulde spiraalarm (arm) met een tussenarm (tus, uitgekerfd bruin).
    open_=(t0,t1): hoekbereik (in omwentelingen, 0 = rechts, met de klok mee) waar de ring open is en de arm doorloopt."""
    out={}
    for y in range(int(cy-R*sy)-2,int(cy+R*sy)+3):
        for x in range(int(cx-R*sx)-2,int(cx+R*sx)+3):
            dx=(x+.5-cx)/sx; dy=(y+.5-cy)/sy; r=math.hypot(dx,dy)
            if r>R: continue
            hoek=(math.atan2(dy,dx)/(2*math.pi))%1.0
            inopen= open_ and (open_[0]<=hoek<=open_[1] if open_[0]<open_[1] else (hoek>=open_[0] or hoek<=open_[1]))
            if r>R-ring and not inopen: out[(x,y)]=rin; continue
            t=(draai*math.atan2(dy,dx)/(2*math.pi)+rot)%1.0
            u=r/P-t; f=u-math.floor(u)
            out[(x,y)]= arm if f<split else tus
    return out
