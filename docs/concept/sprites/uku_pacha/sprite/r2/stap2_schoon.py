# Uku Pacha r2 stap 2: technisch opschonen van stap 1 (geen nieuwe vormen):
#  - lijnen 1 px dun (Zhang-Suen), buiten de koppen (die worden per pixel naar het model gezet in stap 3)
#  - buitenrand = doorlopende 1 px omlijning
#  - losse vlakpixels (geen 4-buur met dezelfde klasse) -> meerderheid van de buren (ruis weg)
#  - klassen samenvoegen: 5->6 (donkere flank), 1/3/4 -> 2 (binnenlijn), 0 = zwart
import numpy as np
S=np.load('S.npy'); L=np.load('L.npy'); V=np.load('V.npy')
IN=S>=0
KOP=np.zeros((64,64),bool); KOP[2:28,0:32]=True; KOP[2:18,29:51]=True  # koppen: hier niet dunnen
lijn=(L>=0)
def rand(m):
    r=np.zeros_like(m)
    for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        sh=np.zeros_like(m); 
        ys=slice(max(dy,0),64+min(dy,0)); yd=slice(max(-dy,0),64+min(-dy,0))
        xs=slice(max(dx,0),64+min(dx,0)); xd=slice(max(-dx,0),64+min(-dx,0))
        sh[yd,xd]=~m[ys,xs]; r|=sh
    return m&r
RAND=rand(IN)
# Zhang-Suen op lijn|rand, rand en koppen blijven vast
B=lijn|RAND
def nb(m,j,i):
    o=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    return [bool(m[j+a,i+b]) if 0<=j+a<64 and 0<=i+b<64 else False for a,b in o]
changed=True
while changed:
    changed=False
    for stap in (0,1):
        weg=[]
        for j,i in zip(*np.where(B)):
            if RAND[j,i] or KOP[j,i]: continue
            p=nb(B,j,i); n=sum(p)
            if not 2<=n<=6: continue
            a=sum((not p[k]) and p[(k+1)%8] for k in range(8))
            if a!=1: continue
            P2,P3,P4,P5,P6,P7,P8,P9=p
            if stap==0 and (P2 and P4 and P6 or P4 and P6 and P8): continue
            if stap==1 and (P2 and P4 and P8 or P2 and P6 and P8): continue
            weg.append((j,i))
        for j,i in weg: B[j,i]=False
        changed|=bool(weg)
# opgegeven lijnpixels krijgen hun vlakklasse
M=np.where(IN,V,-1)
M[B&~RAND]=np.where(L[B&~RAND]>=0,L[B&~RAND],2)
M[RAND]=0
M[M==5]=6
for k in (1,3,4): M[M==k]=2
LIJNK={0,2}
# losse vlakpixels
for it in range(4):
    for j,i in zip(*np.where(IN)):
        c=M[j,i]
        if c in LIJNK or c>=16: continue
        buren=[M[j+a,i+b] for a,b in ((0,1),(0,-1),(1,0),(-1,0)) if 0<=j+a<64 and 0<=i+b<64]
        if c in buren: continue
        vl=[x for x in buren if x>=0 and x not in LIJNK and x<16]
        if vl:
            M[j,i]=max(set(vl),key=vl.count)
np.save('M2.npy',M)
