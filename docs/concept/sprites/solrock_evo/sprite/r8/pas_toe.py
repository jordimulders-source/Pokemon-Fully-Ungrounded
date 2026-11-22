# Ronde 8: MOET 3a-3c, 2a en MAG uit de keuring van r7, per script.
from PIL import Image
im=Image.open('r7/sprite.png'); px=im.load()
S=lambda pts,c:[px.__setitem__(p,c) for p in pts]
S([(28,35)],1); S([(28,36)],12); S([(30,36)],1)
S([(19,34)],1); S([(15,32),(15,33),(15,34)],3); S([(16,32),(16,33),(16,34)],2)
S([(22,47),(23,47),(35,47),(36,47),(38,47),(39,47)],2)
S([(x,48) for x in list(range(24,29))+list(range(33,38))],2)
S([(x,49) for x in range(26,38)],2)
S([(21,42),(19,44),(21,44),(23,45),(21,46)],3)
S([(34,3),(52,12),(54,36),(9,45),(16,46)],6)
S([(31,14)],3)
im.save('r8/sprite.png',transparency=0)
