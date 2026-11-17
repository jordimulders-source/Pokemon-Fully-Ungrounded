# Ronde 12: basis r11. Reparaties van de keurder (fit model x163-859 -> 11-50, y82-941 -> 15-62; kale reductie
# scratchpad/k11/kaal.png). Elke pixel uit het model (rijbreedte per keurdermeting) of de kale reductie van de keurder.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
K11='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f952c4af-e06e-5b56-87d5-86ed60c9233c/scratchpad/k11/kaal.png'
im=Image.open(D+'r11/mate.png'); PAL=im.getpalette(); r11=np.asarray(im).astype(int); a=r11.copy()
k=np.asarray(Image.open(K11)).astype(int)
C={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5}
FIX=[
 # 1 linkerhoorn: modelrijen y22 x18, y23 x18-19, y24 x17-19, y25 x17-20; buitenlijn binnen de modelvorm
 (19,22,'.','buiten model'),(20,23,'.','buiten model'),(20,24,'.','buiten model'),(21,25,'.','buiten model'),
 (19,23,'a','rechterrand binnen model (rij x18-19)'),(19,24,'a','rechterrand binnen model (rij x17-19)'),
 (20,25,'a','rechterrand binnen model (rij x17-20)'),
 (21,26,'a','rand: grensde na het weghalen van (21,25) open aan de lucht'),
 # 2 voet linkerhoorn: tonen kale reductie keurder
 (18,28,'a','kaal 2'),(19,28,'b','kaal 3'),(20,28,'c','kaal 4'),(21,28,'c','kaal 4'),(22,28,'c','kaal 4'),(23,28,'b','kaal 3'),
 (18,29,'a','kaal 2'),(19,29,'b','kaal 3'),(20,29,'b','kaal 3'),(21,29,'c','kaal 4'),
 (19,30,'a','kaal 2 (vouw weg)'),
 # 3 rechterhoorn
 (44,24,'.','buiten model'),(46,23,'#','punt 2 px breed (x45-46); rechterkant zwart zoals de rand eronder'),
 (45,24,'a','linkerrand binnen model na het weghalen van (44,24)'),
 # 4 linkerhand
 (12,42,'a','hand: modelrand linksboven'),(13,42,'d','vulling, kaal 5 (d)'),(13,41,'a','rand boven (13,42), anders open'),
 (11,47,'#','hand: modelrand linksonder (zwarte onderboog)'),(12,47,'b','vulling, kaal 3 (b)'),
 # 5 rechteroog: bovenrand op y36 (rij y35 = kale reductie), y41 x30-33 lichtbruine onderrand
 (29,35,'b','kaal 3'),(30,35,'b','kaal 3'),(31,35,'b','kaal 3'),
 (30,41,'d','lichtbruine onderrand'),(31,41,'d','idem'),(32,41,'d','idem'),(33,41,'d','idem'),
]
for x,y,c,_ in FIX: a[y,x]=C[c]
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r12/mate.png',transparency=0)
Z=np.zeros((64,64),bool)
for x,y,_,_ in FIX: Z[y,x]=True
d=a!=r11; print('buiten de reparaties anders dan r11:',int((d&~Z).sum()),'| gewijzigd:',int((d&Z).sum()))
ch='.#abcdGHIstu'
for (x0,y0,x1,y1) in ((15,21,26,31),(39,21,48,33),(9,39,17,51),(26,34,36,43)):
    for y in range(y0,y1+1): print(y,''.join(ch[v] for v in a[y,x0:x1+1]),' ',''.join(ch[v] for v in r11[y,x0:x1+1]))
    print()
