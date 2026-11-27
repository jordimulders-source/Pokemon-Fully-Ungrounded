# Ronde 5 op H2: hoofd opschonen op spriteniveau (alleen weghalen/verschuiven/tint), schouder, arm, handen.
import numpy as np; from PIL import Image
import hoofd, bewerk, maak_r4 as m4, maak_r2 as m2, schoon
LOG={}
def log(k,v): LOG.setdefault(k,[]).extend(v if isinstance(v,list) else [v])
z=np.zeros((201,201),bool)
for y,(l,r) in bewerk.HOOFD.items(): z[y,l:r+1]=True
hoofd.BREIN=z; m4.SCHOON=True
def basis():
    lab=m4.bouw_sprite(1.25)
    hl=m4.hoofd_labels(1.25); ox=int(round(30.3-(93-hoofd.X0)/(3/1.25)))
    H=np.zeros((64,64),bool)
    for j in range(hl.shape[0]):
        for i in range(hl.shape[1]):
            if hl[j,i] and j<64 and 0<=i+ox<64: H[j,i+ox]=True
    return lab,H
KRUL=[(7,27),(8,27),(9,27),(10,26),(11,26),(12,25),            # krul links (boog)
      (11,32),(10,33),(9,34),(9,35),(10,36),(11,37)]           # krul rechts (koepel)
MOND=[(21,23),(21,24),(21,25),(21,31),(20,32)]+[(22,x) for x in range(27,35)]
WENKBRAUW_VERSCHUIF=[((15,21),(15,22)),((14,23),(15,23)),((15,25),(16,24)),   # links: buiten hoog, binnen laag
                     ((16,31),(16,30))]                                         # rechts: (15,31),(15,32) blijven
WENKBRAUW_BLIJFT=[(15,31),(15,32)]
def zandbuur(lab,p,uit):
    c={}
    for dy,dx in schoon.N8:
        q=(p[0]+dy,p[1]+dx)
        if 0<=q[0]<64 and 0<=q[1]<64 and 11<=lab[q]<=14 and q not in uit: c[lab[q]]=c.get(lab[q],0)+1
    return max(c,key=c.get) if c else 12
def hoofd_schoon(lab,H):
    # 1) wenkbrauwen verschuiven
    for a,b in WENKBRAUW_VERSCHUIF:
        if lab[a]==10: lab[b]=10; lab[a]=-1
    houd=set(KRUL+MOND+WENKBRAUW_BLIJFT+[b for a,b in WENKBRAUW_VERSCHUIF])
    weg=[]
    for y in range(4,22):
        for x in range(17,44):
            if not H[y,x] or (y,x) in houd: continue
            v=lab[y,x]
            if v not in (10,-1): continue
            if any(lab[y+dy,x+dx]==0 for dy,dx in schoon.N4) or any(not H[y+dy,x+dx] and lab[y+dy,x+dx]!=0 for dy,dx in ((1,0),(0,1),(0,-1))):
                if v==-1: lab[y,x]=10
                continue                                   # omtrek blijft
            weg.append((y,x))
    for p in weg: lab[p]=-1
    for p in weg: lab[p]=zandbuur(lab,p,set(weg))
    for p in weg:
        if lab[p]==-1: lab[p]=12
    log('hoofdlijnen weg',weg); log('wenkbrauw verschoven',WENKBRAUW_VERSCHUIF)
    # 2) tintvlakjes in het hoofd < 5 px naar de buurtint
    sub=lab.copy(); sub[lab==10]=5          # lijntint tijdelijk buiten het zandmateriaal, zodat vlakjes geen lijn worden
    sub=schoon.tintclusters(sub,5); sub[lab==10]=10
    d=[(y,x) for y,x in zip(*np.where((sub!=lab)&H))]
    for p in d: lab[p]=sub[p]
    log('hoofd tintvlakjes',d)
    # 2b) brein (rij 5-13): donkere zandtint S1 -> S2, zodat de krullen leesbaar blijven (tintkeuze; schaduwkant blijft via S2/S3-verschil)
    br=[(y,x) for y in range(5,14) for x in range(17,44) if H[y,x] and lab[y,x]==11]
    for p in br: lab[p]=12
    log('brein S1->S2 (tint)',br)
    # 3) ogen vrij: donkere zandtint (S1) direct rond de ogen -> S2
    ogen=list(zip(*np.where(((lab==2)|(lab==3))&H)))
    vrij=[]
    for y,x in ogen:
        for dy,dx in schoon.N8:
            q=(y+dy,x+dx)
            if lab[q]==11: lab[q]=12; vrij.append(q)
    log('ogen vrij (tint)',vrij)
    return lab

# --- rechterschouder: vloeiende boog door pixels voorbij de boog weg te halen (alleen weghalen + lijn mee) ---
BOOG_R={15:44,16:45,17:45,18:46,19:46,20:46,21:46,22:46,23:46,24:46,25:45,26:44,27:43,28:43,29:42,30:42,31:42,32:42,33:41,34:41,35:40}
def schouder(lab):
    weg=[];lijn=[]
    for y,t in BOOG_R.items():
        for x in range(t+1,64):
            if lab[y,x]!=0: lab[y,x]=0; weg.append((y,x))
        if lab[y,t]!=0 and lab[y,t] not in (1,): lab[y,t]=1; lijn.append((y,t))
    log('schouder weg',weg); log('schouderlijn (tint)',lijn); return lab
# --- linkerarm: buitenrand per rij op de afgeronde modelrand (r5, natief silhouet /3) ---
ARM_L={17:17,21:15,22:14}
def arm(lab):
    gedaan=[]
    for y,t in ARM_L.items():
        xs=np.where(lab[y]>0)[0]; e=xs.min(); rand=lab[y,e]; binnen=lab[y,e+1]
        if t>e:
            for x in range(e,t): lab[y,x]=0
            lab[y,t]=rand
        else:
            lab[y,t]=rand
            for x in range(t+1,e+1): lab[y,x]=binnen if 11<=binnen<=14 else 13
        gedaan.append((y,e,t))
    log('armrand verschoven',gedaan); return lab
# --- linkerhand: zand rond de kleine boeien één lichte tint, losse binnenlijnen weg ---
def hand(lab,zone=(12,23,20,33)):
    x0,y0,x1,y1=zone; weg=[]; tint=[]
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            v=lab[y,x]
            if v==10:
                nb=[lab[y+dy,x+dx] for dy,dx in schoon.N4]
                if any(n==0 or 20<=n<30 for n in nb): continue      # omtrek en boeilijn blijven
                weg.append((y,x))
            elif 11<=v<=14 and v!=13: tint.append((y,x))
    for p in weg+tint: lab[p]=13
    log('hand losse lijnen weg',weg); log('hand tint S3',tint); return lab
def bouw_sprite():
    LOG.clear()
    lab,H=basis(); lab=hoofd_schoon(lab,H); lab=schouder(lab); lab=arm(lab); lab=hand(lab)
    # losse 1-px-zandtintjes -> meest voorkomende zand-buurtint
    los=[]
    for t in (11,12,13,14):
        for c in schoon.comps4(lab==t):
            if len(c)==1: los.append(c[0])
    for p in los:
        c={}
        for dy,dx in schoon.N8:
            q=(p[0]+dy,p[1]+dx)
            if 0<=q[0]<64 and 0<=q[1]<64 and 11<=lab[q]<=14 and lab[q]!=lab[p]: c[lab[q]]=c.get(lab[q],0)+1
        if c: lab[p]=max(c,key=c.get)
    log('losse pixels (tint)',los)
    # donker vlekje (S1, 2x2) tussen de ogen -> S2, zodat de ogen vrij staan
    vl=[(16,26),(16,27),(17,26),(17,27)]
    for p in vl:
        if lab[p]==11: lab[p]=12
    log('vlek tussen ogen (tint)',vl)
    return lab
