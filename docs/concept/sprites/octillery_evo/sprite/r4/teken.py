# r4: bewerkt r3 (raster ../r3/raster.txt). Blokken: '~' = r3-pixel houden.
# Bevroren (alpha+kleur): bovenste kanon (x<=17), mondkanon en onderste kanon (x<=31,y>=43; x<=27,y>=56),
# behalve de openingen (punt 9).
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,D+'/..')
import pal,cfg,numpy as np
r3=cfg.read(D+'/../r3/raster.txt'); a=r3.copy()
def B(x0,y0,rows):
    for j,s in enumerate(rows):
        for i,ch in enumerate(s):
            if ch!='~': a[y0+j,x0+i]=cfg.CH.index(ch)
exec(open(D+'/blokken.py').read())
Y,X=np.mgrid[:64,:64]
FROZEN=(X<=17)|((X<=31)&(Y>=43))|((X<=27)&(Y>=56))
OPEN=np.zeros((64,64),bool)          # openingen kanonnen (punt 9) mogen veranderen
OPEN[39:43,1:6]=True; OPEN[51:61,7:15]=True
bad=FROZEN&~OPEN&(a!=r3)
if bad.any(): print('LET OP: bevroren pixels gewijzigd:',list(zip(*np.where(bad)))[:20])
a[FROZEN&~OPEN]=r3[FROZEN&~OPEN]
cfg.write(a,D+'/raster.txt'); cfg.topng(a,D+'/octi.png')
print('pixels veranderd t.o.v. r3:',(a!=r3).sum())
