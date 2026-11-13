# r2/bouw2.py : r1/raster.txt (bevroren basis) + handwerk uit r2/patches.txt -> r2/raster.txt + r2/octi.png
# draaien vanuit sprite2/:  python3 r2/bouw2.py   (patch-formaat als ../bouw.py; '_' = r1 laten staan)
# meldt de pixeldiff t.o.v. r1 per zone (ZONES) en erbuiten.
import sys; sys.path.insert(0,'.')
import cfg,numpy as np
PAL=list(cfg.PAL)
PAL[2]=(72,16,30); PAL[3]=(130,38,56); PAL[4]=(176,58,76); PAL[5]=(206,86,98); PAL[6]=(234,136,136)
PAL[7]=(142,70,84); PAL[8]=(204,136,140)
cfg.PAL=PAL
ZONES=[('rupsband rechts',33,50,63,63),('rupsband links',0,50,33,63),('mondkanon',17,38,31,50),
       ('tentakels links',0,22,25,50),('ogen/kop',22,23,44,42),('mantel',28,7,58,23),('rechterkant',42,22,63,50),('onderlijf',25,42,44,50)]
def build():
    a=cfg.read('r1/raster.txt'); x=y=None
    for l in open('r2/patches.txt'):
        l=l.rstrip('\n')
        if l.startswith('#') or not l.strip(): continue
        if l.startswith('='):
            for t in l[1:].split():
                px,py,c=t.split(','); a[int(py),int(px)]=cfg.CH.index(c)
            continue
        if l.startswith('@'): _,x,y=l.split()[:3]; x=int(x); y=int(y); continue
        for i,ch in enumerate(l):
            if ch!='_': a[y,x+i]=cfg.CH.index(ch)
        y+=1
    return a
if __name__=='__main__':
    a=build(); b=cfg.read('r1/raster.txt')
    cfg.write(a,'r2/raster.txt'); cfg.topng(a,'r2/octi.png')
    n=(a>0).sum(); print('px',n,'kleuren',len(set(a.ravel()))-1,'zwart %.1f%%'%(100*(a==1).sum()/n),'donkerrood %.1f%%'%(100*(a==2).sum()/n))
    d=(a!=b); rest=d.copy()
    for nm,x0,y0,x1,y1 in ZONES:
        print('  diff %-16s %4d'%(nm,(d[y0:y1,x0:x1]&rest[y0:y1,x0:x1]).sum())); rest[y0:y1,x0:x1]=False
    print('  diff buiten zones %d'%rest.sum(), 'totaal',d.sum(), 'silhouet',((a>0)!=(b>0)).sum())
