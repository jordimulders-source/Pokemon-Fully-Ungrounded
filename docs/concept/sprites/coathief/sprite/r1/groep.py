# Groepenkaart uit de onderlaag (geen tekenwerk): per pixel welke materiaalgroep het model daar heeft.
# . transparant  # omlijning (model-zwart)  K zwart/grijze vacht  B bruin  C creme  E oog
from PIL import Image; import numpy as np, os
D=os.path.dirname(os.path.abspath(__file__))
a=np.asarray(Image.open(os.path.join(D,'..','onderlaag_rgb.png'))).astype(int)
g=[]
for y in range(64):
  s=''
  for x in range(64):
    r,gg,b,al=a[y,x]
    if al==0: s+='.'; continue
    L=(r*299+gg*587+b*114)/1000; sat=max(r,gg,b)-min(r,gg,b)
    if 17<=x<=22 and 38<=y<=42 and r-gg>30 and L<120 and r>70: c='E'
    elif r-b>45 and sat>45: c='B'
    elif L<32: c='#'
    elif L>100 and sat<75: c='C'
    else: c='K'
    s+=c
  g.append(s)
open(os.path.join(D,'groep.txt'),'w').write('\n'.join(g)+'\n')
print('\n'.join('%2d '%i+r for i,r in enumerate(g)))
