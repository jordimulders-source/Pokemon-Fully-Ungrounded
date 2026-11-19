# Technische opschoning van kaal.npy (geen tekenwerk), elke wijziging gelogd per stap:
# a) roze naar 3 tinten: L -> l (Coordinator r2: roze <= 3 tinten + selout)
# b) wit (w) -> creme c (wit is alleen nog oogglans; in het vel las wit in de kop als gat)
# c) ontkorrelen binnen een kleurgroep (vulpixel zonder gelijke 4-buur -> meest voorkomende groepstint in de 8-buurt), 2x
# d) oogzwart E buiten de ogen -> #
# e) buitenlijn 1 px: randpixel zonder lijnkleur -> selout (d roze/paars/geel, b creme) als de lege buur boven/links ligt, anders # (creme: b)
import numpy as np, json
from txt import CH, dump
I={c:i for i,c in enumerate(CH)}
a=np.load('kaal.npy').copy(); H,W=a.shape; LOG=[]
def setp(y,x,v,step):
    if a[y,x]!=I[v]: LOG.append((step,int(y),int(x),CH[a[y,x]],v)); a[y,x]=I[v]
for y,x in zip(*np.where(a==I['L'])): setp(y,x,'l','a L->l')
for y,x in zip(*np.where(a==I['w'])): setp(y,x,'c','b w->c')
G={}
for c in 'sml': G[I[c]]='roze'
for c in 'Mp': G[I[c]]='paars'
for c in 'Yt': G[I[c]]='geel'
for c in 'ckb': G[I[c]]='creme'
for _ in range(2):
    b=a.copy(); ch=[]
    for y in range(H):
        for x in range(W):
            v=a[y,x]
            if v not in G or CH[v]=='b': continue
            four=[a[yy,xx] for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=yy<H and 0<=xx<W]
            if v in four: continue
            cnt={}
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if (dy or dx) and 0<=yy<H and 0<=xx<W and G.get(a[yy,xx])==G[v] and a[yy,xx]!=v and CH[a[yy,xx]]!='b':
                        cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
            if cnt: ch.append((y,x,CH[max(cnt,key=cnt.get)]))
    for y,x,v in ch: setp(y,x,v,'c korrel')
EYES=set()
for y,x in zip(*np.where(a==I['E'])):
    if (y,x) not in EYES: setp(y,x,'#','d E->#')
np.save('schoon0.npy',a); json.dump(LOG,open('log_clean.json','w'))
from collections import Counter; print(Counter(s for s,*_ in LOG)); dump(a)
