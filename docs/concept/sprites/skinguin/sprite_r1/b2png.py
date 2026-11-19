import sys,numpy as np; from PIL import Image
B=np.loadtxt(sys.argv[1],dtype=int); PAL=[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[3:19]]
full=np.zeros((64,64),int); full[3:,0:B.shape[1]]=B   # B2.txt is 62 breed (kolom 0 = canvas 0)
im=Image.fromarray(full.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]); im.save(sys.argv[2],transparency=0,bits=4)
