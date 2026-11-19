# r4 = frame 2 van r1 + Jordi's getekende vleugellijn (19 nov: "voor zover ik het kan zien zijn de pixels waar ik zwart in heb getekend de buitenlijn van de vleugel").
# Pixels gevonden door zijn screenshot (r2/jordi_lijn_vleugel.png) te registreren op het raster (rode lijnen x40=94,x45=200,x50=306,x55=413; y10=102; 21,27 px/cel; kleurfout 8,7 bij y10) en per cel zwarte penpixels te tellen.
from PIL import Image
P=[(45,9),(46,9),(44,10),(47,10),(48,10),(43,11),(48,11),(49,11),(42,12),(48,12),(48,13),(47,14),(46,15),(46,16),(46,17),(45,18),(46,18),(45,19),(45,20),(44,21),(43,22)]
for naam,v in (('A',11),('B',1)):
    im=Image.open('r1/frame2.png'); px=im.load()
    for x,y in P: px[x,y]=v
    im.save(f'r4/frame2_{naam}.png',transparency=0)
print(len(P))
