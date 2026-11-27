# Eindkeuring ek1 (Dragonfly Cave: schaduw + belijning + kleurtinten) op ../sprite_r3/kuiken_r3_M_i_a.png.
# Alleen uitvoering: silhouet, vlakvormen/lijnen, oog D en kleurrichting (M / i / a) bevroren; alleen tinten en indextoewijzing.
import numpy as np; from PIL import Image
def label(M):
    lab=np.zeros(M.shape,int); n=0
    for y,x in zip(*np.where(M)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
                q=(cy+dy,cx+dx)
                if 0<=q[0]<64 and 0<=q[1]<64 and M[q] and not lab[q]: lab[q]=n; st.append(q)
    return lab,n
SRC='../sprite_r3/kuiken_r3_M_i_a.png'
B0=Image.open(SRC); B=np.array(B0).astype(int); S=B.copy()
PAL=[tuple(B0.getpalette()[i*3:i*3+3]) for i in range(16)]
ML=np.load('../sprite_r1/ml.npy'); FACE=np.load('../sprite_r3/face.npy')
# oog D: Pidgeot-pixels (ogen.py, verschuiving 17,2) + glans (29,28)
OOGPX=[(13,23),(14,23),(15,23),(12,24),(13,24),(14,24),(15,24),(11,25),(12,25),(13,25),(14,25),(15,25),(11,26),(12,26),(13,26),(14,26),(15,26),(11,27),(12,27),(13,27)]
OOG={(y+2,x+17) for (x,y) in OOGPX}|{(28,29)}
LOG=[]
def zet(zone,y,x,v):
    assert (y,x) not in OOG and B[y,x]>0,(y,x)
    if S[y,x]!=v: LOG.append((zone,y,x,int(S[y,x]),v)); S[y,x]=v
N4=((0,1),(1,0),(0,-1),(-1,0))
def nb(y,x): return [(y+dy,x+dx) for dy,dx in N4 if 0<=y+dy<64 and 0<=x+dx<64]
# --- palet: snavelrand (4) deelt de crème-middentint (vrijwel gelijk), index 4 wordt de eigen donkerste gezichtstint ---
for y,x in zip(*np.where(B==4)): zet('snavel',y,x,9)
PAL[9]=(208,184,140)        # gedeelde crème-midden/snavelrand (was 210,180,136 en 200,190,150)
PAL[4]=(102,80,66)          # gezicht donker: eigen outline base (stap 125 -> 87), iets roder (hue shift)
# --- gezicht: schaduw uit de modelhelderheid per pixel (hooglicht linksboven, sikkel naar kaak/achterhoofd) ---
FZ=FACE&np.isin(B,[8,14])
# modelhelderheid 3x3-gemiddeld binnen het gezicht (per-pixelruis van de reductie eruit, de toonverdeling van het model blijft)
_P=np.pad(ML,1,mode='edge'); _W=np.pad(FZ.astype(float),1); SM=np.zeros_like(ML)
for _y in range(64):
    for _x in range(64):
        _w=_W[_y:_y+3,_x:_x+3]; SM[_y,_x]=(_P[_y:_y+3,_x:_x+3]*_w).sum()/max(_w.sum(),1)
for y,x in zip(*np.where(FZ)):
    if (y,x) in OOG: continue
    if y<29: continue                       # kruin/voorhoofd: r3-verdeling blijft (hooglicht linksboven)
    m=SM[y,x]; v=14 if m>=110 else (8 if m>=86 else 4)
    zet('gezicht',y,x,v)
# kleine tintvlakjes (<3 px) in het gezicht terug naar de buurtint
for _ in range(3):
    for t in (4,8,14):
        lab,n=label((S==t)&FZ)
        for k in range(1,n+1):
            cel=list(zip(*np.where(lab==k)))
            if len(cel)>=3: continue
            for y,x in cel:
                tel={}
                for q in nb(y,x):
                    if FZ[q] and S[q]!=t: tel[S[q]]=tel.get(S[q],0)+1
                if tel: zet('gezicht',y,x,max(tel,key=tel.get))
# --- gezicht: selout aan de lichtkant (linksboven) in de eigen donkerste tint i.p.v. de lijftint ---
for y,x in zip(*np.where(B==5)):
    if (y,x) in OOG: continue
    n=nb(y,x)
    face=any(FACE[q] for q in n); body=any(B[q] in (6,7) for q in n)
    if face and not body and y<=26 and x<=26: zet('gezicht-lijn',y,x,4)
# --- binnenlijnen op lijfvlakken: zwart -> donkerste lijftint (DC: binnenlijnen niet zwart) ---
for (y,x) in [(43,36),(44,36),(45,36),(46,36),     # voorrand vleugel over de flank
              (42,26),(43,26),                     # lijn flank/borst links (lichtkant)
              (20,33),(21,35)]:                    # kuifplukjes boven op de kop
    assert B[y,x]==1; zet('binnenlijn',y,x,5)
# --- buitenlijn links van het lijf: was 5/1 om en om; lichtkant boven gekleurd, vanaf de buikbolling zwart (één overgang) ---
for y in range(41,55):
    xs=[x for x in range(20,64) if B[y,x]>0]; x=xs[0]
    if B[y,x] in (1,5): zet('buitenlijn',y,x,5 if y<=47 else 1)
# --- crème: derde (schaduw)tint = gezicht-midden; de lichtbruine vlekjes (7) in de borst worden crème-schaduw (grijsbeige zoals het model) ---
for y,x in zip(*np.where((B==7)&(np.arange(64)[None,:]<=34))):
    if 40<=y<=54: zet('creme',y,x,8)
zet('vlakje',48,25,6)   # los crème-pixel (1 px) tussen twee zwarte lijnen op de buitenrand -> flanktint zoals r44-47
def opslaan(A,pad):
    im=Image.fromarray(A.astype(np.uint8),'P'); fl=[c for p in PAL for c in p]; im.putpalette(fl+[0]*(768-48)); im.save(pad,transparency=0)
if __name__=='__main__':
    opslaan(S,'kuiken_ek1.png')
    from collections import Counter
    for z,n in Counter(l[0] for l in LOG).items(): print(z,n)
    print('totaal',len(LOG))
    for y in range(18,0): print('%2d '%y+''.join('.' if v==0 else '0123456789ABCDEF'[v] for v in S[y,8:44]))
