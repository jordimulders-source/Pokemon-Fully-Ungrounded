# kijk.py a.png b.png ... -> kijk.png: naast elkaar op 8x (sprites 64x64), plus kop 12x
import sys
from PIL import Image
ims = [Image.open(p).convert('RGBA') for p in sys.argv[1:]]
V = Image.new('RGB', (len(ims) * 520, 520 + 300), (255, 255, 255))
for i, im in enumerate(ims):
    b = im.resize((512, 512), Image.NEAREST); V.paste(b, (i * 520, 0), b)
    k = im.crop((0, 15, 24, 40)).resize((288, 300), Image.NEAREST); V.paste(k, (i * 520, 520), k)
V.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/c799a334-5afa-5ce2-a1de-fd8513506124/scratchpad/kijk.png')
