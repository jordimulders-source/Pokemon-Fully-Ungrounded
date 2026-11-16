# r4 = r3 + ontruisen (Krassault-recept), geen hertekening.
# Bevroren: gezichtszone (x 0-23, y 29-48; uitzondering: bovenooglid herkleuren naar zwart), wolken en wielen
# (alle groene tinten 2-6 met x >= 22 en y >= 14). Kleine geest opnieuw geschrapt met kopring/ogen beschermd.
import sys; sys.path.insert(0,'.')
from schrap_deel import *
from PIL import Image
r3=Image.open('../sprite_r3/sprite.png'); O=np.array(r3).astype(int); R3=O.copy(); H,W=O.shape
GEZ=(0,23,29,48)
def in_gez(x,y): return GEZ[0]<=x<=GEZ[1] and GEZ[2]<=y<=GEZ[3]
def bevroren(x,y): return in_gez(x,y) or (x>=22 and y>=14 and R3[y,x] in (2,3,4,5,6))
N4=[(0,1),(1,0),(0,-1),(-1,0)]; N8=N4+[(1,1),(1,-1),(-1,1),(-1,-1)]
def nb(y,x,d=N8):
    for dy,dx in d:
        if 0<=y+dy<H and 0<=x+dx<W: yield y+dy,x+dx,O[y+dy,x+dx]
def rand(y,x): return any(not(0<=y+dy<H and 0<=x+dx<W) or O[y+dy,x+dx]==0 for dy,dx in N4)
def clusters(mask):
    lab=np.zeros(mask.shape,int); out=[]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        st=[(y,x)]; lab[y,x]=1; cl=[]
        while st:
            cy,cx=st.pop(); cl.append((cy,cx))
            for dy,dx in N8:
                ny,nx=cy+dy,cx+dx
                if 0<=ny<H and 0<=nx<W and mask[ny,nx] and not lab[ny,nx]: lab[ny,nx]=1; st.append((ny,nx))
        out.append(cl)
    return out
METAAL=(7,8,9,10,11,12)
# 1) bovenooglid: donkere pixels direct boven het oog-groen (binnen de oogkolommen) -> zwart
lid=[]
for y in range(GEZ[2],GEZ[3]+1):
    for x in range(GEZ[0],GEZ[1]+1):
        if O[y,x] in (6,9,12) and y+1<H and O[y+1,x] in (2,3) and y<=33:   # alleen boven de ogen (rij 29-33), niet de mondhoek
            O[y,x]=1; lid.append((x,y))
# 2) kleine geest: oude geest (groen in y<=13, x>=12) weg, nieuwe schrapversie (27x13, kop x30-36/y12-19 beschermd) erin
g,_,_,_,_=verklein(29,62,6,22,27,13,tuple(range(30,37)),tuple(range(12,20)))
oud=[(y,x) for y in range(0,14) for x in range(12,W) if O[y,x] in (2,3,4,5,6)]
best=None
for Y in range(0,4):
    for X in range(12,19):
        sc=sum(1 for y in range(13) for x in range(27) if g[y,x] and 0<=Y+y<H and 0<=X+x<W and R3[Y+y,X+x] in (2,3,4,5,6))
        if best is None or sc>best[0]: best=(sc,X,Y)
_,GX,GY=best
for y,x in oud: O[y,x]=0
for y in range(13):
    for x in range(27):
        if g[y,x] and GY+y<=13 and g[y,x] in (2,3,4,5,6): O[GY+y,GX+x]=g[y,x]
# 3) metaal ontruisen buiten de bevroren zones: clusters < 3 px en 1-px-uitsteeksels nemen de meest voorkomende
#    metaal-buurtint; losse zwarte binnenpixels (raken geen lucht, cluster < 3) ook. Randpixels (buitenlijn) blijven.
for ronde in range(3):
    for t in METAAL+(1,):
        for cl in clusters(O==t):
            if len(cl)>=3: continue
            for (y,x) in cl:
                if bevroren(x,y) or rand(y,x) or y<=13: continue
                c=[v for _,_,v in nb(y,x) if v in METAAL and v!=t]
                if c: O[y,x]=max(set(c),key=c.count)
    for y in range(H):
        for x in range(W):
            t=O[y,x]
            if t not in METAAL or bevroren(x,y) or rand(y,x): continue
            if sum(1 for _,_,v in nb(y,x,N4) if v==t)<=1:
                c=[v for _,_,v in nb(y,x,N4) if v in METAAL and v!=t]
                if len(c)>=2: O[y,x]=max(set(c),key=c.count)
# 3b) koeienvanger (x 0-23, y 49-62, onder de gezichtszone): sterker, clusters < 5 px van metaal en zwart binnenin
#     nemen de metaal-buurtint (grote spijlvlakken en de echte tussenruimtes blijven), 2 rondes meerderheidsfilter metaal.
KV=(0,23,49,62)
for ronde in range(2):
    for t in METAAL+(1,):
        for cl in clusters(O==t):
            if len(cl)>=5: continue
            for (y,x) in cl:
                if not (KV[0]<=x<=KV[1] and KV[2]<=y<=KV[3]) or rand(y,x): continue
                c=[v for _,_,v in nb(y,x) if v in METAAL and v!=t]
                if c: O[y,x]=max(set(c),key=c.count)
    n=O.copy()
    for y in range(KV[2],KV[3]+1):
        for x in range(KV[0],KV[1]+1):
            if O[y,x] in METAAL and not rand(y,x):
                c=[v for _,_,v in nb(y,x) if v in METAAL]+[O[y,x]]
                mm=max(set(c),key=c.count)
                if c.count(mm)>c.count(O[y,x]): n[y,x]=mm
    O=n
# 4) buitenlijn van de nieuwe geest: randpixels donkergroen (gekleurde omlijning, zoals de wolken)
for y in range(0,14):
    for x in range(12,W):
        if O[y,x] in (2,3,4,5) and rand(y,x): O[y,x]=6
# bewijs bevriezing
dg=[(x,y) for y in range(H) for x in range(W) if in_gez(x,y) and O[y,x]!=R3[y,x] and (x,y) not in lid]
dw=[(x,y) for y in range(14,H) for x in range(22,W) if R3[y,x] in (2,3,4,5,6) and O[y,x]!=R3[y,x]]
print('ooglid naar zwart:',lid); print('diff gezichtszone buiten ooglid:',len(dg),dg); print('diff wolken/wielen:',len(dw))
print('geest geplakt op',GX,GY,'; pixels gewijzigd totaal:',int((O!=R3).sum()))
im=Image.fromarray(O.astype('uint8'),'P'); im.putpalette(r3.getpalette()); im.save('sprite.png',transparency=0)
with open('raster.txt','w') as f:
    P=r3.getpalette()
    f.write('# index per pixel (0 = transparant, hex), palet:\n')
    for i in range(13): f.write('# %X %s\n'%(i,tuple(P[3*i:3*i+3])))
    for row in O: f.write(''.join('%X'%v if v else '.' for v in row)+'\n')
