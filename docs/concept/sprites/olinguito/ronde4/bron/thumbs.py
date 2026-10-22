"""Ronde 4: drie Gen 3-oogtypes op dezelfde kop (6x) en de hele sprite (1x en silhouet).
A Poochyena: zwaar zwart lid, glans boven de pupil, gouden iris (gekozen: sluw en Dark)
B Teddiursa/Zigzagoon: rond zwart oog met 1 witte glans (lief, geen typesignaal)
C Treecko/Sneasel: hoog ovaal oog met spleetpupil (alert, minder sluw)
python3 thumbs.py <uit.png>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import build
from shapepaint import to_rgba

EYES = {
    'A Poochyena-lid (gekozen)': (['oowooo', 'oGoigG', '.Gogg.'], ['oow', 'Go.', 'G..']),
    'B rond zwart (Teddiursa)': (['.ooo..', 'owoo..', 'oooo..'], ['oo.', 'wo.', 'oo.']),
    'C ovaal, spleetpupil': (['.oooo.', 'owgoG.', 'oggoG.'], ['oo.', 'go.', 'go.']),
}
z = 6
cols = len(EYES)
sheet = Image.new('RGB', (cols * (30 * z + 8), 24 * z + 64 + 64 + 40), (240, 238, 230)); d = ImageDraw.Draw(sheet)
for i, (n, (near, far)) in enumerate(EYES.items()):
    build.EYE_NEAR, build.EYE_FAR = near, far
    f = build.frame1()
    x = i * (30 * z + 8)
    d.text((x + 2, 2), n, fill=(0, 0, 0))
    im = to_rgba(f, build.PAL, 1, (205, 222, 205, 255))
    sheet.paste(im.crop((6, 10, 36, 34)).resize((30 * z, 24 * z), Image.NEAREST).convert('RGB'), (x, 14))
    sheet.paste(im.convert('RGB'), (x, 20 + 24 * z))
    a = np.full((64, 64, 3), 240, np.uint8); a[f > 0] = (20, 20, 20)
    sheet.paste(Image.fromarray(a), (x + 70, 20 + 24 * z))
sheet.save(sys.argv[1]); print(sys.argv[1])
