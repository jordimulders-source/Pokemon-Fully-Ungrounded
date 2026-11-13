# Buikschaduw (Jordi: "klopt de schaduw op de buik volledig?"): twee plekken waar de schaduwkant licht was.
# 1) cremestuk achter de buik/dij (x45-49, y41-45) had de lichtste tint 14 aan de onderkant -> sikkel: bovenrij 13 (x45 blijft 14), onderste rijen 12.
# 2) achterkant van de nabije achterpoot (x51-53, y41-49) had lichtblauw 7 aan de schaduwkant -> 6.
from PIL import Image; import numpy as np, sys
src=sys.argv[1]; dst=sys.argv[2]
b=Image.open(src); P=np.asarray(b).copy(); n=0
for y in range(41,46):
    for x in range(45,50):
        if P[y,x] in (13,14):
            new = 14 if (y==41 and x==45) else (13 if y<=42 else 12)
            if P[y,x]!=new: P[y,x]=new; n+=1
for y in range(41,50):
    for x in range(51,54):
        if P[y,x]==7: P[y,x]=6; n+=1
im=Image.fromarray(P,'P'); im.putpalette(b.getpalette()); im.save(dst,transparency=0); print(dst,n,'px')
