# Ronde 4: groter hoofd (H1/H2/H3 = 1,15/1,25/1,35x) uit r5 + r8-ogen op dezelfde schaal, op het r3-lijf.
import numpy as np; from PIL import Image
import hoofd, maak_r3 as m3, maak_r2 as m2, maak_r1 as m1, schoon, bouw
FASE={1.15:(2,1),1.25:(2,0),1.35:(0,2)}     # oogfase waarbij beide r8-ogen oogwit + pupil houden (gezocht, zie rapport)
LOG={}
def log(k,v): LOG.setdefault(k,[]).extend(v if isinstance(v,list) else [v])
def r8_ogen(hl,s):
    f=3/s; dx,dy=FASE[s]; bx,by=80+dx,52+dy
    o=hoofd.oog_r8(f,(bx,by,107+dx,63+dy))
    W=np.argwhere(o==23); gezet=[]
    for r in range(o.shape[0]):
        for c in range(1,o.shape[1]-1):
            v=o[r,c]
            if v not in (1,23,10): continue
            if not any(abs(r-y)<=1 and abs(c-x)<=1 for y,x in W): continue      # alleen wat bij een oog hoort
            nx=bx+(c+0.5)*f; ny=by+(r+0.5)*f
            links=nx<91.5
            tx=nx+(76.5-85 if links else 93-99); ty=ny+(51-57)     # r8-oogmidden -> r5-oogmidden
            j=int((ty-hoofd.Y0)//f); i=int((tx-hoofd.X0)//f)
            if 0<=j<hl.shape[0] and 0<=i<hl.shape[1] and hl[j,i]!=0:
                hl[j,i]={1:2,23:3,10:10}[v]; gezet.append((j,i))
    log('r8-ogen',gezet); return hl
SCHOON=False
def hoofd_labels(s):
    a=hoofd.schone_bron()[0] if SCHOON else hoofd.bron(3)[0]; f=3/s; hl=hoofd.reduceer(a,f)
    hl=schoon.tintclusters(hl,5)
    wit=[(y,x) for y,x in np.argwhere((hl>=20)&(hl<30))]
    for p in wit: hl[tuple(p)]=m3.zand(hl,tuple(p))
    log('r5-oogwit weg',[tuple(p) for p in wit])
    return r8_ogen(hl,s)
def bouw_sprite(s):
    LOG.clear(); m3.LOG.clear()
    lab=m3.basis(); lab=m3.boeilijn(lab)
    # borst/schouder rechts: tintvlakjes < 8 px naar de buurtint
    zone=np.zeros_like(lab,bool); zone[16:32,35:48]=True
    sub=lab.copy(); sub[~zone & (sub>=10)]=sub[~zone & (sub>=10)]
    lab2=schoon.tintclusters(lab.copy(),8); lab[zone]=lab2[zone]
    hl=hoofd_labels(s); f=3/s
    M=hoofd.masker(); oud=[]
    for y in range(64):
        for x in range(64):
            ny,nx=2+3*(y+2)+1,2+3*x+1
            if ny<201 and nx<201 and M[ny,nx] and lab[y,x]: lab[y,x]=0; oud.append((y,x))
    log('oude hoofd weg',oud)
    ox=int(round(30.3-(93-hoofd.X0)/f)); oy=0
    for j in range(hl.shape[0]):
        for i in range(hl.shape[1]):
            if hl[j,i] and 0<=j+oy<64 and 0<=i+ox<64: lab[j+oy,i+ox]=hl[j,i]
    log('hoofd geplaatst',[(ox,oy)])
    # hoofdomlijning (r5 heeft een zwarte lijn rond het hoofd): hoofdpixels die zijdelings/onder aan lijf grenzen -> lijntint
    H=np.zeros((64,64),bool)
    for j in range(hl.shape[0]):
        for i in range(hl.shape[1]):
            if hl[j,i] and 0<=j+oy<64 and 0<=i+ox<64: H[j+oy,i+ox]=True
    rand=[]
    for y in range(64):
        for x in range(64):
            if H[y,x] and lab[y,x] not in (2,3) and any(0<=y+dy<64 and 0<=x+dx<64 and lab[y+dy,x+dx]!=0 and not H[y+dy,x+dx] for dy,dx in ((1,0),(0,1),(0,-1))):
                rand.append((y,x))
    for p in rand: lab[p]=1
    log('hoofdrand (tint)',rand)
    lab=m1.barst_r5_weg(lab); lab,gb=m1.barst(lab)
    lab=m2.schouderglas(lab); lab,_=m2.linkerbol(lab)
    lab=bouw.binnenlijnen(bouw.buitenlijn(lab))
    for p,t in {(20,41):14,(20,43):14,(21,44):13,(51,23):31,(27,39):12}.items():
        if lab[p]!=0: lab[p]=t
    return lab
