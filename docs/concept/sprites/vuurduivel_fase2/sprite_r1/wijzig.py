# wijzig.py: handmatige reparaties op raster_auto.txt -> raster_r1.txt ; elke pixel met reden (alle naar het model)
R=[list(r.rstrip('\n')) for r in open('raster_auto.txt')]
E={}
def zet(x,y,c,reden): E[(x,y)]=(R[y][x],c,reden); R[y][x]=c
# --- oog: de losse-pixelregel at het rode oog op; terug naar de natieve modelcellen x27-29, y18-20
zet(27,18,'#','oog: bovenlid, model 18b zwart over x27-30')
zet(27,19,'r','oog: iris linksboven, model rozerood in de cel')
zet(28,19,'R','oog: pupil donkerrood, model #R/#m')
zet(29,19,'C','oog: lichte oogrand rechts, model cc/CC')
zet(27,20,'r','oog: iris onder, model CO/BR')
zet(28,20,'R','oog: pupil onder, model #m/Rr')
zet(29,20,'c','oog: onderrand, model CB/Rc (crème met donker)')
# --- hand: de zwart-regel (>=2 van 4) maakte de vingers zwart; met >=3 van 4 komt de bruine hand van het model terug
for (x,y,c) in [(5,29,'h'),(6,29,'B'),(5,30,'B'),(6,30,'h'),(7,30,'B'),(6,31,'h'),(7,31,'H'),(8,31,'B'),(9,31,'B'),(6,32,'H'),(7,32,'H'),(8,32,'B')]:
    zet(x,y,c,'hand: bruine vinger/handpalm, natieve cel (meerderheid zonder lijnpixels)')
# --- vonk boven de handvlam: werd zwart (randregel), model oranje + crème
zet(9,17,'O','vonk: model OO')
zet(9,18,'O','vonk: model .O/.m')
zet(10,18,'A','vonk: model c./C. (licht puntje, randtint)')
import os
if os.path.exists('wijzig_extra.py'): exec(open('wijzig_extra.py').read())
open('raster_r1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
with open('wijzigingen.txt','w') as f:
    for (x,y),(a,b,r) in sorted(E.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s->%s  %s\n'%(x,y,a,b,r))
print(len(E),'pixels met de hand')
