# Laatste per-pixelreparaties (na eigen controle en clusterscript), op stap_lijf.png -> sprite.png
from PIL import Image; import numpy as np
im=Image.open('sprite_r6/stap_lijf.png'); pal=im.getpalette(); a=np.array(im)
F={(15,14):12,                       # gat tussen schoorsteenrand en geest: achterrand doorlopen (C)
   (33,2):5,(34,2):5,(35,2):5,(36,2):5,  # pluim rechtsboven op het hoofd: binnenkleur i.p.v. losse licht/donker-pixels
   (15,12):5,(22,12):5,(16,13):5,     # losse lichte randpixels linkerkwab
   (11,53):1}                          # losse groene pixel in de tussenruimte koeienvanger
for (x,y),v in F.items(): a[y,x]=v
# onderrand geest (rij 14): nu de steelrij weg is, krijgt de onderkant een donkergroene lijn
for x in range(21,40):
    if a[14,x] in (2,5): a[14,x]=6
# onderkant rond i.p.v. één rechte lijn van 22 px: lijf buigt rechts omhoog naar de arm (model: gat tussen lijf en arm)
for x in range(27,33): a[14,x]=0
for x in range(27,32): a[13,x]=6
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r6/sprite.png',transparency=0)
