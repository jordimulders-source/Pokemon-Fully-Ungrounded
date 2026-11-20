# Snelle preview van een klassenraster in modelkleuren (8x) naast het natief model (bewerkt) op dezelfde schaal
import sys; import numpy as np; from PIL import Image
C={'.':(255,255,255),'K':(0,0,0),'k':(30,30,30),'o':(84,60,24),'Y':(232,204,90),'y':(172,142,55),'B':(70,100,155),'b':(45,70,110),'R':(165,50,50),'W':(250,250,250),'?':(255,0,255)}
g=np.load(sys.argv[1]); H,W=g.shape
a=np.array([[C[ch] for ch in r] for r in g],'uint8')
im=Image.fromarray(a).resize((W*12,H*12),Image.NEAREST)
n=Image.open('n_edit.png').crop((29,7,29+48,7+87)).resize((W*12,H*12),Image.NEAREST)
out=Image.new('RGB',(W*24+10,H*12),(200,200,200)); out.paste(im,(0,0)); out.paste(n,(W*12+10,0)); out.save(sys.argv[2])
