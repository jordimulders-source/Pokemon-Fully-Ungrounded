# Bandolingo tintzone-proef: gerichte pixellijsten op af/olinguito.png (geen filters).
from PIL import Image
import os
H=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(H,'../../../olinguito_v2/af/olinguito.png')
im=Image.open(SRC); px=im.load()
ZONES={
 # lijf: rughooglicht als zone op de bolling linksboven, loopt uit naar de staartbasis
 'rug_hooglicht': [((44,27),4),((45,27),4),((46,27),4),((44,28),4),((45,28),4)],
 # lijf: schaduw als sikkel (dun boven, breed onder) i.p.v. een even brede rand
 'schaduwsikkel': [((48,29),4),((47,30),4),((47,31),4)],
 # dij: voorlijn 2 px omhoog doorgetrokken (plooilijn die de dij tekent)
 'dijlijn': [((39,34),3),((39,35),3)],
 # schouder: korte plooilijn schouderblad -> elleboog, sluit aan op de bestaande binnenlijn
 'schouderlijn': [((36,38),3),((35,39),3),((34,40),3)],
 # verre voorpoot: selout aan de lichtkant + lichte streep (cilinder)
 'verre_voorpoot': [((25,44),3),((25,45),3),((25,46),3),((25,47),3),
                    ((26,44),4),((26,45),4),((26,46),4),((26,47),4),((24,48),3),((25,48),4)],
 # nabije achterpoot: lichtstreep doorgetrokken + selout aan de buitenrand
 'nabije_achterpoot': [((42,45),5),((42,46),5),((43,47),5),((43,48),5),((42,47),3),((42,48),3)],
}
for zone,lst in ZONES.items():
    for (x,y),c in lst:
        assert px[x,y]!=0, (zone,x,y)
        px[x,y]=c
pal=im.getpalette()
pal[15:18]=[170,121,76]   # index 5 (lichtbruin) iets lichter: meer contrast
im.putpalette(pal)
im.save(os.path.join(H,'na.png'),transparency=0)
