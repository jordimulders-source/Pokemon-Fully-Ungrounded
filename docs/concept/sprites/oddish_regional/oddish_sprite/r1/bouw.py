# r1: model overnemen. Natief raster (57x60, pitch 10,24) -> 33x35 op de plek van de Oddish uit de game (x21-53, y14-48).
# Verkleinen = oppervlakteweging per spritepixel (vlakgemiddelde); daarna alleen technische opschoning, elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen(); H,W=c.shape
def overlap(X,Y):
    ua=(X-X0)/S+U0-PHX; ub=ua+1/S; va=(Y-Y0)/S+V0-PHY; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))*S*S
            if w>0 and 0<=u<W and 0<=v<H: yield u,v,w
TEAL={2,3,4,5}; OLIJF={6,7,8,9}; ROOD={10,11,12}
# lange donkerbruine modellijnen (bladranden/-naden, >= 5 natieve px); korte vlekjes tellen als vlak
lab,n=label(c==6); lang=np.isin(lab,[i for i in range(1,n+1) if (lab==i).sum()>=5])
# --- 1. kale reductie ---
o=np.zeros((64,64),int)
for Y in range(10,54):
    for X in range(16,60):
        f={}; lumO=[0,0]; o6=0
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]=f.get(k,0)+w
            if k in (7,8,9) or (k==6 and not lang[v,u]): lumO[0]+=w*L[v,u]; lumO[1]+=w
            if k==6 and lang[v,u]: o6+=w
        if f.get(0,0)>0.5: continue
        if f.get(1,0)>=0.25: o[Y,X]=1; continue
        t=sum(f.get(k,0) for k in TEAL); ol=sum(f.get(k,0) for k in OLIJF); r=sum(f.get(k,0) for k in ROOD)
        if t>=ol and t>=r: o[Y,X]=max(TEAL,key=lambda k:f.get(k,0))
        elif ol>=r:
            if o6>=0.25 or lumO[1]==0: o[Y,X]=6
            else:
                l=lumO[0]/lumO[1]; o[Y,X]=9 if f.get(9,0)>=0.3 else 7 if l<128 else 8 if l<175 else 9
        else: o[Y,X]=4   # rood: gezicht komt hieronder
kaal=o.copy(); opslaan(kaal,'r1/kaal.png')
# --- 2. gezicht: modelplek en modelkleuren (oppervlak rood per pixel gemeten; glans < 1/2 spritepixel valt weg) ---
GEZ={(32,27):11,(33,27):11,(33,33):11,(34,33):11,(36,29):10,(36,30):10,(37,29):10,(37,30):11}
for (Y,X),k in GEZ.items(): o[Y,X]=k
print('gezicht: %d px anders dan kaal'%(o!=kaal).sum())
# --- 2b. zebra: twee kelplijnen op 2 px afstand met 1 px vlak ertussen (a_a) worden streepjes; de kortste lijn (in de sprite) wijkt voor de vlaktint ---
def zebra(o):
    lab,n=label(o==6); grootte={i:(lab==i).sum() for i in range(1,n+1)}; paren={}
    for Y in range(64):
        for X in range(62):
            for dy,dx in ((0,1),(1,0)):
                a1=(Y,X); m=(Y+dy,X+dx); a2=(Y+2*dy,X+2*dx)
                if a2[0]>63 or a2[1]>63: continue
                if o[a1]==6 and o[a2]==6 and o[m] in (7,8,9) and lab[a1]!=lab[a2]:
                    k=tuple(sorted((lab[a1],lab[a2]))); paren.setdefault(k,[]).append((a1,a2))
    tel=0
    for (l1,l2),lst in paren.items():
        if len(lst)<3: continue            # alleen een echte ladder (>= 3 keer a_a tussen dezelfde twee lijnen)
        klein=l1 if grootte[l1]<=grootte[l2] else l2
        for a1,a2 in lst:
            for pt in (a1,a2):
                if lab[pt]==klein and o[pt]==6:
                    Y,X=pt; nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (7,8,9)]
                    if nb: o[Y,X]=max(set(nb),key=nb.count); tel+=1
    return tel
print('zebra: %d px'%zebra(o))
# --- 3. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = zwart (schaduwkant); lichtkant = donkerste tint van de groep ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        if o[Y,X]==1 or o[Y,X] in ROOD: continue
        bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
        if not(bgL or bgR or bgU or bgD): continue
        uit.append((Y,X,1 if (bgR or bgD) else (2 if o[Y,X] in TEAL else 6)))
    for Y,X,k in uit: o[Y,X]=k
voor=o.copy(); rand(o); print('buitenlijn: %d px'%(o!=voor).sum())
# --- 4. ontkorrelen: tintvlekjes < 3 px (hooglicht < 2 px) nemen de meest voorkomende buurtint van dezelfde groep aan ---
def ontkorrel(o):
    for k,minim in ((3,3),(4,3),(5,2),(7,3),(8,3),(9,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            grp=TEAL if k in TEAL else OLIJF; buur=[]
            for Y,X in zip(*np.where(m)):
                for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                    v=o[Y+dy,X+dx]
                    if v in grp and v!=k and v not in (2,6): buur.append(v)
            if buur: o[m]=max(set(buur),key=buur.count)
voor=o.copy(); ontkorrel(o); ontkorrel(o); print('ontkorrelen: %d px'%(o!=voor).sum())

print('totaal anders dan kaal: %d px'%(o!=kaal).sum(), 'kleuren', len(set(o.ravel()))-1)
ch='.K0123abcdrRw'
print('   '+''.join(str(x%10) for x in range(20,55)))
for y in range(13,50): print('%2d '%y+''.join(ch[v] for v in o[y,20:55]))
opslaan(o,'r1/oddish_r1.png')
for n,(y0,y1) in {'kelp':(13,29),'lijf+gezicht':(29,42),'voeten':(42,50)}.items():
    print(n,'afwijking van de kale reductie: %d px'%(o[y0:y1]!=kaal[y0:y1]).sum())
