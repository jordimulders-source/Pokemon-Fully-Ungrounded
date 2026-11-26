# r16 = eindkeuring_r15, onderste mastpaneel PF terug naar 3 vakken (zoals PB, Jordi):
# alles onder PE (rij >= 54) = r12, waar PF achter PE eindigt en de PE-punt compleet is.
from PIL import Image
a=Image.open('../../eindkeuring_r15/sprite.png'); r12=Image.open('../r12/sprite.png').load()
px=a.load()
for y in range(54,64):
    for x in range(64): px[x,y]=r12[x,y]
a.save('sprite.png',transparency=0)
Image.open('sprite.png').convert('RGBA').resize((512,512),Image.NEAREST).save('sprite_8x.png')
