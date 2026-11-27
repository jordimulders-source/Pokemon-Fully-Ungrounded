import sys,numpy as np
from PIL import Image
o=sys.argv[1]; fs=sys.argv[2:]
W=Image.new('RGB',(330*(len(fs)+1),330),(98,156,131))
F=Image.open('../../../koningstiran/af/sapa_inca.png'); a=np.array(F); f=F.convert('RGBA'); f.putalpha(Image.fromarray(((a>0)*255).astype('uint8')))
W.paste(f.resize((320,320),Image.NEAREST),(0,0),f.resize((320,320),Image.NEAREST))
for i,p in enumerate(fs):
    im=Image.open(p).convert('RGBA').crop((0,0,32,32)).resize((320,320),Image.NEAREST); W.paste(im,(330*(i+1),0),im)
W.save(o)
