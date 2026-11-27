# Uitsnede sprite (12x) naast dezelfde uitsnede van het bewerkte natieve model (zelfde schaal).
import numpy as np; from PIL import Image; import kijk
def paar(lab_png, nat, x0,y0,x1,y1,s=12):
    sp=kijk.op_wit(Image.open(lab_png) if isinstance(lab_png,str) else lab_png,s).crop((x0*s,y0*s,x1*s,y1*s))
    nx0=2+3*x0; ny0=2+3*(y0+2); m=Image.fromarray(nat).crop((nx0,ny0,nx0+3*(x1-x0),ny0+3*(y1-y0))).resize(sp.size,Image.NEAREST)
    c=Image.new('RGB',(sp.width*2+10,sp.height),'white'); c.paste(sp,(0,0)); c.paste(m,(sp.width+10,0)); return c
