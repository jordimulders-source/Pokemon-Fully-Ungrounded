# Stap 6: gezicht per pixel gerepareerd NAAR HET MODEL (meetkaart modelpunten.py), x20-34, y14-27.
#  - ogen: Bibarel Gen 3 (graphics/pokemon/bibarel/anim_front.png frame 1, x14-18 y14-17) pixel voor pixel, palet omgezet:
#    Bibarel 8 wit->d, 7 lichtgrijs->e, 3 zwart->1, 6 grijsbruin->a, 5 creme->7, c donker->8.
#    Nabij oog (rechts) volledig: wit x30-32, pupil (31,17), rand x29/x33. Ver oog (links) = Bibarel-oog met de rechterkolom
#    weggelaten (Pincurchin-les: smaller in perspectief door een kolom te schrappen, pupil heel): wit x22-23, pupil (23,17) = modelpupil.
#  - neus rood/oranje op de modelplek (x24-25, y19); tanden 2 px per tand op de modelplek (x24-27, y23-26), lijnen eromheen.
#  - snuit (9 met lijn 8), oogband creme (7, tussen de ogen 6 zoals het model), lijn onder de klep (2) op y14.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
o=laad('sprite_r1/gezicht.png').copy()
R={14:"x2222222222222x",   # x20..34 ; x = laten staan
   15:"x6ed777777ede77",
   16:"3adda6666addda7",
   17:"3ad1a6666ad1da7",
   18:"4add88888addd86",
   19:"4489fc999999844",
   20:"448989999999984",
   21:"4a9999999999984",
   22:"4a881111898888x",
   23:"4481dedd188888x",
   24:"4431dedd188883x",
   25:"4431dedd188883x",
   26:"3341dedd1833444",
   27:"3344111144xxxxx"}
for y,r in R.items():
    for i,c in enumerate(r):
        if c!='x': o[y,20+i]=int(c,16)
opslaan(o,'sprite_r1/gezicht2.png',8)
