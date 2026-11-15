# snel kijkvel: gezicht 12x van de opgegeven pngs + Haunter
import sys
from PIL import Image
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/kijk.png'
fs=sys.argv[1:]; Z=12; box=(12,16,44,42); w=(box[2]-box[0])*Z; h=(box[3]-box[1])*Z
c=Image.new('RGB',((w+8)*len(fs),h+70),'white')
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im)
    c.paste(bg.crop(box).resize((w,h),Image.NEAREST),(i*(w+8),0))
    c.paste(bg,(i*(w+8),h+4))
c.save(S)
