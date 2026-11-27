# Sprite (png) 8x naast het r7-model op dezelfde schaal (8x); optioneel uitsnede x0 y0 x1 y1 in spritepx en factor.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
sp=sys.argv[1]; out=sys.argv[2]
x0,y0,x1,y1=(int(v) for v in sys.argv[3:7]) if len(sys.argv)>6 else (0,0,64,64)
F=int(sys.argv[7]) if len(sys.argv)>7 else 8
im=Image.open(sp); im=Image.open(sp).convert('RGBA') if 'transparency' in im.info else im.convert('RGBA')
bg=Image.new('RGBA',im.size,(248,248,248,255)); bg.alpha_composite(im); im=bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*F,(y1-y0)*F),Image.NEAREST)
m=Image.open('../gemini/r7.png').convert('RGB'); P=1024/160
# modelvlak voor spritepx (X,Y): natief NX0+(X-OX)/S ... -> origineel pixels via pitch 6,4 en randfase 6,5
def o(n): return 0.1+6.4*n
mx0=o(NX0+(x0-OX)/S); mx1=o(NX0+(x1-OX)/S); my0=o(NY0+(y0-OY)/S); my1=o(NY0+(y1-OY)/S)
mm=m.crop((int(mx0),int(my0),int(mx1),int(my1))).resize(im.size,Image.LANCZOS)
v=Image.new('RGB',(im.width*2+10,im.height),(255,255,255)); v.paste(im.convert('RGB'),(0,0)); v.paste(mm,(im.width+10,0)); v.save(out)
