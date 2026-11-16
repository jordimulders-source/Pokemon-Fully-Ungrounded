import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'r6w')
from proj import *; import p6
o=p6.from_txt(sys.argv[1]); p6.save(o,'/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/dc7c53d6-43c5-5b88-a920-99d5791f3af7/scratchpad/t')
a=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/dc7c53d6-43c5-5b88-a920-99d5791f3af7/scratchpad/t_8x.png'); b=Image.open('r5_8x.png').convert('RGB'); m=model_s(8)
V=Image.new('RGB',(1536+16,512),'white'); V.paste(a,(0,0)); V.paste(b,(520,0)); V.paste(m,(1040,0)); V.save(sys.argv[2])
