# Palet (index = klasse uit lib.NAMEN). Zwart = blauwzwart zoals Gen 3 Murkrow/Umbreon (vlakken leesbaar tegen de lijn);
# volgorde van de tinten = modelmetingen (km.py: 3 / 18 / 27-29 / 36-48 / 53 / 68 / 101-154). Roze = Pom-Pom/Baile-poot en -snavel.
from lib import NAMEN
PAL={'_':(152,208,160),'O':(16,16,24),'D1':(28,28,42),'D2':(40,42,60),'D3':(54,58,82),'D4':(68,72,100),'D5':(90,96,128),'D6':(132,138,172),
     'K1':(255,166,181),'K2':(191,105,120),'K3':(115,63,72),'W':(255,255,255),'R':(136,24,40),'R2':(88,16,30)}
NAMEN2=NAMEN+['R2']
def pal(): return [PAL[n] for n in NAMEN2]
