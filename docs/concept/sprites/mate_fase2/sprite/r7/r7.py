# r7 = r6 zacht; rechterbuitenlijn loopt verder omlaag tot op de omlijning van het zeefje, zodat de romp (bombilla
# weggedacht) één gesloten vorm is: rand x56 rij 50-52, x55 rij 53, dan x54 rij 54 = bestaande omlijning zeefje;
# daarachter sluit de lijn achter het zeefje aan op de bodemlijn (x50, rij 58).
# Jordi: "zacht is beter, maar hij moet nog iets verder naar beneden om goed aan te sluiten, nu zou er een gat zitten
# als je de bombilla weg zou denken". Nieuwe rompppixels alleen op achtergrond naast het zeefje, tint = schaduwband (B,
# index 3, zoals de rand erboven); omlijning zwart (schaduwkant). Bombilla/zeefje en alles daarbuiten bevroren.
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'
src=Image.open(D+'r6/mate2_zacht.png'); a=np.asarray(src).astype(int); s=a.copy()
NIEUW={51:56,52:56,53:55}          # rij: x van de nieuwe omlijning
log=[]
for y,nx in NIEUW.items():
    ox=max(x for x in range(44,64) if s[y,x]!=0)
    assert s[y,ox]==1
    for x in range(ox,nx):
        assert a[y,x] in (0,1), (y,x)   # alleen achtergrond of de oude omlijning
        log.append((x,y,int(s[y,x]),3)); s[y,x]=3
    log.append((nx,y,int(s[y,nx]),1)); s[y,nx]=1
ch=np.argwhere(s!=a)
assert all(52<=x<=56 and 51<=y<=53 for y,x in ch)
assert all(not(10<=a[y,x]<=12) for y,x in ch)
print('gewijzigd',len(log),log)
o=Image.fromarray(s.astype('uint8'),'P'); o.putpalette(src.getpalette()); o.save(D+'r7/mate2.png',transparency=0)
# hulpbeeld: bombilla + zeefje (zilver en de omlijning eromheen) weggemaskeerd (lichtroze), sluitlijn achter het
# zeefje (van rand x54 rij 54 naar bodem x50 rij 58) in rood
pal=np.array(src.getpalette()[:48]).reshape(16,3)
rgb=np.where(s[...,None]==0,np.array([235,240,235]),pal[s]).astype('uint8')
zil=(s>=10)&(s<=12); m=zil.copy()
for y,x in np.argwhere(s==1):
    if any(zil[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if 0<=y+dy<64 and 0<=x+dx<64) and x>=40 and y>=40: m[y,x]=True
m[:40]=False; m[:, :40]=False
for x in (48,49,50): m[58,x]=False     # bodemlijn romp (raakt het zeefje maar hoort bij de romp)
rgb[m]=(255,205,215)
for x,y in [(54,54),(53,55),(52,56),(51,57)]: rgb[y,x]=(220,30,30)
Image.fromarray(rgb).save(D+'r7/hulp_zonder_bombilla.png')
