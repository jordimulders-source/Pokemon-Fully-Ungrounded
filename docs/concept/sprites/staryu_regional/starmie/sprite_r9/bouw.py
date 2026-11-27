# bouw.py r9: python3 sprite_r9/bouw.py   (vanuit starmie/)
# Eindkeuring Dragonfly Cave op r8_A (r7 + bovenste voorpunt 1 rij langer). Alleen uitvoering, niets getekend.
# Silhouet bevroren (alpha-diff 0, assert); elke wijziging (x, y, oude index, nieuwe index, reden), oude index ge-assert.
import numpy as np; from PIL import Image
IN='sprite_r8/starmie_r8_A.png'; OUT='sprite_r9/starmie_r9.png'
im=Image.open(IN); o=np.array(im).copy(); o0=o.copy(); pal=im.getpalette()
# (a) de glansstreep (6) die binnen de linker buitenlijn van de bovenarm loopt ((27,9) (26,11) (25,13) ... (19,20))
#     stopte op rij 9; ze loopt nu door tot rij 7 van de bovenpunt, op de twee lichtste koekpixels van de tip
#     (modelhelderheid D: (28,8) 188, (28,7) 181; glans-mediaan 188, 5-mediaan 166). Rij 4-6 van de tip blijven 5/4 (D <= 178).
W=[(28,8,5,6,'a glansstreep tot in de tip, D188'),(28,7,5,6,'a glansstreep tot in de tip, D181')]
for x,y,a,b,r in W:
    assert o0[y,x]==a,(x,y,o0[y,x],a,r); o[y,x]=b
assert ((o>0)==(o0>0)).all(),'silhouet veranderd'
assert (o!=o0).sum()==len(W)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(OUT,transparency=0)
print('gewijzigd',len(W))
