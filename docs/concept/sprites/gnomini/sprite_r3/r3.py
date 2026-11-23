# r3.py: vanaf r2 -> gnomini_A.png (grens roze/blauw als gebogen ring) en gnomini_B.png (A + 1 px streep op de grens).
# Beide: armpje links als rond balletje (Jordi: "zijn linkerhand is niet rond"). Bewijst diff 0 buiten lijf-vlak en arm L.
import sys, os, numpy as np; from PIL import Image
os.chdir('../sprite_r1'); sys.path.insert(0,'.'); from gemeen import opslaan; os.chdir('../sprite_r3')
o=np.asarray(Image.open('r2.png')).astype(int); n=o.copy()
z=np.load('../sprite_r1/zone_A.npy'); L=np.load('../sprite_r1/lijn_A.npy')
ROZE=[6,7,8,9]; BLAUW=[10,11,12,13]
vlak=(z==3)&~L&np.isin(o,ROZE+BLAUW)
oud_b={x:min([y for y in range(30,60) if vlak[y,x] and o[y,x] in BLAUW],default=None) for x in range(21,43)}
# ring: eerste blauwe rij b(x) = C + A*(1-u^2), u=(x-XM)/HW; zijkanten omhoog, midden zakt door
XM,HW,A=31.5,11.0,3.4
def b(x): u=(x-XM)/HW; return int(round(44.0+A*(1-u*u)))
gem_oud=np.mean([v for v in oud_b.values() if v is not None]); gem_new=np.mean([b(x) for x in oud_b if oud_b[x] is not None])
print('gemiddelde eerste blauwe rij oud %.2f nieuw %.2f'%(gem_oud,gem_new)); print('b(x):',[(x,b(x)) for x in range(21,43)])
# familie volgt de nieuwe grens, toonklasse (donker/schaduw/midden/licht) blijft van r2 (sikkels en lenzen houden hun plek)
for y,x in zip(*np.where(vlak)):
    t=(ROZE+BLAUW).index(o[y,x])%4
    n[y,x]=(BLAUW if y>=b(x) else ROZE)[t]
# toon aanpassen aan de nieuwe grens: hooglichtlens blauw (z) op de bolling linksboven van het blauwe vlak, roze lens blijft
for y,x in zip(*np.where(vlak)):
    if n[y,x]==13: n[y,x]=12
for x,y in [(23,48),(24,48),(25,48),(26,48),(22,49),(23,49),(24,49),(25,49),(26,49),(27,49),(23,50),(24,50),(25,50),(26,50)]:
    if vlak[y,x] and n[y,x] in BLAUW: n[y,x]=13
# roze dat nu boven de ring ligt en in r2 blauw-midden was links: midden (r) - komt al uit de toonklasse
# roze sikkel rechts 3 px breed (afstand tot de rechterrand van het lijfvlak), ook waar nu roze ligt dat in r2 blauw was
for y in range(41,47):
    for x in range(30,43):
        if vlak[y,x] and n[y,x] in ROZE and y>40:
            r=x
            while vlak[y,r+1]: r+=1
            if r-x<3: n[y,x]=7
            elif n[y,x]==7: n[y,x]=8
for y,x in zip(*np.where(vlak)):
    if n[y,x]==9 and not (41<=y<=44 and 26<=x<=32): n[y,x]=8
A_img=n.copy()
# armpje links: rond balletje, zelfde plek/formaat (x15-20, y40-46), opbouw als armpje rechts (selout linksboven, D-hooglicht, B-schaduw, zwart onder)
ARM={40:{17:6,18:6,19:6},
     41:{16:6,17:9,18:9,19:8,20:6},
     42:{15:6,16:9,17:9,18:8,19:8,20:6},
     43:{15:6,16:8,17:8,18:8,19:8,20:6},
     44:{15:6,16:8,17:8,18:8,19:7,20:6},
     45:{15:1,16:7,17:7,18:7,19:7,20:1},
     46:{16:1,17:1,18:1,19:1,20:1}}
armzone=np.zeros((64,64),bool)
for y in range(40,47):
    for x in range(14,21):
        if z[y,x]==4 or (y in ARM and x in ARM[y]): armzone[y,x]=True
for y in range(40,47):
    for x in range(14,21):
        if armzone[y,x]: A_img[y,x]=ARM.get(y,{}).get(x,0)
# B: streep op de grens (1 px) = blauwe vlakpixels die boven of opzij aan roze grenzen
def streep(img,k):
    s=img.copy()
    for y,x in zip(*np.where(vlak)):
        if img[y,x] in BLAUW and any(img[y+dy,x+dx] in ROZE and vlak[y+dy,x+dx] for dy,dx in ((-1,0),(0,-1),(0,1))): s[y,x]=k
    return s
opslaan(A_img,'gnomini_A.png')
opslaan(streep(A_img,10),'gnomini_B.png')        # donkerblauwe binnenlijn (56,109,142)
opslaan(streep(A_img,6),'gnomini_B_proze.png')   # alternatief: p-roze (172,72,102)
for f in ('gnomini_A.png','gnomini_B.png','gnomini_B_proze.png'):
    q=np.asarray(Image.open(f)).astype(int); d=q!=o
    print(f,'diff buiten lijfvlak+arm L:',(d&~vlak&~armzone).sum(),'| lijfvlak:',(d&vlak).sum(),'| arm L:',(d&armzone).sum(),'| arm R:',(d&(z==5)).sum(),
          '| silhouet buiten arm L:',(((q>0)!=(o>0))&~armzone).sum())
