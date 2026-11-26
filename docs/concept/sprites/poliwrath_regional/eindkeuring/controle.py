import numpy as np, sys
from PIL import Image
from zones import *
im,a=laad(); fn=sys.argv[1] if len(sys.argv)>1 else 'poliwrath_regional_ek.png'
b=np.array(Image.open(fn)) if fn.endswith('.png') else np.load(fn)
F=bevroren(a)
if fn.endswith('.png'): assert Image.open(fn).getpalette()[:48]==im.getpalette()[:48]; print('palet byte-gelijk aan r2_E2M1: ja')
print('alpha-diff', int(((a==0)!=(b==0)).sum()))
print('bevroren zone diff', int((F&(a!=b)).sum()), 'van', int(F.sum()), 'px')
mat=lambda v: np.select([np.isin(v,YEL),np.isin(v,ICE),np.isin(v,DARK),np.isin(v,RED),v==1],[1,2,3,4,5],0)
ch=(a!=b); ma,mb=mat(a),mat(b)
ok=(ma==mb)|((ma==5)&np.isin(mb,[1,2,4]))   # lijnpixel -> outline base eigen materiaal (geel 7, ijs b, rood e)
print('materiaalwissels buiten lijn->outline base:', int((ch&~ok).sum()))
print('gewijzigd totaal', int(ch.sum()))
for z,(y0,y1) in {'kop (r0-22)':(0,23),'romp/armen (r23-40)':(23,41),'benen/voeten (r41-63)':(41,64)}.items():
    print(' ',z, int(ch[y0:y1].sum()))
for (p,q) in sorted({(int(x),int(y)) for x,y in zip(a[ch],b[ch])}):
    print('  %x->%x: %d'%(p,q,int(((a==p)&(b==q)).sum())))
print('kleuren gebruikt (incl. transparant):', len(np.unique(b)), '/ palet 16')
print('zwart (1):', int((a==1).sum()),'->',int((b==1).sum()), '= %.1f %% van'%(100*(b==1).sum()/(b>0).sum()), int((b>0).sum()))
for k,v in ((5,'geel licht'),(6,'geel'),(7,'geel donker')):
    print(' %s (%d): %d -> %d'%(v,k,(a==k).sum(),(b==k).sum()))
P=np.pad(b,1)
rand=[(x,y) for y in range(64) for x in range(64) if b[y,x] and any(P[y+1+dy,x+1+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))]
LICHT=(5,6,8,9,10,12,13)
lr=[(x,y,int(b[y,x])) for x,y in rand if b[y,x] in LICHT]
print('lichte pixels (5,6,8,9,a,c,d) op de buitenrand:', len(lr), lr)
print('  (ter vergelijking r2_E2M1:', sum(1 for y in range(64) for x in range(64) if a[y,x] in LICHT and any(np.pad(a,1)[y+1+dy,x+1+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))),')')
# losse pixels: geen enkele 4-buur met dezelfde index, en ook geen 8-buur (echte eenlingen), buiten bevroren zones
los=[]
for y in range(64):
    for x in range(64):
        v=b[y,x]
        if not v or F[y,x]: continue
        n8=[P[y+1+dy,x+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
        if v not in n8: los.append((x,y,int(v)))
print('eenlingen (geen 8-buur met dezelfde index, buiten bevroren):', len(los), los)
los_a=sum(1 for y in range(64) for x in range(64) if a[y,x] and not F[y,x] and a[y,x] not in [np.pad(a,1)[y+1+dy,x+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx])
print('  (r2_E2M1:', los_a, ')')
# zwart (1) binnen het silhouet dat niet aan lucht grenst, buiten bevroren
zb=[(x,y) for y in range(64) for x in range(64) if b[y,x]==1 and not F[y,x] and not any(P[y+1+dy,x+1+dx]==0 for dy in (-1,0,1) for dx in (-1,0,1))]
print('zwarte binnenpixels buiten bevroren:', zb)
# om-en-om zwart / outline base langs de buitenrand: buitenlijnpixel 1 met aan twee kanten (langs de rand) 7/b en geen 1-buur op de rand
oo=[]
RS=set(rand)
for x,y in rand:
    if b[y,x]!=1: continue
    nb=[(x+dx,y+dy) for dy in (-1,0,1) for dx in (-1,0,1) if (dx or dy) and (x+dx,y+dy) in RS]
    vals=[b[j,i] for i,j in nb]
    if vals and 1 not in vals and sum(v in (7,11,14) for v in vals)>=2: oo.append((x,y))
print('zwarte eenling tussen outline base op de rand (om-en-om):', oo)
def clusters(m):
    seen=np.zeros(m.shape,bool); out=[]
    for y,x in np.argwhere(m):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            j,i=st.pop(); c.append((i,j))
            for dj,di in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                J,I=j+dj,i+di
                if 0<=J<64 and 0<=I<64 and m[J,I] and not seen[J,I]: seen[J,I]=True; st.append((J,I))
        out.append(c)
    return out
for k in (6,7):
    nieuw=[c for c in clusters((b==k)&~F) if len(c)<3 and any(ch[j,i] for i,j in c)]
    print('nieuwe %d-clusters <3 px (8-verbonden) door de ronde:'%k, nieuw)
