import sys
from PIL import Image
import tempfile; S=tempfile.gettempdir()+'/'
im=Image.open(sys.argv[1]); im.save(S+'_t.png',transparency=0)
a=Image.open(S+'_t.png').convert('RGBA').resize((512,512),Image.NEAREST)
m=Image.open('r3/model_A3.png').convert('RGBA').crop((91-6*16,0,91-6*16+1024,1024)).resize((512,512),Image.LANCZOS)
V=Image.new('RGBA',(1034,512),(255,255,255,255)); V.paste(a,(0,0),a); V.paste(m,(522,0)); V.save(S+sys.argv[2])
