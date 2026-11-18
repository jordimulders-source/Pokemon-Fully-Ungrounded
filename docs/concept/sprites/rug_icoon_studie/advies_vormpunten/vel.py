"""vel.py uit.png a.png b.png ... : front (4x) + iconen (8x) + iconen 1x op groen tussen in-game buren"""
import sys
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
fr=Image.open(R+'docs/concept/sprites/viscacha/af/viscacha.png').convert('RGBA').crop((0,0,64,64))
ics=[Image.open(p).convert('RGBA').crop((0,0,32,32)) for p in sys.argv[2:]]
bur=[Image.open(R+f'graphics/pokemon/{s}/icon.png').convert('RGBA').crop((0,0,32,32)) for s in ('rattata','eevee','raichu','dedenne')]
Z=8; W=256+20+len(ics)*(32*Z+12); H=32*Z+60
im=Image.new('RGBA',(W,H),(255,255,255,255))
im.alpha_composite(fr.resize((256,256),Image.NEAREST),(0,0))
for i,c in enumerate(ics):
    bg=Image.new('RGBA',(32,32),(152,208,160,255)); bg.alpha_composite(c)
    im.alpha_composite(bg.resize((32*Z,32*Z),Image.NEAREST),(276+i*(32*Z+12),0))
row=Image.new('RGBA',(32*(4+len(ics)),32),(98,156,131,255))
for i,c in enumerate(bur[:2]+ics+bur[2:]): row.alpha_composite(c,(32*i,0))
im.alpha_composite(row.resize((row.width*2,64),Image.NEAREST),(0,32*Z-4+8))
im.save(sys.argv[1])
