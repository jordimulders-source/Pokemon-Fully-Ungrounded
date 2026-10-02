"""Past data/layouts/Underwater_Route136/map.bin aan (kopie van Underwater_SealedChamber):
de braille onderaan het plateau wordt een zwemgat (zoals de ingang van Underwater_SeafloorCavern, metatiles
0x265-0x267 / 0x26D-0x26F, gedrag MB_WATER_DOOR). Het gat (12,43) is een warp naar de Suicune-grot.
Gebruik: python3 tools/grounded/maptools/underwater136.py (idempotent)"""
import struct, os
REPO=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
P=os.path.join(REPO,'data/layouts/Underwater_Route136/map.bin')
W,H=22,48
v=list(struct.unpack('<%dH'%(W*H),open(P,'rb').read()))
SOLID=0xc00
for i,(top,bot) in enumerate(((0x265,0x26d),(0x266,0x26e),(0x267,0x26f))):
    x=11+i
    v[42*W+x]=top|SOLID
    v[43*W+x]=bot|(0 if bot==0x26e else SOLID)
open(P,'wb').write(struct.pack('<%dH'%(W*H),*v))
print('ok')
