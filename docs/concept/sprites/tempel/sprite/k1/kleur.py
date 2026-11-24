# Kleurronde k1 tempel: handmatige tintwijzigingen binnen bestaande vlakken.
# Silhouet, vormen, ogen en deurgat bevroren (zie gereedschap.bewijs).
import sys
from gereedschap import *
a0,pal0=laad()
a=a0.copy()
PAL=[ (152,208,160),  # 0 transparant
      (24,22,20),     # 1 zwart: outline shadow
      (48,44,38),     # 2 donkere lijn (bevroren: oog)
      (222,214,186),  # 3 steen licht, warm
      (180,176,156),  # 4 steen basis (bevroren: oog)
      (150,144,136),  # 5 steen midden
      (120,114,114),  # 6 steen schaduw, koeler
      (82,78,68),     # 7 lijn lichtkant / donker (bevroren: oog)
      (160,182,98),   # 8 mos licht
      (110,138,70),   # 9 mos midden
      (255,216,112),  # 10 goud (bevroren)
      (232,152,48),   # 11 goud donker (bevroren)
      (36,32,30),     # 12 deur (bevroren)
      (66,90,54),     # 13 mos donker
      (66,60,72),     # 14 diepe schaduw, paarsig
      (92,86,94) ]   # 15 schaduw donker, koel
pal=[v for c in PAL for v in c]
def R(x0,y0,x1,y1,van,naar):
    if isinstance(van,int): van=[van]
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if a[y,x] in van: a[y,x]=naar
def P(naar,pts):
    for x,y in pts: a[y,x]=naar
def rij(y,x0,s):
    # s: tekenreeks vanaf x0; '.' of ' ' = ongemoeid, anders hexindex
    for i,c in enumerate(s):
        if c in '. ': continue
        a[y,x0+i]=int(c,16)
RAS=os.path.join(HIER,'raster.txt')
if os.path.exists(RAS) and '--basis' not in sys.argv:
    rows=open(RAS).read().split('\n')[:64]
    a=np.array([[0 if c=='.' else int(c,16) for c in r] for r in rows])
else:
    exec(open(os.path.join(HIER,'bewerkingen.py')).read())
if __name__=='__main__':
    uit=HIER
    bewaar(a,pal,os.path.join(uit,'tempel.png'))
    print(bewijs(a,pal,a0,pal0))
    vel(a,pal,a0,pal0,os.path.join(TEMPEL,'referenties','model.webp'),os.path.join(uit,'vel.png'))
    big=Image.open(os.path.join(uit,'tempel.png')).convert('RGBA').resize((512,512),Image.NEAREST)
    bg=Image.new('RGB',(512,512),(255,255,255)); bg.paste(big,(0,0),big); bg.save(os.path.join(uit,'tempel_8x.png'))
