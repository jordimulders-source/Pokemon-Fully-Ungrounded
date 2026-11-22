# hulpbeeld: 9 rasterfasen van reduce.py naast elkaar (lijnen in hun modelfamilie-kleur)
import numpy as np, sys; from PIL import Image
from reduce import red; from palet import pal
P=pal('model'); f=float(sys.argv[1]); st=f/3
big=Image.new('RGB',(3*420,3*450),'white')
for a in range(3):
  for b in range(3):
    o,fam,_=red(f,a*st,b*st); im=np.zeros(o.shape+(3,),'uint8')+255
    for k,c in enumerate(P):
        if k: im[o==k]=c
    im[(o==1)&(fam==1)]=(0,90,0); im[(o==1)&(fam==2)]=(150,110,0); im[(o==1)&(fam==3)]=(140,40,60)
    ys,xs=np.where(o>0)
    big.paste(Image.fromarray(im).crop((xs.min()-1,ys.min()-1,xs.min()+59,ys.min()+63)).resize((360,384),Image.NEAREST),(b*420,a*450))
big.save(sys.argv[2])
