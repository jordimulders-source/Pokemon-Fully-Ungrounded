# kop.py: kop op natieve schaal (1 modelpixel = 1 spritepixel; kop ±21 breed = Mr. Mime-formaat).
# Gezicht (ogen = pupil + dunne lichtgrijze boog, snor, wang, kaak) = natief model 1-op-1 (banden -> palet).
# Goedgekeurde afwijkingen: kale ronde koepel i.p.v. de haarmop; nabije kuif = modelhaar rechts van de koepel;
# verre kuif = dezelfde vorm ongespiegeld naar links verschoven, alleen het deel boven/achter de koepel.
import numpy as np, sys; from PIL import Image
a=np.asarray(Image.open('../sprite_r10/natief.png').convert('L')).astype(float)
band=np.select([a<25,a<66,a<115,a<160,a<225],[1,2,3,4,5],6)
HAAR={1:1,2:2,3:3,4:4}
GEZ ={1:1,2:2,3:5,4:6,5:7,6:8}
CX,CY,R=51.6,19.8,9.6              # koepel (natief)
SHIFT=int(sys.argv[1]) if len(sys.argv)>1 else 13
# gezichtsgrenzen per rij (natief, uit het model: buitenlijn links, wang/kaak rechts)
L={15:43,16:43,17:43,18:42,19:42,20:42,21:42,22:41,23:41,24:41,25:41,26:42,27:42,28:43,29:44,30:46}
Rr={15:56,16:56,17:56,18:56,19:56,20:58,21:60,22:60,23:60,24:60,25:61,26:58,27:58,28:57,29:55,30:52}
H,W=34,80
kop=np.zeros((H,W),int); binnen=np.zeros((H,W),bool); kuif=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if (x-CX)**2+(y-CY)**2<=R*R: binnen[y,x]=1
        if y in L and L[y]<=x<=Rr[y]: binnen[y,x]=1
        if 5<=y<=20 and x>={11:62,12:60}.get(y,62 if y<11 else 57) and band[y,x]<=4: kuif[y,x]=1
# nabije kuif alleen het samenhangende deel rechts
# verre kuif: kuif-vorm SHIFT naar links, alleen boven/achter de koepel
for y,x in zip(*np.where(kuif)):
    if not binnen[y,x-SHIFT] and y<=12 and x-SHIFT>=45: kop[y,x-SHIFT]=HAAR[band[y,x]]
for y,x in zip(*np.where(binnen)):
    kop[y,x]=GEZ[band[y,x]] if (y>=15 and y in L and L[y]<=x<=Rr[y]) else 8
for y,x in zip(*np.where(kuif)): kop[y,x]=HAAR[band[y,x]]
# buitenlijn van koepel/gezicht: rand naar buiten (niet naar haar) = zwart
o=kop.copy()
for y,x in zip(*np.where(binnen&~kuif)):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        if not (binnen|kuif)[y+dy,x+dx]: o[y,x]=1
kop=o
np.save('kop_ruw.npy',kop)
for j in range(4,32): print('%2d '%j+''.join(str(v) if v else '.' for v in kop[j,25:76]))
