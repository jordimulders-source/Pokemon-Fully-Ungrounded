# Eindkeuring: omlijningsronde (DC) + schaduwsikkel geel. Varianten V1 (alleen lijn), V2 (lijn + sikkel), eindversie.
import numpy as np
from PIL import Image
from lijn import *
im,a=laad(); F=bevroren(a); L=np.load('mlum.npy')
HANDMATIG={}
def stap_lijn(a):
    o=a.copy(); log=[]
    for x,y,nx,ny,own,m in analyse(a):
        if F[y,x] or not licht(nx,ny): continue
        t={'Y':7,'I':11,'R':14}.get(own)        # donker lijf: outline base = zwart (zoals Poliwag/Poliwhirl)
        if t==14: continue                       # spiraaleinde aan de buikrand: zwart laten (spiraal bevroren, zie NOTITIES)
        if t:
            # regel 4 (r. 111-116): de lijn moet donkerder zijn dan het vlak erachter. Is het eigen vlak naast de lijn
            # al de donkerste tint (geel 7 / ijs b), dan valt een outline base weg in het vlak -> zwart laten.
            binnen=[a[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64
                    and a[y+dy,x+dx] in (YEL if own=='Y' else ICE)]
            vier=[a[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64]
            if (binnen and sum(v==t for v in binnen)*2>=len(binnen)) or t in vier:
                HANDMATIG[(x,y)]='bleef 1: vlak ernaast = %d'%t; continue
            o[y,x]=t; log.append((x,y,own,t))
    return o,log
DONKER=(1,2,3)
def sikkel(o):
    """geel 5/6 met aan de schaduwkant (rechts, onder, rechtsonder) zwart of donker lijf:
    modelschaduwzone (lum<190) -> 7 (zoals Poliwhirl V3), vlakke modelzone -> 5 wordt 6 (1 px sikkel langs de vorm)."""
    s=o.copy(); log=[]
    for y in range(1,63):
        for x in range(1,63):
            v=o[y,x]
            if v not in (5,6) or F[y,x] or np.isnan(L[y,x]): continue
            r,d,dr=o[y,x+1],o[y+1,x],o[y+1,x+1]
            # alleen waar de vorm aan de lichtkant doorloopt (links resp. boven ook geel): een vorm van 1 px dik
            # (teen, smalle strook) houdt zijn licht, anders verdwijnt het hooglicht (linkervoet r56).
            rechts=r in DONKER and o[y,x-1] in YEL
            onder=(d in DONKER or dr in DONKER) and o[y-1,x] in YEL
            if not (rechts or onder): continue
            if L[y,x]<190: t=7
            elif v==5: t=6
            else: continue
            s[y,x]=t; log.append((x,y,int(v),t))
    return s,log
def opslaan(arr,fn):
    p=Image.fromarray(arr.astype('uint8'),'P'); p.putpalette(im.getpalette()); p.save(fn,transparency=0)
if __name__=='__main__':
    v1,ll=stap_lijn(a); v2,sl=sikkel(v1); print('lijn bleef zwart',HANDMATIG)
    np.save('V1.npy',v1); np.save('V2.npy',v2)
    print('lijn',len(ll),ll); print('sikkel',len(sl),sl)
def clusters(m):
    seen=np.zeros(m.shape,bool); out=[]
    for y,x in np.argwhere(m):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            j,i=st.pop(); c.append((i,j))
            for dj in (-1,0,1):
                for di in (-1,0,1):
                    J,I=j+dj,i+di
                    if 0<=J<64 and 0<=I<64 and m[J,I] and not seen[J,I]: seen[J,I]=True; st.append((J,I))
        out.append(c)
    return out
def opschonen(s,voor):
    """nieuwe tintpixels (6 of 7, niet op de buitenrand) die een groepje < 3 px vormen gaan terug naar hun waarde vóór de
    sikkel: geen tintvlakjes < 3 px (SPRITE_KERN 'Netheid')."""
    s=s.copy(); log=[]; P=np.pad(s,1)
    rand=lambda x,y: any(P[y+1+dy,x+1+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
    for k in (7,6):
        for c in clusters(s==k):
            if len(c)<3:
                for i,j in c:
                    if s[j,i]!=voor[j,i] and not rand(i,j): log.append((i,j,k,int(voor[j,i]))); s[j,i]=voor[j,i]
    return s,log
if __name__=='__main__':
    v3,cl=opschonen(v2,v1); np.save('V3.npy',v3); print('opgeschoond',cl)
    # Eindversie: V3 + (45,10) terug naar 1: enige outline-base-pixel tussen zwart (boven) en de ijslijn (rechts) op de
    # rechterkopflank; alleen zou hij als los vlekje in de zwarte lijn lezen (Gnomad r10: geen zwart/outline base om en om).
    ek=v3.copy(); ek[10,45]=1
    # Om-en-om oplossen (SPRITE_KERN: "nooit zwart en ... om en om op een rand"): de regel 'vlak ernaast al donkerste tint
    # -> zwart' liet losse zwarte pixels tussen outline base staan. Per rand een doorlopende keuze:
    for x,y in ((9,21),(1,27),(1,33)): ek[y,x]=11      # ijs: hele lichtkant b (handschoen links, schouderkristal)
    ek[41,19]=7                                         # linkerdij bovenrand: 7-7-7 doorlopend
    for (x,y) in [(x,y) for y in range(51,64) for x in range(64) if ek[y,x]==7 and a[y,x]==1]:
        ek[y,x]=1                                       # voeten: vlak is 6/7 (donkerste geel) -> hele voetrand zwart
    ek[23,55]=6      # rechterbovenarm: enige 5 tussen sikkel 6-6 en 7 (boven zwart, dus door de 1-px-regel overgeslagen)
    ek[41,21]=7      # linkerdij: losse 6 tussen 7-en na de sikkel -> 7 (geen eenling)
    opslaan(ek,'poliwrath_regional_ek.png'); np.save('ek.npy',ek)
    Image.open('poliwrath_regional_ek.png').convert('RGBA').resize((512,512),Image.NEAREST).save('poliwrath_regional_ek_8x.png')
