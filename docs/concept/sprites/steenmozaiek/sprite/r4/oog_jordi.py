# Jordi (rood kruis op variant 3): "haal deze pixels eens weg" -> (14,18), (14,19), (15,19) terug naar de buurtint (7, 8, 8 zoals in r3).
from PIL import Image; import numpy as np
b=Image.open('r4/oog_3.png'); P=np.asarray(b).copy()
for (x,y),v in {(14,18):7,(14,19):8,(15,19):8,(14,20):8}.items(): P[y,x]=v  # (14,20): Jordi "die moet ook weg"
im=Image.fromarray(P,'P'); im.putpalette(b.getpalette()); im.save('r4/oog_3b.png',transparency=0); im=Image.open('r4/oog_3b.png')
c=lambda im:im.convert('RGBA').crop((7,14,20,24)).resize((13*32,10*32),Image.NEAREST)
V=Image.new('RGBA',(13*32*2+20,10*32+90),(235,235,235,255)); V.paste(c(b),(0,0)); V.paste(c(im),(13*32+20,0))
for i,s in enumerate([b,im]):
    s=s.convert('RGBA'); V.paste(s.crop((0,10,40,45)).resize((80,70),Image.NEAREST),(i*(13*32+20)+10,330),s.crop((0,10,40,45)).resize((80,70),Image.NEAREST)); V.paste(s.crop((0,10,40,45)),(i*(13*32+20)+120,345),s.crop((0,10,40,45)))
V.save('r4/oog_3b_vel.png')
