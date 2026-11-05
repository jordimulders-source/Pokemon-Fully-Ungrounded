"""Vergelijkvel model ↔ sprite (verplicht vóór Jordi bij elke sprite die uit een model/render komt).
Gebruik: python3 tools/grounded/model_vs_sprite.py <render_512.png> <sprite_64.png> <uit.png>
Toont: render | sprite 8x | render 55% over de sprite. Claude loopt daarna ELK onderdeel af
(kop, kuif/oren, oog, wang, snuit/snavel, borst/buik, vleugel/armen, poten/klauwen, staart, licht)
en schrijft per onderdeel 'gelijk aan render / wijkt af in ...' vóór er iets naar Jordi gaat."""
import sys
import numpy as np
from PIL import Image
render, sprite, uit = sys.argv[1:4]
r = Image.open(render).convert('RGBA').resize((512, 512))
sp = Image.open(sprite).convert('RGBA').resize((512, 512), Image.NEAREST)
v = Image.new('RGBA', (512 * 3 + 40, 512), (230, 230, 230, 255))
v.alpha_composite(r, (0, 0)); v.alpha_composite(sp, (532, 0))
ov = Image.new('RGBA', (512, 512), (230, 230, 230, 255)); ov.alpha_composite(sp)
a = np.asarray(r).copy(); a[..., 3] = (a[..., 3] * 0.55).astype('uint8'); ov.alpha_composite(Image.fromarray(a))
v.alpha_composite(ov, (1064, 0)); v.save(uit)
