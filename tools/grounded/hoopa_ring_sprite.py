"""Project Grounded: overworld-object van Hoopa's ring (Hoopa-quest, Mirage Bazaar).

Hergebruikt de ring uit Hoopa's gevechtsanimatie (graphics/battle_anims/sprites/hoopa_ring.png, 32x32) als
stilstaand object (OBJ_EVENT_GFX_HOOPA_RING): de luchtspiegeling in de woestijn van Route 111 en de ringen in de
bazaar en de schatkamer. Schrijft graphics/object_events/pics/misc/hoopa_ring.png + palettes/hoopa_ring.pal.

Gebruik: python3 tools/grounded/hoopa_ring_sprite.py"""
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
src = Image.open(os.path.join(ROOT, 'graphics/battle_anims/sprites/hoopa_ring.png'))
assert src.mode == 'P' and src.size == (32, 32)
src.save(os.path.join(ROOT, 'graphics/object_events/pics/misc/hoopa_ring.png'))
pal = src.getpalette()[:48]
pal += [0] * (48 - len(pal))
with open(os.path.join(ROOT, 'graphics/object_events/palettes/hoopa_ring.pal'), 'w', newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n')
    for i in range(16):
        f.write('%d %d %d\n' % tuple(pal[i * 3:i * 3 + 3]))
print('klaar: hoopa_ring.png + hoopa_ring.pal')
