# bouw.py rN : auto.txt (onderlaag, zie onder.py + auto.py) + handwerk uit rN/patches.txt -> rN/raster.txt + rN/octi.png
# patches.txt: blokken "@ x y" gevolgd door rasterregels; '_' = onderlaag laten staan
import cfg,sys,numpy as np
r=sys.argv[1]; a=cfg.read('auto.txt')
x=y=None
for l in open(r+'/patches.txt'):
    l=l.rstrip('\n')
    if l.startswith('#') or not l.strip(): continue
    if l.startswith('@'): _,x,y=l.split()[:3]; x=int(x); y=int(y); continue
    for i,ch in enumerate(l):
        if ch!='_': a[y,x+i]=cfg.CH.index(ch)
    y+=1
SPIRAAL=int(sys.argv[2]) if len(sys.argv)>2 else 2
a[a==14]=SPIRAAL   # 'e' = spiraallijn rupsbanden
cfg.write(a,r+'/raster.txt'); cfg.topng(a,r+'/octi.png')
n=(a>0).sum(); print('px',n,'kleuren',len(set(a.ravel()))-1,'zwart %.1f%%'%(100*(a==1).sum()/n),'donkerrood %.1f%%'%(100*(a==2).sum()/n))
