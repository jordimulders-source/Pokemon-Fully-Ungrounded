# r15: ijzer van koeienvanger en kop opnieuw uit het model (ijskomeet-methode r15/r21):
#  lijnpixels = lijnregel van r14 (onderlaag.py: >=50% modelpixels lum<70 in de voetafdruk -> lijn), losse lijnpunten zonder lijnbuur vallen weg;
#  vulling = gaussgemiddelde van het model (alleen ijzerpixels) per voetafdruk; tint (roest/grijs) uit een grof gemiddelde, licht/donker uit een fijn gemiddelde;
#  kop-bruin: 7 alleen bij modelglans, 9 waar het model donkerder bruin is (grof gemiddelde over alleen bruin), anders 8.
#  1-px-eilandje in de vulling -> opnieuw berekenen met een groter gemiddelde (geen clusterregel, geen buurkleur overnemen).
# Bevroren (diff 0, zie bewijs onderaan): al het groen, gezichtslijnen (zwart binnen 2 px van groen in de kop), kleine geest/wolken (groen),
# schoorsteen incl. rand (rij <=19), buitenrand van kop en koeienvanger, al het overige (lijf, wielen) = r14.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r15')
from basis import *
import kopzone as K
D=O.D
im=Image.open(D+'sprite_r14/sprite.png'); r=np.array(im); P=np.array(im.getpalette()[:48]).reshape(16,3).astype(float)
GR={2,3,4,5,6,13}
T1K=float(sys.argv[1]) if len(sys.argv)>1 else 112
LICHT=float(sys.argv[2]) if len(sys.argv)>2 else 121
lum=lambda c:0.3*c[0]+0.59*c[1]+0.11*c[2]
def buiten(a,y,x): return x==0 or any(a[y+dy,x+dx]==0 for dy,dx in((0,1),(1,0),(0,-1),(-1,0)))
# ---- zones
kz=np.zeros((64,64),bool)
for y in range(45,59):
    for x in range(0,27):
        if r[y,x]!=0 and r[y,x] not in GR and not buiten(r,y,x): kz[y,x]=True
hz=K.zone.copy()
Lk,_=lijnregel(-1); Lh=K.L
# ---- velden
G16,G08,G12,G25=glad(1.6),glad(0.8),glad(1.2),glad(2.5); GB=glad(2.0,BRUIN); GB25=glad(2.5,BRUIN)
def kaakkleur(x,y,gh,gl):
    ch=vul(x,y,gh,-1); cl=vul(x,y,gl,-1)
    if ch is None: return None
    if ch[0]-ch[2]>45: return 8 if lum(cl)>95 else 9
    l=lum(cl); return 10 if l>T1K else (11 if l>84 else 12)
def kopkleur(x,y,gh,gl,gb):
    ch=vul(x,y,gh,0); cl=vul(x,y,gl,0)
    if ch is None: return None
    if ch[0]-ch[2]>45:
        cb=vul(x,y,gb,0,BRUIN); lb=lum(cb) if cb is not None else 999
        return 7 if (lum(cl)>140 or lb>LICHT) else (9 if lb<104 else 8)
    return [7,10,11,12][int(np.argmin(((P[[7,10,11,12]]-cl)**2).sum(1)))]   # grijze platen: dichtstbijzijnde paletkleur (model-plaat is roze-lichtgrijs)
a=r.copy(); lijn=np.zeros((64,64),bool)
for zone,L,f,args in ((kz,Lk,kaakkleur,(G16,G08)),(hz,Lh,kopkleur,(G12,G08,GB))):
    for y,x in zip(*np.where(zone)):
        if L[y,x]:
            lijn[y,x]=True
            if zone is hz: a[y,x]=1      # kop: lijn = zwart; koeienvanger: r14-lijnpixel blijft (zwart/donker uit de lijnregel)
            continue
        c=f(x,y,*args)
        if c is not None: a[y,x]=c
# Toets r15 naast r14 (1x/2x/16x): kop rechtsonder (x>=22, y>=38) werd een dambord van zwart/rust/donkergrijs -> terug naar r14 (daar schoon).
terug=hz&(np.arange(64)[None,:]>=22)&(np.arange(64)[:,None]>=38)
a[terug]=r[terug]; hz=hz&~terug; lijn&=~terug
# lijn boven de donkere band (rij 22-23) werd 2 px dik waar hij een trede maakt: rij 23 x20-22 terug naar r14 (donkergrijs)
for x in (20,21,22): a[23,x]=r[23,x]; lijn[23,x]=False; hz[23,x]=False
zone=kz|hz
# losse lijnpunten (geen enkele zwarte buur) vallen weg
los=0
for y,x in zip(*np.where(zone&lijn)):
    nb=a[y-1:y+2,x-1:x+2]
    if (nb==1).sum()<=1 and a[y,x]==1:
        lijn[y,x]=False; los+=1
        a[y,x]=(kaakkleur(x,y,G16,G08) if kz[y,x] else kopkleur(x,y,G12,G08,GB)) or a[y,x]
# 1-px-eilandjes in de vulling: groter gemiddelde
def eiland(a,y,x): return (a[y-1:y+2,x-1:x+2]==a[y,x]).sum()==1
ei1=ei2=0
for y,x in zip(*np.where(zone&~lijn)):
    if eiland(a,y,x):
        ei1+=1
        c=kaakkleur(x,y,G25,G25) if kz[y,x] else kopkleur(x,y,G25,G25,GB25)
        if c is not None: a[y,x]=c
for y,x in zip(*np.where(zone&~lijn)):
    if eiland(a,y,x): ei2+=1
print('zone koeienvanger',kz.sum(),'kop',hz.sum(),'| losse lijnpunten weg',los,'| 1-px-eilandjes',ei1,'-> na groter gemiddelde',ei2)
# ---- bewijs bevroren
groen=np.isin(r,list(GR))|np.isin(a,list(GR))
print('groen diff',int((a[groen]!=r[groen]).sum()))
print('gezichtslijnen diff',int((a[K.gezicht]!=r[K.gezicht]).sum()),'(',int(K.gezicht.sum()),'px)')
print('rij<=19 (schoorsteen, rand, geest, wolken) diff',int((a[:20]!=r[:20]).sum()))
print('buiten de twee zones diff',int((a[~zone]!=r[~zone]).sum()))
print('gewijzigd in koeienvanger',int((a[kz]!=r[kz]).sum()),'/',int(kz.sum()),' kop',int((a[hz]!=r[hz]).sum()),'/',int(hz.sum()))
print('kleuren gebruikt',sorted(set(np.unique(a))))
np.save(D+'sprite_r15/sprite.npy',a)
o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(im.getpalette()); o.save(D+'sprite_r15/sprite.png',transparency=0)
with open(D+'sprite_r15/raster.txt','w') as f:
    for row in a: f.write(''.join('.' if q==0 else '%X'%q for q in row)+'\n')
