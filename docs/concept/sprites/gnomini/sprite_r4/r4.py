# r4.py: zichtbare lijfomtrek (tussen armpjes en voetjes, rijen 46-52) als vloeiende Gen 3-curve vanaf r3-B.
# Per rij de linker- en rechterrand (omlijningspixel) van het lijf; achter armpjes/voetjes loopt het lijf door.
# Muts, neus, armpjes, voetjes: diff 0. Ring-grens + donkerblauwe streep en tonen volgen de nieuwe vorm.
import sys, os, numpy as np; from PIL import Image
os.chdir('../sprite_r1'); sys.path.insert(0,'.'); from gemeen import opslaan; os.chdir('../sprite_r4')
o=np.asarray(Image.open('r3B.png')).astype(int)
z=np.load('../sprite_r1/zone_A.npy')
ROZE=[6,7,8,9]; BLAUW=[10,11,12,13]
ander=(z>0)&(z!=3); ander[40:47,13:21]|=o[40:47,13:21]>0     # incl. rond armpje L uit r3
def b(x): u=(x-31.5)/11.0; return int(round(44.0+3.4*(1-u*u)))
# r3:  L 47:20 48:21 49:22 50:22 | R 46:43 47:43 48:42 49:42 50:41 51:41 52:40  (links 1-1-2, rechts 2-2-2 = rechte trap)
RAND={'A':({47:20,48:21,49:21,50:22,51:22},{46:43,47:43,48:43,49:42,50:42,51:41,52:40}),     # runs 1-2-1 / 3-2-1-1
      'B':({47:20,48:20,49:20,50:21,51:21},{46:43,47:43,48:43,49:43,50:42,51:41,52:40})}     # bol: 3-2 / 4-2-1
def maak(var):
    Lr,Rr=RAND[var]; n=o.copy()
    oud_lijf=(z==3)|((z==0)&(o>0))
    for y in range(46,53):
        l=Lr.get(y,min(x for x in range(64) if oud_lijf[y,x] or ander[y,x])); r=Rr.get(y)
        for x in range(14,50):
            if ander[y,x]: continue
            if l<=x<=r: 
                if n[y,x]==0: n[y,x]=12
            elif n[y,x]>0: n[y,x]=0
        for x in (l,r):
            if not ander[y,x]: n[y,x]=1
    # vlak: alle lijfpixels (zone 3 of nieuw) zonder eigen omlijning; omlijning = lijfpixel met achtergrondbuur
    fg=n>0; lijf=(~ander)&fg&(np.arange(64)[:,None]>=41)&(np.arange(64)[:,None]<=55)&((z==3)|(z==0))
    rand=np.zeros((64,64),bool)
    for y,x in zip(*np.where(lijf)):
        if any(not fg[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): rand[y,x]=True
        if y>=47 and (z[y,x+1]==5): rand[y,x]=True   # lijn tegen de onderkant van armpje R blijft (zoals r3)
    vlak=lijf&~rand&~((z==3)&(o==1)&~(np.arange(64)[:,None]>=46))
    oud_vlak=(z==3)&np.isin(o,ROZE+BLAUW); oy,ox=np.where(oud_vlak)
    for y,x in zip(*np.where(vlak)):
        if oud_vlak[y,x]: t=(ROZE+BLAUW).index(o[y,x])%4
        else:
            i=np.argmin((oy-y)**2+(ox-x)**2); t=(ROZE+BLAUW).index(o[oy[i],ox[i]])%4
        if t==0: t=2
        n[y,x]=(BLAUW if y>=b(x) else ROZE)[t]
    # schaduwkant: binnenste pixel tegen de rechterrand -> schaduw; linkerrand onder de ring houdt zijn toon
    for y,x in zip(*np.where(vlak&(np.arange(64)[:,None]>=46))):
        if rand[y,x+1] and n[y,x] in BLAUW: n[y,x]=11
    for y,x in zip(*np.where(rand)): n[y,x]=1

    s=n.copy()
    for y,x in zip(*np.where(vlak)):
        if n[y,x] in BLAUW and any(n[y+dy,x+dx] in ROZE and vlak[y+dy,x+dx] for dy,dx in ((-1,0),(0,-1),(0,1))): s[y,x]=10
    opslaan(s,'gnomini_%s.png'%var)
    d=s!=o; zl=np.isin(z,[0,3])
    print(var,'| lijf (vlak+eigen rand):',(d&zl).sum(),'| muts',(d&(z==1)).sum(),'neus',(d&(z==2)).sum(),'arm L',(d&(z==4)).sum(),'arm R',(d&(z==5)).sum(),
          'voet L',(d&(z==6)).sum(),'voet R',(d&(z==7)).sum(),'| silhouet',((s>0)!=(o>0)).sum())
maak('A'); maak('B')
