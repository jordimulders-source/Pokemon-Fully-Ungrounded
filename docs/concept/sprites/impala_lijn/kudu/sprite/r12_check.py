# Ronde 12 controle: rechte lijnstukken voor/na, pixeldiff-zone, oogvlak, tintvlakjes, 0/d om en om.
import r12, r8lib as L, numpy as np
OOG={(x,y) for x in range(9,15) for y in range(21,27)}   # oogvlak K4, zelfde als vel8.OOG (vel8 importeren herschrijft r8/)
from scipy import ndimage as nd
G,B=r12.G,r12.B6A
H,W=L.H,L.W
def lijnpix(g):
    return {(x,y) for y in range(H) for x in range(W) if g[y][x] in '0dK' and
            any(0<=x+a<W and 0<=y+b<H and g[y+b][x+a] in 'lm' for a in(-1,0,1) for b in(-1,0,1))}
def rechte(g):
    P=lijnpix(g); out=[]
    for y in range(H):
        run=[]
        for x in range(W+1):
            if (x,y) in P: run.append(x)
            else:
                if len(run)>3: out.append(('h',y,run[0],run[-1]))
                run=[]
    for x in range(W):
        run=[]
        for y in range(H+1):
            if (x,y) in P: run.append(y)
            else:
                if len(run)>3: out.append(('v',x,run[0],run[-1]))
                run=[]
    return out
manen=lambda g:{(x,y) for y in range(H) for x in range(W) if g[y][x] in 'lm'}
def omtrek(S,g):   # manen/franje-vulling + hun lijnpixels
    return S|lijnpix(g)
HALS_OUD=set(L.HALS); HALS_NIEUW={(x,y) for x,y in L.HALS|{(15,33),(15,34),(15,35),(16,36),(16,37),(16,38),(12,29),(13,29)} if G[y][x]=='M'} - {(14,28),(14,29)}
KERN=omtrek(manen(B),B)|omtrek(manen(G),G)|HALS_OUD|HALS_NIEUW
KERN={p for p in KERN if p[0]<40}            # (49,42) is een losse l op de rechterrand, geen manen
ZONE={(x+a,y+b) for x,y in KERN for a in(-1,0,1) for b in(-1,0,1)}
diff={(x,y) for y in range(H) for x in range(W) if G[y][x]!=B[y][x]}
def clusters(g,pts):
    bad=[]
    for c in 'lmLMD':
        A=np.zeros((H,W),bool)
        for y in range(H):
            for x in range(W):
                if g[y][x]==c: A[y,x]=True
        lab,n=nd.label(A,structure=np.ones((3,3)))
        for k in range(1,n+1):
            p={(int(x),int(y)) for y,x in np.argwhere(lab==k)}
            if len(p)<3 and p&pts: bad.append((c,sorted(p)))
    return bad
OMG={(x+a,y+b) for x,y in diff for a in range(-2,3) for b in range(-2,3)}
if __name__=='__main__':
    print('rechte lijnstukken >3 px (0/d/K naast manen/franje-vulling): B6a',rechte(B),'| r12',rechte(G) or 'geen')
    print('pixels anders dan B6a: %d; buiten manen+franje+halsstrook+1px: %d %s; oogvlak: %d'%(len(diff),len(diff-ZONE),sorted(diff-ZONE),len(diff&OOG)))
    print('tintvlakjes <3 px rond de wijzigingen: B6a',clusters(B,OMG),'| r12',clusters(G,OMG))
    print('kleuren incl. transparant:',len({c for r in G for c in r}))
