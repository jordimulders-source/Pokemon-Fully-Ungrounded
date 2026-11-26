# Varianten r1: basis (basis.py) + spiraal (a = Poliwhirl-vorm in modelrood, b = Poliwhirl letterlijk) + ogen (1 = Gen 3-Poliwhirl, 2 = regionale Poliwag).
# Alleen pixels 1-op-1 uit de bronsprites; kleuren omgezet naar het palet. Verder niets.
import sys, numpy as np; from PIL import Image
exec(open('basis.py').read())
ROOT='../../../../../'
pw=np.array(Image.open(ROOT+'graphics/pokemon/poliwhirl/anim_front_gba.png'))[:64]
pr=np.array(Image.open('../../poliwag_regional/af/poliwag_regional.png'))
BASIS=out.copy()
SPCX,SPCY=22.5,23.5        # midden modelspiraal (rode cellen, reductie)
PWCX,PWCY=31,32           # midden Poliwhirl-spiraal (gba); straal 5 valt in een witte tussenruimte (bandmeting)
RAD=float(sys.argv[1]) if len(sys.argv)>1 else 5.0
DX,DY=int(round(SPCX-PWCX)),int(round(SPCY-PWCY))
# buik = gele/rode cellen rond de modelspiraal (verbonden gebied)
bm=((cls==1)|(cls==2)); lb,_=comps(bm); buik=(lb==lb[24,22])&(jj>=17)&(ii>=15)&(ii<=31)
# venster: cirkel rond het spiraalmidden
venster=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        sx,sy2=x-DX,y-DY
        if 0<=sx<64 and 0<=sy2<64 and (sx-PWCX)**2+(sy2-PWCY)**2<=RAD**2 and pw[sy2,sx] in (1,2,3,4,8,9,15): venster[y,x]=True
venster&=buik
OOGMAP={1:8,2:9,3:10,4:10,8:4,9:3,15:1}   # Poliwhirl gba -> palet: wit->ijswit, lichtgrijs->ijs licht/midden, grijs->lijf 4/3, zwart->1
def geel_onder(o):
    # modelrood in de buik terug naar geel (tint uit de gele omgeving, zoals de rest van de buik)
    sy=blur(lum,Y&buik,1.2); r=buik&(cls==2)
    o[r]=np.select([sy[r]>=203,sy[r]>=172],[5,6],7)
def spiraal(o,v):
    geel_onder(o)
    for y,x in zip(*np.where(venster)):
        p=pw[y-DY,x-DX]
        if v=='a':
            if p in (8,9,15): o[y,x]={8:12,9:13,15:14}[p]
        else:
            o[y,x]=OOGMAP[p]
def oog_pw(o,c0,c1,r0,r1,cx,cy):
    sub=pw[r0:r1+1,c0:c1+1]; m0=np.isin(sub,[1,2,3,8,9,15])
    # alleen het samenhangende oog (geen buikpixels uit het kader)
    m=np.zeros_like(m0); st=[(sub.shape[0]//2,sub.shape[1]//2)]
    while st:
        j,i=st.pop()
        if j<0 or i<0 or j>=m.shape[0] or i>=m.shape[1] or m[j,i] or not m0[j,i]: continue
        m[j,i]=True; st+=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
    yy,xx=np.where(m); dx=int(round(cx-(xx.min()+xx.max())/2)); dy=int(round(cy-(yy.min()+yy.max())/2))
    ring=np.zeros_like(m)
    for j,i in zip(yy,xx):
        for a,b in ((1,0),(-1,0),(0,1),(0,-1)):
            if 0<=j+a<m.shape[0] and 0<=i+b<m.shape[1] and not m[j+a,i+b]: ring[j+a,i+b]=True
    for j,i in zip(*np.where(ring)): o[j+dy,i+dx]=1
    for j,i in zip(yy,xx): o[j+dy,i+dx]=OOGMAP[sub[j,i]]
    return (xx.min()+dx,xx.max()+dx,yy.min()+dy,yy.max()+dy)
def oog_pr(o,rows,cx,cy):
    # regionale Poliwag r1 (= af): de oogregels letterlijk, incl. ooglid 6/7 en lijf 2
    pts=[(x0+dx,y,int(ch,16)) for y,(x0,r) in rows.items() for dx,ch in enumerate(r)]
    ey=[p for p in pts if p[2] not in (2,6,7)]
    xs_=[p[0] for p in ey]; ys_=[p[1] for p in ey]
    dx=int(round(cx-(min(xs_)+max(xs_))/2)); dy=int(round(cy-(min(ys_)+max(ys_))/2))
    for x,y,v in pts: o[y+dy,x+dx]=v
    return (min(xs_)+dx,max(xs_)+dx,min(ys_)+dy,max(ys_)+dy)
OOG_VER={7:(5,"77"), 8:(5,"111"), 9:(4,"1911"), 10:(3,"19181"), 11:(3,"18311"), 12:(3,"19116"), 13:(2,"77887"), 14:(3,"671")}
OOG_NABIJ={7:(16,"72"), 8:(14,"611992"), 9:(14,"1911992"), 10:(13,"61881991"), 11:(14,"1111981"), 12:(14,"1333981"), 13:(14,"1118816"), 14:(14,"771116")}
OOGL=(16,4.5); OOGR=(29,4.5)   # middens modelogen (reductiecellen, gemeten op de zwarte oogring)
def ogen(o,v):
    if v=='1':
        oog_pw(o,19,27,12,20,*OOGL); oog_pw(o,36,46,12,20,*OOGR)
    else:
        oog_pr(o,OOG_VER,*OOGL); oog_pr(o,OOG_NABIJ,*OOGR)
def maak(sv,ov):
    o=BASIS.copy(); spiraal(o,sv); ogen(o,ov); return o
if __name__=='__main__':
    for sv in 'ab':
        for ov in '12':
            np.save('r1_%s%s.npy'%(sv,ov),maak(sv,ov))
