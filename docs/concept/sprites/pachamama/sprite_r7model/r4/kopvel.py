# kopvel: koppen op 12x naast elkaar + model (gelijk vergroot, zelfde raster)
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
MY,MX=-21,-2; y0,y1,x0,x1=8,34,17,44; S=12
def rgb(o): return Image.fromarray(np.array([[(255,255,255) if v==0 else PAL3[v] for v in r] for r in o],np.uint8))
items=[(a.split('=')[0],a.split('=')[1]) for a in sys.argv[2:]]
ims=[(t,rgb(np.load(f)[y0:y1,x0:x1]).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)) for t,f in items]
mg=Image.open('r4/natief_g2.png').convert('RGB').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS)
ims.append(('model, gezicht gelijk 1,28x',mg))
w,h=ims[0][1].size; v=Image.new('RGB',(len(ims)*(w+8),h+16),(235,235,235)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(ims): v.paste(im,(i*(w+8),16)); d.text((i*(w+8)+3,2),t,fill=0)
v.save(sys.argv[1])
