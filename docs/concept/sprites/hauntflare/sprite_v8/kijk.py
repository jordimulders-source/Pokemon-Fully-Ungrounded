import sys
from PIL import Image
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/'
ims=[Image.open(p).convert('RGBA') for p in sys.argv[1:]]
W=26*14; out=Image.new('RGBA',(W*len(ims)+10*len(ims),18*14+80),(60,60,60,255))
for i,im in enumerate(ims):
    out.paste(im.crop((14,24,40,42)).resize((26*14,18*14),Image.NEAREST),(i*(W+10),0))
    out.paste(im,(i*(W+10),18*14+8),im)
out.save(S+'k.png')
