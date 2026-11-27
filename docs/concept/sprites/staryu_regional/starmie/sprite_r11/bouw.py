# bouw.py r11: python3 sprite_r11/bouw.py   (vanuit starmie/)
# Jordi over r10 (A): "hij moet nog smoother, de overgang bovenin is nog niet helemaal goed en rechts is de punt puntiger dan de rest".
# Alleen tinten binnen het bestaande silhouet (alpha-diff 0, ge-assert), diff 0 buiten de zonemaskers (ge-assert), palet ongewijzigd.
# A = starmie_r11.png, B = starmie_r11_B.png (alleen verschil: aansluiting bovenin zone 1 en tiplijn zone 2, zie NOTITIES).
import numpy as np; from PIL import Image
IN='sprite_r10/starmie_r10.png'
im=Image.open(IN); o0=np.array(im); pal=im.getpalette()
M=np.zeros((64,64),bool); M[10:21,36:47]=True; M[20:27,44:58]=True   # zelfde zones als r10
# zone 1, beide varianten: lichtband 5 met gelijkmatige diagonale rechtergrens (eind x43,42,41,40) en uitloper op rij 15
Z1={(40,14):(4,5),(38,15):(4,5)}
Z1A={(38,13):(2,5)}            # A: selout-trap bovenin 3-2-2-1 eindigt op (37,13) tegen de voorste-sterlijn
Z1B={(37,13):(2,5)}            # B: trap eindigt op (38,13), raakt de voorste-sterlijn diagonaal op (37,14)
# zone 2, beide varianten: lichte rand 2 rijen hoog tot in de tip, tipeinde 5/4/4 (spiegel linker arm 5/5/4), hoek selout
Z2={(51,23):(5,5),(53,23):(4,5),(54,23):(4,5),(55,22):(4,5),(55,23):(3,4),(55,24):(3,4),(55,21):(1,2)}
Z2B={(56,22):(1,2)}            # B: tipkolom 2/1/1 precies als de linker arm (4,22-24)
def bouw(*ws):
    o=o0.copy()
    for w in ws:
        for (x,y),(a,b) in w.items():
            assert M[y,x] and o0[y,x]==a,(x,y,o0[y,x],a); o[y,x]=b
    assert ((o>0)==(o0>0)).all(),'silhouet veranderd'
    assert (o[~M]==o0[~M]).all(),'diff buiten zones'
    return o
def save(o,p):
    q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(pal); q.save(p,transparency=0)
A=bouw(Z1,Z1A,Z2); B=bouw(Z1,Z1B,Z2,Z2B)
save(A,'sprite_r11/starmie_r11.png'); save(B,'sprite_r11/starmie_r11_B.png')
for n,o in (('A',A),('B',B)):
    d=o!=o0; print(n,'gewijzigd',d.sum(),'buiten zones',(d&~M).sum())
