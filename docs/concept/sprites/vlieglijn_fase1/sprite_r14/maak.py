# r14: maakt de 4 combinaties uit _stap3.png (punt 1 verschuiving, punt 3 onderrand, punt 4 zwart vak)
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
A_,B_,C_=10,11,12
# ringen: (rij van de brede witte rij, kolom bovenkabel, kolom onderkabel) na verschuiving
RINGEN=[(45,18,17),(44,23,23),(47,30,31),(47,34,35),(46,41,42)]
def ring(b,r,cu,cl,var):
    lo=min(cu,cl); hi=max(cu,cl)+1          # binnenkant van de unie
    if cu==cl: lo-=1; hi+=1                  # rechte kabel: ring 1 px breder aan elke kant (4 binnen)
    if var=='A':   # kraal: smal-breed-smal, afgeronde uiteinden
        b[cu-1,r-1]=1; b[cu,r-1]=A_; b[cu+1,r-1]=B_; b[cu+2,r-1]=1
        b[lo-1,r]=1; b[hi+1,r]=1
        for x in range(lo,hi+1): b[x,r]=B_
        b[lo+ (1 if hi-lo>=2 else 0),r]=A_ if hi-lo>=3 else B_
        b[hi,r]=C_
        b[cl-1,r+1]=1; b[cl,r+1]=C_; b[cl+1,r+1]=C_; b[cl+2,r+1]=1
    else:          # B: band binnen de kabel, onderbreekt de glans, geen uitstekende kapjes
        b[cu-1,r]=1; b[cu,r]=A_; b[cu+1,r]=B_; b[cu+2,r]=1
        b[cl-1,r+1]=1; b[cl,r+1]=C_; b[cl+1,r+1]=C_; b[cl+2,r+1]=1
OOG_R=[(18,29),(18,30),(17,31),(19,31),(16,32),(20,32),(16,33),(20,33)]
OOG_L=[(10,29),(10,30),(9,31),(11,31),(9,32),(12,32),(12,33)]
def led(b,var):
    if var=='L1':   # losse lampjes, 1 px ertussen
        aan={(18,29),(17,31),(19,31),(16,33),(20,33),(10,29),(9,31),(11,31),(12,33)}
        for p in OOG_R+OOG_L:
            if p not in aan: b[p]=2
    else:           # L2: doorlopende ^ + raster van uit-lampjes (index 3) achter de ^
        D=set(OOG_R+OOG_L)
        for y in range(28,35):
            for x in range(9,22):
                if b[x,y]==2 and x%2==0 and y%2==1:
                    if not any((x+dx,y+dy) in D for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
                        b[x,y]=3
def maak(ringv,ledv):
    im=Image.open('sprite_r14/_stap3.png'); b=im.load()
    weg=set()   # oude ringen (witte rij, blauwe rij, zwarte kapjes) eerst leegmaken
    for r,cu,cl in RINGEN:
        for y in (r,r+1):
            for x in range(min(cu,cl)-2,max(cu,cl)+4):
                if b[x,y] in (A_,C_) or (b[x,y]==1 and (b[x-1,y] in (A_,C_) or b[x+1,y] in (A_,C_))): weg.add((x,y))
    for p in weg: b[p]=0
    for r,cu,cl in RINGEN: ring(b,r,cu,cl,ringv)
    for (x,y) in weg:   # gewiste kapjes die ook lijfrand waren: rand dicht houden
        if b[x,y]==0 and any(b[x+dx,y+dy] in (2,3,4,5,6) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): b[x,y]=1
    led(b,ledv)
    return im
if __name__=='__main__':
    for rv in 'AB':
        for lv in ('L1','L2'):
            im=maak(rv,lv); n='sprite_r14/vlieg_r14_%s_%s'%(rv,lv)
            im.save(n+'.png',transparency=0)
            onbg(im).resize((512,512),Image.NEAREST).save(n+'_8x.png')
