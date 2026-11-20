# blad.npy -> pixelblad.png (64x64 op 14x, raster, coördinaten), pixelblad.csv (x,y,hex), naast.png
import numpy as np, sys
from PIL import Image
from raster import *
B=np.load(sys.argv[1] if len(sys.argv)>1 else 'blad.npy',allow_pickle=True).item()
rgb=B['rgb']; bgm=B['bg']; NR,NC=bgm.shape
S=np.full((64,64,3),255); M=np.zeros((64,64),bool); W=np.full((64,64),'',dtype='U6'); W[OY:OY+NR,OX:OX+NC]=B['why']; T=np.zeros((64,64)); T[OY:OY+NR,OX:OX+NC]=B['toon']
S[OY:OY+NR,OX:OX+NC][~bgm]=rgb[~bgm]; M[OY:OY+NR,OX:OX+NC]=~bgm
np.save('blad64.npy',{'rgb':S,'mask':M,'why':W,'toon':T},allow_pickle=True)
with open('pixelblad.csv','w') as f:
    f.write('x,y,hex\n')
    for y in range(64):
        for x in range(64):
            if M[y,x]: f.write('%d,%d,#%02X%02X%02X\n'%(x,y,*S[y,x]))
K=14
pb=labels(grid(Image.fromarray(S.astype('uint8')).resize((64*K,64*K),Image.NEAREST),K),K,18)
pb.save('pixelblad.png')
md=labels(grid(model_img(K),K),K,18)
r16=Image.open('../r16/hoatzin.png').convert('RGBA'); w=Image.new('RGB',(64,64),'white'); w.paste(r16,(0,0),r16)
r6=labels(grid(w.resize((64*K,64*K),Image.NEAREST),K),K,18)
n=Image.new('RGB',(pb.width*3+20,pb.height),'white'); n.paste(pb,(0,0)); n.paste(md,(pb.width+10,0)); n.paste(r6,(2*pb.width+20,0))
n.save('naast.png'); print('cellen',M.sum(), 'bbox y',np.where(M.any(1))[0][[0,-1]],'x',np.where(M.any(0))[0][[0,-1]])
