# r8: bovenste voorpunt minder afgekapt (Jordi: "de bovenkant is wat afgekapt", "is nu een rechte lijn").
# Basis r7. Plek: modelsilhouet van r5 (rij 2-4 waren daar figuur). A = 1 rij terug, B = 2 rijen terug.
from PIL import Image
import numpy as np, os
d=os.path.dirname(os.path.abspath(__file__))
src=Image.open(os.path.join(d,'../sprite_r7/starmie_r7.png')); pal=src.getpalette()
base=np.array(src)
assert list(base[5,28:33])==[2,2,2,2,1]
def bouw(rijen,naam):
    a=base.copy()
    a[5,28:33]=[2,5,5,4,1]          # oude platte toprij wordt binnenrij
    for y,row in rijen: a[y,29:32]=row
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal); im.save(os.path.join(d,naam),transparency=0)
    return a
A=bouw([(4,[2,2,1])],'starmie_r8_A.png')
B=bouw([(3,[2,2,1]),(4,[2,5,1])],'starmie_r8_B.png')
ims=[Image.open(os.path.join(d,f)).convert('RGBA') for f in ('../sprite_r7/starmie_r7.png','starmie_r8_A.png','starmie_r8_B.png')]
W=Image.new('RGBA',(3*522+3*74,512),(255,255,255,255))
for i,im in enumerate(ims):
    W.alpha_composite(im.resize((512,512),Image.NEAREST),(i*522,0)); W.alpha_composite(im,(3*522+i*74,10)); W.alpha_composite(im.resize((128,128),Image.NEAREST),(3*522+i*74-30,90) if False else (3*522,90+i*135))
W.convert('RGB').save(os.path.join(d,'keuze_r7_A_B.png'))
