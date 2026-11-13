# Jordi: "bol ietsje blauwer misschien zodat het verschilt van het lichaam". Alleen de binnenkleur van de bol (index 5/6 binnen bol_mask) krijgt een eigen, blauwere paletkleur (index 14). Verder niets.
from PIL import Image; import numpy as np
o=np.array(Image.open('sprite/onderlaag.png')); g=np.load('sprite/bol_mask.npy')
P=np.array(Image.open('sprite/onderlaag.png').getpalette()[:48]).reshape(16,3)
for naam,kleur in [('A',(206,225,240)),('B',(194,216,238))]:
    q=o.copy(); m=g&((o==5)|(o==6)); q[m]=14
    pal=P.copy(); pal[14]=kleur
    im=Image.new('P',(64,64)); im.putpalette(pal.reshape(-1).tolist()+[0]*(768-48)); im.putdata(q.reshape(-1).tolist()); im.save(f'sprite/r1_{naam}.png',transparency=0)
    print(naam,'px gewijzigd',int(m.sum()))
# vel: onderlaag | A | B op 8x, plus 1x
ims=[Image.open(f).convert('RGB') for f in ('sprite/onderlaag.png','sprite/r1_A.png','sprite/r1_B.png')]
def wit(im,f):
    a=np.array(im); o2=np.array(Image.open(f)); a[o2==0]=255; return Image.fromarray(a)
ims=[wit(i,f) for i,f in zip(ims,('sprite/onderlaag.png','sprite/r1_A.png','sprite/r1_B.png'))]
v=Image.new('RGB',(3*528,512+80),'white')
for k,i in enumerate(ims):
    v.paste(i.resize((512,512),Image.NEAREST),(k*528,0)); v.paste(i,(k*528,520))
v.save('sprite/r1_vel.png')
