import sys
from r4 import *
for f in sys.argv[1:]: globals()[f]()
im=Image.fromarray(S.astype('uint8'),'P'); p=[]
for c in PAL: p+=list(c)
im.putpalette(p+[0]*(768-len(p))); im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df86894d-b124-532a-bd91-e1c7851558e7/scratchpad/t1.png',transparency=0)
