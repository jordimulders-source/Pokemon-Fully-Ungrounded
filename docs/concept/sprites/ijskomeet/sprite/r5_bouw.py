# r5: lijf (naden uit model) + kern als spiraal met gloed + pieken + kleine fixes -> r5.txt/r5.png
import numpy as np, math
from gio import from_txt, to_txt, CH
from PIL import Image
from pal import PAL
import r5_pieken
C={c:i for i,c in enumerate(CH)}
o=from_txt('r5_lijf.txt'); r2=from_txt('r2.txt')
# lijf-fixes: dubbele buitenlijn links/linksonder weg
for (x,y,c) in [(3,36,'W'),(3,37,'W'),(4,42,'M'),(8,55,'D'),(9,56,'D'),(10,57,'D')]: o[y,x]=C[c]
# kern: gloed (v klein in het midden -> n -> j -> i), lichte krul (w) die rond de kern draait
cx,cy=25.6,34.9
for y in range(29,39):
    for x in range(21,32):
        if o[y,x]<0 or CH[o[y,x]] not in 'ijnvw': continue
        dx=(x+0.5-cx)/1.0; dy=(y+0.5-cy)/(1.1 if y+0.5<cy else 1.4)
        d=math.hypot(dx,dy)
        t='n' if d<4.0 else 'j' if d<5.4 else ('i' if CH[o[y,x]] in 'vwn' else None)
        if t: o[y,x]=C[t]
krul={(24,32):'w',(25,32):'w',(26,32):'w',(27,33):'w',(28,34):'v',(28,35):'v',(27,36):'v',(26,37):'v',(25,37):'v',(24,36):'v',
      (25,34):'v',(26,34):'v',(25,35):'v',(26,35):'w'}
for (x,y),c in krul.items(): o[y,x]=C[c]
# sterpixels: hooguit 2
o[38,40]=r2[38,40]
# pieken
o=r5_pieken.run(o)
to_txt(o,'r5.txt')
m=np.load('mask_r1.npy'); print('alpha-diff',int(((o>=0)!=m).sum()))
P=list(PAL); P[CH.index('i')]=(58,54,112); P[CH.index('j')]=(88,80,150)
im=Image.fromarray((o+1).astype('uint8'),'P'); pal=[255,255,255]+[v for c in P for v in c]; im.putpalette(pal+[0]*(768-len(pal))); im.save('r5.png',transparency=0)
print('kleuren',len(set(np.asarray(Image.open('r5.png')).ravel())))
r=Image.open('r5.png').convert('RGBA').resize((512,512),0); b=Image.new('RGBA',(512,512),(255,255,255,255)); b.alpha_composite(r); b.convert('RGB').save('r5_8x.png')
for y in range(28,40): print('%2d '%y+''.join('.' if v<0 else CH[v] for v in o[y,18:36]))
