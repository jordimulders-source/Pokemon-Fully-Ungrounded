# snelle blik: A | B | r9 | model op 8x (naar het kladblok of argv[1])
import os,sys,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,H+'/../r8'); from gemeen import model_op_schaal
def rgb(path,bg=(255,255,255)):
    im=Image.open(path); a=np.array(im); w=np.array(im.convert('RGB')); w[a==0]=bg; return Image.fromarray(w)
ims=[rgb(H+'/hoatzin_r10_A.png'),rgb(H+'/hoatzin_r10_B.png'),rgb(H+'/../r9/hoatzin_r9.png'),model_op_schaal().convert('RGB')]
f=int(sys.argv[2]) if len(sys.argv)>2 else 8
out=Image.new('RGB',(4*64*f+30,64*f),(200,200,200))
for i,m in enumerate(ims): out.paste(m.resize((64*f,64*f),0),(i*(64*f+10),0))
out.save(sys.argv[1])
