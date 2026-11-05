import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maak import *
from PIL import Image
S = '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/730fa6d2-b179-5919-a5dc-5a7ead9d8899/scratchpad/hand'
def kijk(a, naam):
    im = Image.fromarray(a, 'P'); im.putpalette(PAL); im = im.convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    c8 = bg.crop((2, 42, 28, 64)).resize((26 * 10, 22 * 10), Image.NEAREST)
    f3 = bg.resize((192, 192), Image.NEAREST)
    o = Image.new('RGBA', (260 + 192 + 64 + 30, 230), (255, 255, 255, 255))
    o.paste(c8, (0, 0)); o.paste(f3, (270, 0)); o.paste(bg, (472, 0))
    o.save(os.path.join(S, naam + '.png'))
    M = '.ko3456789abclmW'
    for y in range(44, 63): print('%2d ' % y + ''.join(M[a[y, x]] for x in range(4, 25)))
