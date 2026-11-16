# Ronde 2 opschonen + bevroren zones uit r1. Telt alles.
import numpy as np, pickle
o=np.load('kaal_r2.npy'); Z=np.load('zone.npy'); BLK=pickle.load(open('blk.pkl','rb'))
r1=np.load('../sprite_r1/post_B.npy'); log={}
P=['#292018','#b5f3b6','#72d779','#67b370','#467e4b','#3f6036','#9cf08d','#a0846a','#725641','#3d3827','#8c6246','#aba09a','#7b7c7e','#4a443c']
LUM=np.array([sum(np.array([int(c[i:i+2],16) for i in (1,3,5)])*[0.3,0.59,0.11]) for c in P])
GROUP={1:'O',2:'G',3:'G',4:'G',5:'G',6:'G',7:'N',8:'W',9:'W',10:'W',11:'W',12:'S',13:'S',14:'S'}
def mark(why,y,x,v):
    if o[y,x]!=v: o[y,x]=v; log[why]=log.get(why,0)+1
# A. buitenlijn
fg=o>0; p=np.pad(fg,1)
n4=p[:-2,1:-1].astype(int)+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:]
edge=fg&(n4<4)
for y,x in zip(*np.where(edge)):
    v=o[y,x]; G=GROUP.get(v,'O')
    if G=='G' and y>=23:          # staart/wolk: selout #467e4b, nooit zwart; dunne uitloper (<=1 buur) niet dichtmetselen
        if n4[y,x]<=1: mark('staart: uitlopertip selout',y,x,4 if LUM[v-1]>LUM[3] else v)
        else: mark('staart: rand selout',y,x,5)
    else:
        cc=BLK.get((y,x)); 
        if cc is None: continue
        cc=cc[[(GROUP[q]==G or q==1 or (G=='N' and GROUP[q]=='G')) for q in cc]]
        if len(cc): mark('rand: donkerste modelkleur',y,x,cc[np.argmin(LUM[cc-1])])
# B. losse tintpixels / losse lijnpixels (zoals r1)
for it in range(2):
    c=o.copy()
    for y in range(1,63):
        for x in range(1,63):
            v=c[y,x]
            if v in (0,1,7): continue
            nb=[c[y-1,x],c[y+1,x],c[y,x-1],c[y,x+1]]
            if len(set(nb))==1 and nb[0]!=v and nb[0] in GROUP and GROUP[nb[0]]==GROUP[v]: mark('losse tintpixel',y,x,nb[0])
for y in range(1,63):
    for x in range(1,63):
        if o[y,x]==1:
            nb=np.delete(o[y-1:y+2,x-1:x+2].ravel(),4)
            if (nb>0).all() and not np.isin(nb,[1,5,9,10,14]).any():
                u,uc=np.unique(nb,return_counts=True); mark('losse lijnpixel',y,x,u[uc.argmax()])
# B2. bouten: losse lichtgrijze pixel in het hout (buiten de wielen) -> donkere boutkleur van het model #4a443c
for y in range(1,63):
    for x in range(1,63):
        if o[y,x] in (12,13) and not ((39<=y<44 and x<5) or (40<=y<45 and 14<=x<19)):
            nb=np.delete(o[y-1:y+2,x-1:x+2].ravel(),4)
            if not np.isin(nb,[12,13]).any(): mark('bout: lichtgrijs -> #4a443c',y,x,14)
kaal_na=o.copy()
# C. bevroren uit r1: rijen 0-22 (gezicht, kop, armen, vuist) behalve de krul; geest achter de wagon; wielen
F=np.zeros((64,64),bool); F[0:23,:]=True; F[0:4,42:54]=False
for y in range(23,32):
    for x in range(24,45):
        if r1[y,x] in (2,3,4,5): F[y,x]=True
nf=0
for y,x in zip(*np.where(F)):
    if o[y,x]!=r1[y,x]: o[y,x]=r1[y,x]; nf+=1
print('bevroren pixels teruggezet uit r1:',nf,'(F-zone',F.sum(),')')
# C2. krul: donkere modellijn die als hout/staal is ingedeeld (#3d3827/#4a443c) is de spiraallijn (in het model donkergroen) -> #467e4b
for y in range(0,4):
    for x in range(42,54):
        if o[y,x] in (9,10,11,14): mark('krul: spiraallijn = donkergroen van het model (#2c3d23/#446f3f) -> #467e4b',y,x,5)
# D. wielen opnieuw uit het model (wiel.py-bemonstering, rand dicht): licht linksboven, donker rechtsonder, naaf rechts
T=['.OOO..','OgggO.','OGGGsO','OGGGsO','OsssO.','.OOO..']; cm={'O':1,'g':12,'G':13,'s':14}
for (wx,wy) in ((0,39),(14,39)):
    for dy,row in enumerate(T):
        for dx,ch in enumerate(row):
            if ch!='.': mark('wiel uit model',wy+dy,wx+dx,cm[ch])
# E. ashout tussen de wielen: middelpunt-bemonstering van de lichte balk uit het model (x6-13, rij 40-43)
cls=np.load('cls.npy'); s,X0,Y0,oy,XC,k=[float(v) for v in open('r1.meta').read().split()]
for y in range(40,44):
    for x in range(6,14):
        v=int(cls[int(Y0+(y-oy+0.5)/s), int(X0+(x+0.5)/s)])
        if v==11: v=9
        if v: mark('ashout uit model',y,x,v)
o[o==6]=5
np.save('post_r2.npy',o); np.save('frozen.npy',F); print(log)
