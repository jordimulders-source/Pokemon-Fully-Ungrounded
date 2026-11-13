# r3/bouw3.py : r2/raster.txt (basis) + handwerk uit r3/patches.txt -> r3/raster.txt + r3/octi.png
# draaien vanuit sprite2/:  python3 r3/bouw3.py
# patch-formaat: '@ x y' + regels ('_' = r2 laten staan); '= x,y,c ...' losse pixels; '! y' + volledige rij als stukken ('3*26' = 26x kleur 3; samen 64 tekens)
# meldt de index-diff t.o.v. r2 per zone, bewijst diff 0 in de bevroren zones en meet het aandeel bijna-zwart (luma < 50).
import sys; sys.path.insert(0,'.')
import cfg,numpy as np
PAL=list(cfg.PAL)
PAL[1]=(32,12,18)      # contour schaduwkant / boring
PAL[2]=(126,18,34)     # r3: lijntint = echt donkerrood (luma 52; r2 was (72,16,30), luma 34)
PAL[3]=(130,38,56); PAL[4]=(176,58,76); PAL[5]=(206,86,98); PAL[6]=(234,136,136)   # vlaktinten ongewijzigd t.o.v. r2
PAL[7]=(142,70,84); PAL[8]=(204,136,140)   # mauve: in r3 niet meer gebruikt (lippen terug naar lijfrood)
cfg.PAL=PAL
# bevroren (index-diff 0): mantel+vin, rechteroog, linker kanontentakel (vorm) -- als lijst van rechthoeken (x0,y0,x1,y1 exclusief)
BEVROREN=[('mantel + vin',28,7,56,25),('mantel/kop boven kanon',25,25,43,34),('rechteroog',32,35,41,41),
          ('linker kanontentakel (arm)',10,26,17,40),('linker kanontentakel (arm onder)',12,40,17,43),('linker kanon (omtrek+boring)',3,25,10,33)]
LIP_L={(5,26),(6,26),(7,26),(8,26),(4,27),(5,27),(8,27),(9,27),(4,28),(8,28),(9,28),(4,29),(8,29),(9,29),(4,30),(8,30),(9,30),(5,31),(6,31),(7,31),(8,31)}
ZONES=[('rupsband rechts',33,50,64,64),('rupsband links',0,50,33,64),('mondkanon',18,41,33,50),('linkeroog',22,35,27,41),
       ('tentakel B + rand A',17,22,25,43),('lage tentakel C',0,43,18,50),('kanon rechts',43,25,52,33),('tentakel D',52,22,62,41),
       ('lage tentakel G',44,43,64,50),('onderlijf',26,40,46,50),('kanon links (lip)',3,25,11,33)]
def build():
    a=cfg.read('r2/raster.txt'); x=y=None; L=open('r3/patches.txt').read().split('\n'); i=0
    while i<len(L):
        l=L[i]; i+=1
        if l.startswith('#') or not l.strip(): continue
        if l.startswith('='):
            for t in l[1:].split():
                px,py,c=t.split(','); a[int(py),int(px)]=cfg.CH.index(c)
            continue
        if l.startswith('!'):
            y=int(l.split()[1]); r=''.join(t[0]*int(t[2:]) if t[1:2]=='*' else t for t in L[i].split()); i+=1; assert len(r)==64,(y,len(r))
            a[y]=[cfg.CH.index(c) for c in r]; continue
        if l.startswith('@'): _,x,y=l.split()[:3]; x=int(x); y=int(y); continue
        for k,ch in enumerate(l):
            if ch!='_': a[y,x+k]=cfg.CH.index(ch)
        y+=1
    return a
def luma(c): return .299*c[0]+.587*c[1]+.114*c[2]
if __name__=='__main__':
    a=build(); b=cfg.read('r2/raster.txt')
    cfg.write(a,'r3/raster.txt'); cfg.topng(a,'r3/octi.png')
    n=(a>0).sum(); used=sorted(set(a.ravel())-{0})
    print('px',n,'bbox x',np.where(a.any(0))[0][[0,-1]],'y',np.where(a.any(1))[0][[0,-1]],'kleuren',len(used),[cfg.CH[v] for v in used])
    dk=sum((a==i).sum() for i in used if luma(PAL[i])<50)
    print('bijna-zwart (luma<50) %.1f%%   index1 %.1f%%  index2 %.1f%%'%(100*dk/n,100*(a==1).sum()/n,100*(a==2).sum()/n))
    d=(a!=b); rest=d.copy()
    print('BEVROREN (moet 0 zijn):')
    for nm,x0,y0,x1,y1 in BEVROREN:
        m=d[y0:y1,x0:x1].copy()
        if 'kanon (' in nm:
            for (px,py) in LIP_L: m[py-y0,px-x0]=False
        print('  %-30s x%d-%d y%d-%d  diff %d'%(nm,x0,x1-1,y0,y1-1,m.sum()))
    print('DIFF per zone t.o.v. r2:')
    for nm,x0,y0,x1,y1 in ZONES:
        print('  %-22s %4d'%(nm,(d[y0:y1,x0:x1]&rest[y0:y1,x0:x1]).sum())); rest[y0:y1,x0:x1]=False
    ys,xs=np.where(rest)
    print('  buiten zones %d'%rest.sum(),sorted(zip(xs.tolist(),ys.tolist())),'| totaal',d.sum(),'silhouet',((a>0)!=(b>0)).sum())
