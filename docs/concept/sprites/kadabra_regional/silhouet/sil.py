# silhouet = model verkleind (dekking >= 0,5 per spritepixel, kleur_r1/meet.npz) + 13 px in dunne delen met de hand (dekking 0,3-0,5 in het model):
# kaartrand boven (3,19) (4,19) en links (1,23); duim boven (47,25); onderlijn klauw rechtervinger (60,25); tweede gebogen vinger (6,31) (7,32) (8,32);
# hielklauw linkervoet (27,55) (28,56); onderlijn teenklauw (18,60) (19,60); teenklauw rechtervoet (40,61).
# Gaten die in het model achtergrond zijn (onder de duim, tussen arm en romp, tussen de vingers) blijven open. Bevroren vanaf kleur_r1.
import numpy as np
from PIL import Image
s=np.load('../kleur_r1/meet.npz')['sil'].copy()
for x,y in [(3,19),(4,19),(1,23),(47,25),(60,25),(6,31),(7,32),(8,32),(27,55),(28,56),(18,60),(19,60),(40,61)]: s[y,x]=True
Image.fromarray((s*255).astype('uint8')).save('silhouet.png')
ys,xs=np.where(s); print('box',xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'px',s.sum())
