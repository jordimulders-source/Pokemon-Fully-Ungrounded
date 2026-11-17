# Ronde 5: lijf = ellips gefit op de modelomtrek (zonder handen/hoorns), bolschaduw (licht linksboven, sikkel rechts/onder),
# linkerhand als want (ellips op de modelomtrek), linkervoet op de grondlijn y60, mond als D met ronde boog.
# Ring, yerba, bombilla, hoorns, ogen, neus, rechterhand en rechtervoet: pixels uit r4.
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image
im=Image.open('r4/mate.png'); PAL=im.getpalette(); r4=np.asarray(im).astype(int)
T1,T2=0.12,0.85; OUT=sys.argv[3] if len(sys.argv)>3 else 'r5/mate.png'
L={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5,'G':6,'H':7,'I':8,'s':9,'t':10,'u':11}
H,W=64,64; Y,X=np.mgrid[0:H,0:W]; px,py=X+0.5,Y+0.5
CX,CY,RX,RY=31.92,42.70,17.80,16.70          # least-squares ellips op de modelomtrek (rest <= 0,9 px)
E=((px-CX)/RX)**2+((py-CY)/RY)**2<=1
HX,HY,HRX,HRY=14.2,46.0,2.7,4.7              # linkerhand: modelomtrek x11,6-(achter het lijf), y41,4-50,6
HL=((px-HX)/HRX)**2+((py-HY)/HRY)**2<=1
# rechterhand uit r4: binnenkant (flood vanaf het midden, begrensd) + haar lijnen
hr=np.zeros((H,W),bool); st=[(46,45)]; hr[46,45]=True
while st:
    y,x=st.pop()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 43<=yy<=50 and 38<=xx<=50 and not hr[yy,xx] and r4[yy,xx] in (3,4,5): hr[yy,xx]=True; st.append((yy,xx))
for y in range(41,53):
    for x in range(37,52):
        if r4[y,x] in (1,2) and any(hr[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1)) : hr[y,x]=True
hr[42,47]=hr[42,48]=True
HR=hr&(r4>0)
VR=np.zeros((H,W),bool); VR[57:63,33:44]=True; VR&=(r4>0)        # rechtervoet r4
TOP=(Y<30)&(r4>0)                                                  # ring, bombilla, hoorns: r4
VL=np.zeros((H,W),bool)                                            # linkervoet, nieuw
VLrows={57:(19,"aaabb#"),58:(18,"#dcccbb#"),59:(18,"#ccccbb#"),60:(19,"######")}
VLpix={}
for y,(x0,r) in VLrows.items():
    for i,ch in enumerate(r): VL[y,x0+i]=True; VLpix[(x0+i,y)]=L[ch]
B=(E|TOP)&~VL                                                      # lijf + bovenkant
a=np.zeros((H,W),int)
# 1. bolschaduw zoals Voltorb: sikkel = lijf minus dezelfde ellips SH px naar linksboven geschoven (gelijke breedte langs
#    rechts/onder), licht = ronde vlek linksboven (voorhoofd links, boven het linkeroog; modellicht), midden ertussen
SH=float(sys.argv[1]) if len(sys.argv)>1 else 3.5
Es=((px-CX+SH*0.75)/RX)**2+((py-CY+SH)/RY)**2<=1
LX,LY,LRX,LRY=(float(v) for v in (sys.argv[4:8] if len(sys.argv)>7 else (24.5,34.5,7.5,6.0)))
D=((px-LX)/LRX)**2+((py-LY)/LRY)**2<=1
a[E]=4; a[E&~Es]=3; a[E&D&Es]=5
u=(px-CX)/RX; v=(py-CY)/RY; w=np.sqrt(np.clip(1-u*u-v*v,0,1))
Ld=np.array([-0.55,-0.65,0.52]); Ld/=np.linalg.norm(Ld); I=u*Ld[0]+v*Ld[1]+w*Ld[2]
a[TOP]=r4[TOP]
# 2. buitenlijn van het lijf (y>=30): selout a aan de lichtkant (links/boven het midden), anders zwart
def buur_buiten(M,y,x): return any(not M[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
for y in range(30,63):
    for x in range(1,63):
        if B[y,x] and buur_buiten(B,y,x):
            a[y,x]=2 if (u[y,x]<-0.15 and v[y,x]<0.25) else 1
# 3. kenmerken uit r4 binnen het lijf: zwarte lijn onder de ring en de lijn aan de voet van de rechterhoorn
for (x0,y0,x1,y1) in ((25,30,40,30),(39,30,45,33)):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if E[y,x] and r4[y,x] in (1,2) and not buur_buiten(B,y,x): a[y,x]=r4[y,x]
# ogen (gat, groen) + lichte lip, en de neus uit r4
for (x0,y0,x1,y1,lip) in ((18,34,22,39,40),(28,35,34,41,42)):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if r4[y,x] in (1,6,7,8): a[y,x]=r4[y,x]
    for x in range(x0,x1+1):
        if r4[lip,x]==5: a[lip,x]=5
for y in range(41,47):
    for x in range(20,28):
        if r4[y,x] in (1,2) or (21<=x<=26 and y<=45): a[y,x]=r4[y,x]
# 4. rechterhand en rechtervoet uit r4
a[HR]=r4[HR]; a[VR]=r4[VR]
# 5. linkervoet
for (x,y),c in VLpix.items(): a[y,x]=c
# 6. linkerhand (want): eigen bolschaduw, buitenlijn selout boven/links, zwart onder; binnenrand tegen het lijf zwart
hu=(px-HX)/HRX; hv=(py-HY)/HRY; hw=np.sqrt(np.clip(1-hu*hu-hv*hv,0,1)); HI=hu*Ld[0]+hv*Ld[1]+hw*Ld[2]
for y in range(40,53):
    for x in range(9,18):
        if not HL[y,x]: continue
        nb=[(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if any(not HL[q] and not B[q] for q in nb): a[y,x]=2 if (hv[y,x]<0.0 and hu[y,x]<0.3) else 1
        elif any(not HL[q] for q in nb): a[y,x]=1
        else: a[y,x]=5 if HI[y,x]>=T2+0.05 else (4 if HI[y,x]>=T1+0.1 else 3)
# 7. mond: D met ronde boog (model x19-29, y47-52,7), hoeken 1 px omhoog
M=["?##???????##?",   # y47 x18-30
   "?#a#######a#?",
   "?#aaaaaaaaa#?",
   "??#aaaaaaa#??",
   "???#aaaaa#???",
   "????#####????",
   "????ddddd????"]   # lip y53
for j,r in enumerate(M):
    for i,ch in enumerate(r):
        if ch!='?': a[47+j,18+i]=L[ch]
# mondgebied buiten de D: vulling volgens de bolschaduw (oude r4-lijnen weg)
for y in range(47,54):
    for x in range(17,31):
        if M[y-47][x-18] if 0<=x-18<13 else None: pass
for y in range(47,54):
    for x in range(18,31):
        if M[y-47][x-18]=='?' and E[y,x] and a[y,x] in (1,2) and not buur_buiten(B,y,x): a[y,x]=5 if (D&Es)[y,x] else (4 if Es[y,x] else 3)
a[~(B|HL|HR|VR|VL)]=0
# naad tussen want en lijf dicht (open inkeping onder de hand)
for y in range(40,56):
    for x in range(10,20):
        if a[y,x]==0 and a[y,x-1]>0 and a[y,x+1]>0 and a[y-1,x]>0: a[y,x]=1
# kleine vlakjes (check.py): want licht linksboven 3 px, schaduw rechtsonder aaneen; ooglip doorlopend; voet
for (x,y,ch) in ((13,44,'d'),(14,47,'b'),(23,40,'d'),(19,58,'c')): a[y,x]=L[ch]
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(OUT,transparency=0); np.save(OUT+'.npy',a)
for n,t in ((3,'b'),(4,'c'),(5,'d')): print(t,(a==n).sum(),end='  ')
print('afwijking t.o.v. r4',int((a!=r4).sum()),'silhouet',int(((a>0)!=(r4>0)).sum()),'kleuren',len(set(a.ravel()))-1)
