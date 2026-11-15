# Hulpje: toont een indexraster (npy) op 10x op wit, naast de basis. python3 .../toon.py stap1_kleur.npy uit.png
import sys; sys.path.insert(0,'docs/concept/sprites/hauntflare/sprite_v2')
from PIL import Image; import numpy as np
S='docs/concept/sprites/hauntflare/sprite_v2/'
PAL=[(255,255,255),(0x24,0x16,0x1a),(0x5a,0x2a,0x33),(0x8a,0x4e,0x55),(0xb0,0x74,0x7a),(0xc8,0x43,0x5b),(0xf0,0x44,0x82),(0xfa,0x76,0xa2),(0xf8,0xae,0xc2),(0xf9,0xcc,0xd8),(0x9a,0x2a,0x22),(0xd8,0x40,0x30),(0xf4,0x86,0x59),(0xf8,0xb8,0x50),(0xff,0xff,0xff),(0xee,0x74,0x7c)]
o=np.load(S+sys.argv[1]) if sys.argv[1].endswith('.npy') else np.array(Image.open(S+sys.argv[1]))
im=np.array(PAL,'uint8')[o]
b=Image.open('docs/concept/sprites/hauntflare/basis/basis_64.png'); w=Image.new('RGBA',(64,64),'white'); w.alpha_composite(b)
v=Image.new('RGB',(1290,640),'gray'); v.paste(Image.fromarray(im).resize((640,640),0),(0,0)); v.paste(w.convert('RGB').resize((640,640),0),(650,0))
v.save(sys.argv[2])
