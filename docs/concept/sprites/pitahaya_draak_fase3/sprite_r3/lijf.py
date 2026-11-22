# Lijfvulling r3: volume-toonkaart (volume.py) per spritepixel, gekwantiseerd naar G (schaduw) / h (midden) / H (licht),
# daarna clusters < 3 px opgeruimd (naar de meerderheid van de buren). Lijnen (#, g) en roze blijven zoals in r2.
import sys,numpy as np; sys.path.append('../sprite_r2'); from volume import kaart
geo=np.load('../sprite_r2/kaal_info.npz')['geo']; S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
def venster(Y,X):
    j=Y-Y0+ymin; i=X-X0+xmin; y0=by0-S+OY+S*j; x0=bx0-S+OX+S*i
    return slice(max(int(round(y0)),0),int(round(y0+S))),slice(max(int(round(x0)),0),int(round(x0+S)))
def per_pixel(R=10.0,A=0.5,L=(-0.55,-0.65,0.52)):
    m,v=kaart(R,A,L); out=np.full((64,64),np.nan)
    for Y in range(64):
        for X in range(64):
            sl=venster(Y,X); mm=m[sl]
            if mm.sum()>=0.25*mm.size: out[Y,X]=v[sl][mm].mean()
    return out
def vul(o,V,zone,pct=(35,82),tonen=(7,8,9)):
    """zone: bool 64x64 (welke vulpixels opnieuw); pct: percentielen schaduw/licht binnen de zone"""
    pos=[(y,x) for y,x in zip(*np.where(zone)) if not np.isnan(V[y,x])]
    vals=np.array([V[y,x] for y,x in pos]); q=np.percentile(vals,pct)
    for (y,x),v in zip(pos,vals): o[y,x]=tonen[0] if v<q[0] else (tonen[1] if v<q[1] else tonen[2])
    return o
def clusters(o,zone,minpx=3,tonen=(7,8,9)):
    for _ in range(3):
        seen=np.zeros((64,64),bool)
        for y0,x0 in zip(*np.where(zone)):
            if seen[y0,x0]: continue
            k=o[y0,x0]; st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
            while st:
                y,x=st.pop(); cl.append((y,x))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    a,b=y+dy,x+dx
                    if 0<=a<64 and 0<=b<64 and zone[a,b] and not seen[a,b] and o[a,b]==k: seen[a,b]=1; st.append((a,b))
            if len(cl)<minpx:
                for y,x in cl:
                    nb=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64 and zone[y+dy,x+dx] and o[y+dy,x+dx]!=k]
                    if nb: o[y,x]=max(set(nb),key=nb.count)
    return o
