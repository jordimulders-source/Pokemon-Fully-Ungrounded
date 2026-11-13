# Eindkeuring DFC: MOET 2 + MAG 1-2 toepassen op huidig (zwart) en selout B; alleen de buitenlijn verschilt tussen de twee.
from PIL import Image; import numpy as np
ED={(14,61):7,(15,61):7,(16,61):7,(18,61):7,(19,61):7,(56,51):12,(48,18):4,(46,20):4}
out={}
for naam,src in (('zwart','steenjaguar_r4.png'),('selout','eindkeuring/selout_voorstel_b.png')):
    b=Image.open(src); P=np.asarray(b).copy()
    for (x,y),v in ED.items(): P[y,x]=v
    im=Image.fromarray(P,'P'); im.putpalette(b.getpalette()); im.save(f'steenjaguar_r4_{naam}.png',transparency=0); out[naam]=Image.open(f'steenjaguar_r4_{naam}.png').convert('RGBA')
d=(np.asarray(Image.open('steenjaguar_r4_zwart.png'))!=np.asarray(Image.open('steenjaguar_r4_selout.png'))).sum(); print('verschil buitenlijn',d,'px')
V=Image.new('RGBA',(512*2+20,512+160),(235,235,235,255))
for i,k in enumerate(('zwart','selout')):
    s=out[k]; V.paste(s.resize((512,512),Image.NEAREST),(i*532,0),s.resize((512,512),Image.NEAREST))
    for j,bg in enumerate(((248,248,248,255),(40,44,56,255))):
        t=Image.new('RGBA',(150,150),bg); t.paste(s.resize((128,128),Image.NEAREST),(11,11),s.resize((128,128),Image.NEAREST)); t.paste(s,(80,80),s); V.paste(t,(i*532+j*170,515))
V.save('buitenlijn_keuze.png')
