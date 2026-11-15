# Hulpje: gezicht op 16x naast Haunters gezicht 16x. python3 .../zoom.py raster.npy uit.png
import sys; from PIL import Image; import numpy as np
S='docs/concept/sprites/hauntflare/sprite_v2/'
PAL=[(255,255,255),(0x24,0x16,0x1a),(0x5a,0x2a,0x33),(0x8a,0x4e,0x55),(0xb0,0x74,0x7a),(0xc8,0x43,0x5b),(0xf0,0x44,0x82),(0xfa,0x76,0xa2),(0xf8,0xae,0xc2),(0xf9,0xcc,0xd8),(0x9a,0x2a,0x22),(0xd8,0x40,0x30),(0xf4,0x86,0x59),(0xf8,0xb8,0x50),(0xff,0xff,0xff),(0xee,0x74,0x7c)]
o=np.load(S+sys.argv[1]) if sys.argv[1].endswith('.npy') else np.array(Image.open(S+sys.argv[1]))
x0,y0=int(sys.argv[3]) if len(sys.argv)>3 else 12,int(sys.argv[4]) if len(sys.argv)>4 else 14
im=Image.fromarray(np.array(PAL,'uint8')[o]).crop((x0,y0,x0+30,y0+28)).resize((480,448),0)
h=Image.open('graphics/pokemon/haunter/anim_front.png').convert('RGB').crop((8,22,38,50)).resize((480,448),0)
v=Image.new('RGB',(970,448),'gray'); v.paste(im,(0,0)); v.paste(h,(490,0)); v.save(sys.argv[2])
