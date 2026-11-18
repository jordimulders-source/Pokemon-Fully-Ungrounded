# r12 = r11 + de 4 reparaties van keuring r11 (per pixel, Claude) + glansvlek weg.
from PIL import Image; import numpy as np
im=Image.open('../r11/banette_evo.png'); a=np.array(im); pal=im.getpalette()
S=[]
for x,y in ((47,9),(48,9),(48,10),(49,10),(49,11),(50,11),(49,12),(50,12),(49,13),(50,13),(50,14),(51,15),(51,16)): S.append((x,y,7))  # 1 krul donker
S.append((32,47,1))                                                   # 2 naad strookje/flap
S+= [(7,35,1),(8,35,1),(7,36,4),(8,36,1),(8,37,1)]                    # 3 linkerbel: gat hoger + spleet naar onderlijn
S+= [(52,19,1),(53,19,1),(51,20,3),(52,20,1),(52,21,1)]               # 3 rechterbel idem
S.append((11,29,1))                                                   # 4 losse pixel muts
S+= [(x,y,6) for y in range(12,20) for x in range(26,38) if a[y,x]==15]   # glansvlek weg
for x,y,v in S:
    if a[y,x]!=v: a[y,x]=v
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
