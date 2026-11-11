# r5: kleine reparatieronde op r4 (keuring r4/KEURING.md, punt 1-5). Palet ongewijzigd (pal.py = r4).
# Alleen pixels in de vijf zones veranderen; buiten de zones diff 0 (gecontroleerd onderaan).
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,D+'/..')
import pal,cfg,numpy as np
r4=cfg.read(D+'/../r4/raster.txt'); a=r4.copy()
C=lambda ch: cfg.CH.index(ch)
def P(zone,pts):
    for (x,y),ch in pts.items(): a[y,x]=C(ch); ZONE[y,x]=zone
ZONE=np.zeros((64,64),int)
# 1. roze schijven rechtsonder weg: tint 3, onderste rij tint 2 (binnenlijn (34,60)-(50,57) blijft)
P(1,{(41,60):'3',(42,60):'3',(43,60):'3',(41,61):'2',(42,61):'2',(43,61):'2',
     (46,59):'3',(47,59):'3',(48,59):'3',(46,60):'2',(47,60):'2',(48,60):'2'})
# 2. tentakel rechts midden: x56-62 taps tot 1 px, bovenrand y50, onderrand stijgt, punt omhoog op (62,49)
P(2,{(57,50):'2',(57,51):'4',
     (58,50):'2',(58,51):'4',(58,52):'3',
     (59,50):'2',(59,51):'3',(59,52):'1',(59,53):'.',
     (60,50):'2',(60,51):'1',(60,52):'.',(60,53):'.',
     (61,49):'2',(61,50):'1',(61,51):'.',(61,52):'.',(61,53):'.',
     (62,49):'1',(62,51):'.',(62,52):'.'})
# 3. onderrand mantel schuin: y38 x49-51, y37 x52-57, y36 x58-60
P(3,{(50,37):'3',(51,37):'3',(50,38):'1',(51,38):'1',
     (58,37):'.',(59,37):'.',(60,37):'.',(58,36):'1',(59,36):'1',(60,36):'1'})
# 4. F-kolom x=30 buigen (hol naar rechts), tint 2
P(4,{(30,58):'2',(30,59):'2',(30,60):'2',(30,61):'3',(30,62):'3',(31,61):'2',(31,62):'2'})
# 5. wratten op de lus: (31,57),(33,58),(35,58); (37,59) weg
P(5,{(31,57):'b',(33,58):'b',(35,58):'b',(37,59):'3'})
d=a!=r4
print('pixels veranderd t.o.v. r4:',d.sum())
for z in range(1,6): print(' zone %d: %d'%(z,(d&(ZONE==z)).sum()))
print(' buiten de zones:',(d&(ZONE==0)).sum())
assert (d&(ZONE==0)).sum()==0
cfg.write(a,D+'/raster.txt'); cfg.topng(a,D+'/octi.png')
