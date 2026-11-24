# Gnomad tintzones-proef (24 nov). Alleen gerichte pixellijsten, geen kwantiseren/blur.
from PIL import Image
import os
D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, '../../../gnomad/af/gnomad.png')
im = Image.open(SRC); px = im.load()
orig = im.copy(); opx = orig.load()

edits = {
 # MUTS: buitenlijn linksboven consequent in eigen donker (2), airbrushpixel weg
 'muts_lijn': [((24,11),2),((25,11),2),((23,12),5),((20,15),5)],
 # MUTS: plooilijn boven de omgeslagen rand als één doorlopende lijn van 1 px
 'muts_randplooi': [((18,21),2),((19,21),2),((20,21),2),((21,21),2),((26,22),2),((27,23),2),((29,24),2),((30,24),2)],
 # MUTS: rand (band) links één lichte zone, onderkant één schaduwzone
 'muts_rand': [((14,22),5),((13,24),5),((12,25),3),((13,25),3)],
 # MUTS: tweede (parallelle) vouwlijn weg; flap = één schaduwvlak, lichte rand-ring aan de schaduwkant weg
 'muts_flap': [((41,20),3),((41,21),3),((41,22),3),
               ((45,22),3),((46,22),3),((47,22),3),((48,22),3),((46,23),3),((47,23),3),((48,23),3),
               ((47,24),3),((48,24),3),((48,25),3),((48,26),3),((49,27),3),((49,28),3)],
 # MUTS: los lichtpixel in de punt wordt de belichte bovenkant van de punt
 'muts_punt': [((55,35),4),((56,35),4)],
 # LIJF: losse donkere vlekjes onder de snor weg (één grondtint)
 'lijf_romp': [((16,39),8),((17,39),8),((21,39),8),((14,40),8),((15,40),8),((22,40),8),((23,40),8)],
 # LIJF: schaduwsikkel rechts als één 7-zone, 6-vlekjes erin weg
 'lijf_sikkel': [((35,34),7),((36,34),7),((38,34),7),((36,35),7),((39,35),7),((40,35),7),((39,36),7)],
 # HAND LINKS: lijn lichtkant in 6, arm boven licht / onder schaduw, hand licht linksboven + sikkel rechtsonder, polslijn blijft
 'hand_links': [((5,40),6),((4,41),6),((12,40),8),((11,41),8),((12,41),8),((7,42),8),((9,42),7),((7,43),7),((8,43),7)],
 # HAND RECHTS: buitenlijn schaduwkant zwart, schaduwsikkel rechtsonder
 'hand_rechts': [((49,42),1),((48,43),7),((47,44),7),((46,45),7),((47,45),7)],
}
for zone, lst in edits.items():
    for (x,y),c in lst:
        assert px[x,y] != 0, (zone,x,y)
        px[x,y] = c

pal = im.getpalette()
pal[3*3:3*3+3] = [130,104,178]   # lila schaduw: verzadigder
pal[4*3:4*3+3] = [178,150,224]   # lila grondtint
pal[5*3:5*3+3] = [212,190,246]   # lila licht
im.putpalette(pal)
im.save(os.path.join(D, 'na.png'))
for zone, lst in edits.items():
    n = sum(1 for (x,y),c in lst if opx[x,y] != c)
    print(zone, n)
