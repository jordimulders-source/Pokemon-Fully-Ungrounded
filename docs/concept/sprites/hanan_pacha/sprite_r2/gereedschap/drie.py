import sys,numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
fs=sys.argv[2:]; out=sys.argv[1]; F=6
v=Image.new('RGB',(len(fs)*(64*F+8),64*F),'white')
for i,f in enumerate(fs):
    o=np.array(Image.open(f)); v.paste(Image.fromarray(rgb(o,(248,248,248))).resize((64*F,64*F),Image.NEAREST),(i*(64*F+8),0))
v.save(out)
