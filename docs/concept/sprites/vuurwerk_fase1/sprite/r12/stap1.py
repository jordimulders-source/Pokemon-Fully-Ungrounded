# Stap 1: handen. Basis r11; alleen pixels in de handenzone, elk op een meting uit het model (meet.py: lijn = lum<75-dekking, beige = huls, lum huid).
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'../r10')
from txt import CH; from meet import meet
import numpy as np; from PIL import Image
B=Image.open('../r11/sprite.png'); a=np.array(B); I={c:i for i,c in enumerate(CH)}
P=[ # (rij,kol,nieuw, reden)
 # linkerhand: r11 volgt de modellijnen al ((16,22)(16,23) 44/42 %, (18,23) 44 %, (19,22) 62 %, (20,20-23)); alleen de vingertop over de huls ontbrak
 (17,24,'l','vingertop 1 over de huls: model huid-lum 207 (lichtste huid van de hand), beige maar 40 %; vinger 1 = (17,22)-(17,24) onder lijn (16,22)-(16,23)'),
 # rechterhand: vingerlijn loopt recht omlaag langs kol 29 (16-18), vinger 1 wijst schuin links-omlaag over de huls
 (18,29,'d','vingerlijn: model lijn 35 %, verlengt (16,29)-(17,29)'),
 (20,28,'d','onderlijn vinger 1: model lijn 54 %'),
]
LOG=[]
for r,c,v,why in P:
    ln,be,e,L=meet(r,c); LOG.append('(%d,%d) %s->%s  lijn %d%% beige %d%% lum %d  %s'%(r,c,CH[a[r,c]],v,100*ln,100*be,L,why)); a[r,c]=I[v]
out=sys.argv[1] if len(sys.argv)>1 else 'stap1.png'
im=Image.fromarray(a,'P'); im.putpalette(B.getpalette()); im.save(out,transparency=0)
print('\n'.join(LOG))
