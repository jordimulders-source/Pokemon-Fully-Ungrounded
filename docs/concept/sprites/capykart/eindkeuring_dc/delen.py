# Onderdelenkaart Capykart eindkeuring_dc: elk spritepixel -> onderdeel (alleen indelen, geen vorm veranderen).
# Bron: eindkeuring_r17/capykart.png (silhouet + lijnen) ; grenzen kop/nek/rand gemeten op de modelhelderheid.
import numpy as np; from PIL import Image
from scipy import ndimage as nd
SRC='eindkeuring_r17/capykart.png'
# r17-indices: 0 tr,1 K,2-5 bruin (lijn,schaduw,licht,hoog),6/7 hoepel licht/donker,8 geel,9/10 rood l/d,11/12 blauw l/d,13/14 groen l/d,15 wit
_o=np.array(Image.open(SRC))
BESCHERMD=set()   # alleen lijn-/grijs-/witpixels van oog+wenkbrauw, tanden, morrillo, neusgaten, mond
for x in range(28,34):
    for y in range(16,23):
        if _o[y,x] in (1,2): BESCHERMD.add((x,y))      # oog + wenkbrauw
for x in range(16,25):
    for y in range(31,36):
        if _o[y,x] in (1,6,7,15): BESCHERMD.add((x,y))  # tanden + tandenkader
for p in [(16,23),(20,23),(18,29),(20,30)]: BESCHERMD.add(p)   # neusgaten, mond (model)
for p in [(22,16),(23,16),(24,16),(21,17),(22,17),(23,17)]: BESCHERMD.add(p)   # morrillo
def kopgrens(y):   # rechts hiervan = nek (rij 24-30), gemeten op de donkere wangboog in het model
    return {24:38,25:37,26:36,27:35,28:34,29:33,30:32}.get(y,99)
def rand(x):       # bovenrand van de bak (zwarte randlijn), voor de nek -> bak-scheiding
    if 23<=x<=26: return 34
    if 27<=x<=30: return 35
    if 31<=x<=32: return 36
    if x==33: return 37
    if 34<=x<=37: return 41
    if 38<=x<=40: return 40
    if 41<=x<=43: return 39
    if 44<=x<=47: return 38
    return -1
NAMEN=['-','kop','nek','kap','midden','achter','wiel_v','wiel_a','wiel_ver','hoepel','geel','rood','blauw','dak','gezicht']
def delen():
    o=np.array(Image.open(SRC)); d=np.zeros(o.shape,int)
    bruin=np.isin(o,[2,3,4,5]); hoe=np.isin(o,[6,7])
    for y in range(64):
        for x in range(64):
            k=o[y,x]
            if k in (0,1): continue
            if k in (13,14): d[y,x]=13
            elif k==8 or (44<=x<=56 and 11<=y<=17 and k in (2,4,5,3)): d[y,x]=10
            elif k in (9,10) or (k==2 and 44<=x<=55 and 17<=y<=18): d[y,x]=11
            elif k in (11,12): d[y,x]=12
            elif hoe[y,x] and not (x,y) in BESCHERMD: d[y,x]=9
    # bruin: kop / nek / auto
    for y in range(64):
        for x in range(64):
            if not bruin[y,x] or d[y,x]: continue
            if y<=23 or (y<=30 and x<=kopgrens(y)): d[y,x]=1
            elif 23<=x<=47 and y<rand(x) and x>=24: d[y,x]=2
            elif y<=33 and x<24: d[y,x]=1
    for p in BESCHERMD:
        x,y=p
        d[y,x]=14
    # rest bruin = auto: componenten
    rest=bruin&(d==0)
    lab,n=nd.label(rest)
    for i in range(1,n+1):
        m=lab==i; ys,xs=np.where(m); cx,cy=xs.mean(),ys.mean(); sz=m.sum()
        if sz<4:
            d[m]=-1; continue
        if cx>=49 and cy<45 : d[m]=5
        elif cx>=48: d[m]=7
        elif 22<=cx<=37 and cy>=48: d[m]=6
        elif cx<16 and cy>=55: d[m]=8
        elif cx>=33:
            d[m]=4
            mm=m.copy(); mm[42:,:]=False; mm[:,34:]=False; d[mm]=3   # stuk kap achter de voorste hoepel (x<=33, y<=41)
        else: d[m]=3
    for p in [(17,34),(16,35),(17,35)]: d[p[1],p[0]]=1   # kin links van de tanden
    # losse stukjes: meest voorkomende buurdeel
    for y,x in zip(*np.where(d==-1)):
        c=[d[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<64 and 0<=xx<64 and d[yy,xx]>0]
        c=[v for v in c if v in (1,2,3,4,5,6,7,8)]
        d[y,x]=max(set(c),key=c.count) if c else 5
    return o,d
if __name__=='__main__':
    o,d=delen()
    ch='.knKmAvwWhYRBDg'
    print('   '+''.join(str(x%10) for x in range(64)))
    for y in range(64): print('%2d '%y+''.join('#' if o[y,x]==1 else ch[d[y,x]] for x in range(64)))
