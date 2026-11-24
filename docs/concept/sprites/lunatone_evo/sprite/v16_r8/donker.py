# Iris donkerder zoals Lunatone (perspectief): alleen paletkleuren van het oog
from PIL import Image
NIEUW = {8: (140, 14, 26), 9: (190, 30, 40), 11: (96, 8, 18), 10: (214, 92, 100)}
for n in ('A_0px', 'B_2px', 'C_4px'):
    im = Image.open(n + '.png'); p = im.getpalette()
    for i, c in NIEUW.items(): p[i*3:i*3+3] = list(c)
    im.putpalette(p); im.save(n + '_donker.png', transparency=0)
    Image.open(n + '_donker.png').convert('RGBA').resize((512, 512), Image.NEAREST).save(n + '_donker_8x.png')
