# Varianten: dij-bult onder het lijf (\"rare kont\") geleidelijk kleiner: onderrand k px omhoog.
from PIL import Image
w={36:1/3,37:2/3,38:1,39:1,40:1,41:1,42:1,43:1,44:1,45:2/3,46:1/3}
for k in (1,2,3,4):
    im=Image.open('nachtaap_fase3.png'); P=im.load()
    log=[]
    for x,f in w.items():
        bot=max(y for y in range(44,60) if P[x,y]!=0)
        r=int(k*f+0.5)
        nb=bot-r
        if r==0: continue
        for y in range(nb+1,bot+1): P[x,y]=0
        P[x,nb]=1
        if P[x,nb-1] in (3,4): P[x,nb-1]=2
        log.append('x%d %d->%d'%(x,bot,nb))
    im.save('varianten/dij_min%d.png'%k,transparency=0)
    print(k,'; '.join(log))
# -4 met de hand glad: onderrand per kolom (geen deuk bij x36-38, geen trap van 2 px bij x45-46)
bot4={34:48,35:49,36:49,37:49,38:49,39:50,40:50,41:50,42:50,43:50,44:51,45:51,46:52}
base=Image.open('nachtaap_fase3.png').load()
im=Image.open('nachtaap_fase3.png'); P=im.load()
for x,b in bot4.items():
    for y in range(44,60):
        if y>b: P[x,y]=0
        elif y==b: P[x,y]=1
        elif y==b-1: P[x,y]=2
        else: P[x,y]=base[x,y]
im.save('varianten/dij_min4.png',transparency=0)
