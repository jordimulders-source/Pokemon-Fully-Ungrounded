# Verkleint een RGBA-laag in r7-origineelcoordinaten (1024x1024-raam, mag groter met offset) naar spritepixels,
# met dezelfde regels als r1: achtergrond >= BG, donkere punt >= TP, lijn >= LMIN, anders grootste vlakgroep + tint uit
# de gemiddelde helderheid. Klassen per origineelpixel op kleur (zoals klassen.py), achtergrond = alpha 0.
import numpy as np
from gemeen import NX0,NY0,S,OX,OY
def klas(rgb,alpha):
    a=rgb.astype(int); r,g,b=a[...,0],a[...,1],a[...,2]; L=(r*299+g*587+b*114)/1000
    mx=a.max(-1); mn=a.min(-1); d=(mx-mn).astype(float)
    rf,gf,bf=r/255,g/255,b/255; dd=np.maximum(d/255,1e-6)
    hue=np.where(mx==r,((gf-bf)/dd)%6,np.where(mx==g,(bf-rf)/dd+2,(rf-gf)/dd+4))*60
    sat=d/np.maximum(mx,1); col=sat>0.30
    c=np.full(L.shape,5)
    c[col&((hue<14)|(hue>320))]=3; c[col&(hue>=14)&(hue<32)]=6; c[col&(hue>=32)&(hue<75)]=4
    c[(~col)&(L<110)]=2; c[L<40]=1
    c[alpha<128]=0
    return c,L
def o2s(ox,oy): return OX+((ox-0.1)/6.4-NX0)*S, OY+((oy-0.1)/6.4-NY0)*S
def s2o(X,Y): return 0.1+6.4*(NX0+(X-OX)/S), 0.1+6.4*(NY0+(Y-OY)/S)
def tint(g,l):
    if g==3: return 8 if l<66 else 9 if l<100 else 10
    if g==4: return 2 if l<118 else 3 if l<156 else 4 if l<188 else 5
    if g==5: return 6 if l<214 else 7
    if g==2: return 13
    return 4
def reduceer(c,L,BG=0.5,TP=0.35,LMIN=0.25,goud6=True,box=(0,0,64,64),DG=None):
    """c,L: klassen per origineelpixel (zelfde raam als r7). Geeft spritematrix (0 = leeg) en lijnaandeel."""
    o=np.zeros((64,64),int); fr=np.zeros((64,64,7))
    H,W=c.shape
    for Y in range(box[1],box[3]):
        for X in range(box[0],box[2]):
            x0,y0=s2o(X,Y); x1,y1=s2o(X+1,Y+1)
            xa,xb=int(round(x0)),int(round(x1)); ya,yb=int(round(y0)),int(round(y1))
            if xb<=0 or yb<=0 or xa>=W or ya>=H: continue
            cc=c[max(0,ya):yb,max(0,xa):xb]; ll=L[max(0,ya):yb,max(0,xa):xb]
            n=(yb-ya)*(xb-xa)
            f=np.array([(cc==k).sum() for k in range(7)],float); f[0]+=n-cc.size; f/=n
            if goud6: f[4]+=f[6]; f[6]=0
            fr[Y,X]=f
            if f[2]>=TP: o[Y,X]=13; continue
            if f[0]>=BG: continue
            if f[1]>=LMIN: o[Y,X]=1; continue
            if DG is not None and ((cc==4)&(ll<118)).sum()/n>=DG: o[Y,X]=2; continue   # donkere goudlijn (veerscheiding) wint vanaf DG
            if f[2:].sum()==0: o[Y,X]=1; continue
            g=2+int(np.argmax(f[2:]))
            o[Y,X]=tint(g,ll[cc==g].mean())
            if g==3:
                lv=ll[cc==3]; fl=(lv>=100).sum()/n; fd=(lv<66).sum()/n
                if fl>=0.38: o[Y,X]=10
                elif fd>=0.45: o[Y,X]=8
    return o,fr
