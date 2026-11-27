# Uku Pacha r3: kronkels per BAND schaduwen (vervangt blokken.py uit r2, dat een mozaïek gaf).
# Het model heeft geen gesloten spiraalcontouren die banden afsluiten; de band leest door zijn toon.
# Daarom: op het natieve modelraster de helderheid van de vlakcellen (geen lijncellen) per toongroep
# (lichte buikband = modelklassen 13-15, donkere lijfbanden = 5-12) gladstrijken (gauss, sigma S
# natieve cellen, genormaliseerd binnen de groep), zodat losse schubblokjes opgaan in het licht-donker
# van de band. Per spritepixel: overheersende groep in de voetafdruk -> die ladder, toon = gemiddelde
# gladde helderheid. Lijnpixels (K, n) blijven precies staan (niets weggehaald).
import numpy as np, geom, sys
cls=np.load('cls.npy'); GH=np.load('GH.npy'); P=np.load('PALmed.npy')
R=[list(l.rstrip('\n')) for l in open('raster.txt')][:64]
S=float(sys.argv[1]) if len(sys.argv)>1 else 2.0
Y0=int(sys.argv[2]) if len(sys.argv)>2 else 41
LUM=np.full(19,np.nan)
for k in range(5,16): LUM[k]=P[k].mean()
xs=np.arange(100)[None,:]; ys=np.arange(100)[:,None]
GHN=np.isin(cls,[13,14,15])&(xs>=72)
fill=(cls>=5)&(cls<=15)&~GHN
lum=np.where(fill,LUM[np.clip(cls,0,18)],0.0)
grp={'licht':fill&(cls>=13),'donker':fill&(cls<=12)}
def gauss(img,m,s):
    r=int(np.ceil(3*s)); k=np.exp(-(np.arange(-r,r+1)**2)/(2*s*s))
    def conv(a):
        a=np.pad(a,r); a=np.apply_along_axis(lambda v:np.convolve(v,k,'valid'),0,a)
        return np.apply_along_axis(lambda v:np.convolve(v,k,'valid'),1,a)
    num=conv(img*m); den=conv(m.astype(float)); return num/np.maximum(den,1e-6), den
glad={g:gauss(lum,m,S) for g,m in grp.items()}
DONKER=[('d',(LUM[5]+LUM[6])/2),('s',(LUM[8]+LUM[9])/2),('m',LUM[11]),('b',LUM[12])]
LICHT=[('b',LUM[12]),('l',LUM[13]),('p',LUM[14]),('w',LUM[15])]
def ins(x,y): return 0<=x<64 and 0<=y<64 and R[y][x]!='.'
def rand(x,y): return any(not ins(x+a,y+b) for a,b in ((0,1),(0,-1),(1,0),(-1,0)))
n=0
for y in range(Y0,64):
  for x in range(64):
    if not ins(x,y) or GH[y,x] or R[y][x] in 'KnDBhYPW' or rand(x,y): continue
    x0,x1,y0,y1=geom.s2n(x,y); acc={'licht':0,'donker':0}; val={'licht':0,'donker':0}
    for cy in range(int(y0),int(np.ceil(y1))):
      for cx in range(int(x0),int(np.ceil(x1))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
        if a<=0: continue
        for g in acc:
            if grp[g][cy,cx]: acc[g]+=a
            val[g]+=a*glad[g][0][cy,cx]
    tot=(x1-x0)*(y1-y0)
    g=max(acc,key=acc.get) if max(acc.values())>0 else ('licht' if R[y][x] in 'lpw' else 'donker')
    v=val[g]/tot
    lad=LICHT if g=='licht' else DONKER
    R[y][x]=min(lad,key=lambda t:abs(t[1]-v))[0]; n+=1
print('kronkelpixels opnieuw getoond:',n)
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
# Lijngewicht naar het model: in het model zijn de spiraal-/omlijningslijnen zwart (klasse 0) en de
# schubsegmentlijnen dun navy. Een lijnpixel met >= 25% zwarte of bijna-zwarte (klasse 0-1) modelcellen in zijn voetafdruk = K
# (spiraal); de rest = segmentlijn: in een donkere band een tint donkerder dan het vlak eromheen
# (d op s/m/b, anders n), zodat ze de toonopbouw van de band niet opdelen. Geen lijn verdwijnt.
DR=set('smb'); LI=set('lpw')
R2=[r[:] for r in R]; nk=ns=0
for y in range(Y0,64):
  for x in range(64):
    if R[y][x] not in 'Kn' or GH[y,x] or rand(x,y): continue
    x0,x1,y0,y1=geom.s2n(x,y); z0=0
    for cy in range(int(y0),int(np.ceil(y1))):
      for cx in range(int(x0),int(np.ceil(x1))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
        if a>0 and cls[cy,cx] in (0,1): z0+=a
    if R[y][x]=='K': nk+=1; continue
    nb=[R[y+b][x+a] for a in (-1,0,1) for b in (-1,0,1) if (a or b) and ins(x+a,y+b) and R[y+b][x+a] not in 'KnD.']
    if nb and all(c in DR for c in nb): R2[y][x]='d'; ns+=1
    elif any(c in LI for c in nb): R2[y][x]='n'
    else: R2[y][x]='n'
R=R2
print('spiraal K:',nk,'segment -> d:',ns)
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
