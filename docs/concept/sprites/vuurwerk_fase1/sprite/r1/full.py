# sprite 8x | model verkleind (zelfde schaal) naast elkaar
import sys,numpy as np; from PIL import Image
from reduce2 import PAL
a=np.load(sys.argv[1]); Z=int(sys.argv[3]) if len(sys.argv)>3 else 8
rgb=PAL[a].astype('uint8'); rgb[a==0]=255
A=Image.fromarray(rgb).resize((a.shape[1]*Z,a.shape[0]*Z),Image.NEAREST)
f=lambda v,o:(o+3*v)*5.12-0.42
B=Image.open('../../referenties/model.png').convert('RGB').crop((round(f(0,76)),round(f(0,14)),round(f(a.shape[1],76)),round(f(a.shape[0],14)))).resize(A.size,Image.LANCZOS)
S=Image.new('RGB',(A.width*2+10,A.height),'white'); S.paste(A,(0,0)); S.paste(B,(A.width+10,0)); S.save(sys.argv[2])
