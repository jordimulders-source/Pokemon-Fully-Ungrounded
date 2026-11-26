# Eindkeuring ronde 2 gaucho-Ludicolo: alleen indexwissels op de snavelrand (ogen ongewijzigd). Basis = ../af/ludicolo_gaucho.png (= mond_V2).
import os; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'..','af','ludicolo_gaucho.png')); b=im.copy()
W=[ # (x,y, was, nu, reden)
 (18,27,1,12,'2x2-lijncluster (17-18,27-28); model hier geel (225,158,83) -> geel donker'),
 (18,28,2,1,'onderkant van het bovenste snavellobje: zwart zoals (19,28) (onderkant zwart)'),
 (16,30,2,3,'dubbele lijn met de buitenlijn (15,30); terug naar de V0-tint rood diep'),
 (34,31,2,4,'L-cluster met (33,31)/(34,32); model (147,72,52) = rood donker'),
 (34,29,1,2,'rechterzijkant: zwart en rood om en om -> rode lijn'),
 (33,30,1,2,'rechterzijkant: zwart en rood om en om -> rode lijn'),
]+[(x,y,2,1,'onderkant snavel: nog rode lijn -> zwart (outline shadow, zoals x18-23)') for x,y in [(32,34),(31,35),(30,35)]+[(x,36) for x in range(24,30)]]
for x,y,was,nu,r in W:
    assert b.getpixel((x,y))==was,(x,y,b.getpixel((x,y)))
    b.putpixel((x,y),nu); print((x,y),was,'->',nu,r)
b.save(os.path.join(H,'ludicolo_gaucho_e2.png'),transparency=0)
print('totaal',len(W))
