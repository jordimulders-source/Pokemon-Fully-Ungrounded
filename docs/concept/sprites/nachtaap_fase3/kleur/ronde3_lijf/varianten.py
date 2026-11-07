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
