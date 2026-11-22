# Diffbewijs r3 -> r4: lavabrok, ogen, kelp, kieren/kwijl/mond (gloed), zwart, silhouet en palet buiten index 8.
import numpy as np; from PIL import Image
a=Image.open('r3/gloom_r3.png'); b=Image.open('r4/gloom_r4.png')
o=np.array(a).astype(int); n=np.array(b).astype(int); d=o!=n
pa=a.getpalette()[:48]; pb=b.getpalette()[:48]
print('palet gewijzigd op indexen:',[k for k in range(16) if pa[3*k:3*k+3]!=pb[3*k:3*k+3]])
brok=np.zeros_like(d); brok[:26,:]=True                      # alles boven het lijf (y<=25)
steen_gloed=np.isin(o,[2,3,4,9,10,11,15])                     # steen + gloed + sintel overal (brok, kieren, kwijl, mond)
print('lavabrok (y<=25, alle pixels):',int((d&brok).sum()))
print('steen/gloed/sintel-pixels overal:',int((d&steen_gloed).sum()))
print('zwart (lijn, ogen, mondlijn):',int((d&(o==1)).sum()), '| nieuw zwart:',int((d&(n==1)).sum()))
ogen=np.zeros_like(d); ogen[28:32,18:34]=True
print('ogen (zwart in x18-33, y28-31):',int((d&ogen&((o==1)|(n==1))).sum()))
print('kelp (12-14):',int((d&np.isin(o,[12,13,14])).sum()),'| nieuw kelp:',int((d&np.isin(n,[12,13,14])).sum()))
print('silhouet (transparant <-> figuur):',int(((o==0)!=(n==0)).sum()))
print('wissels buiten lijftinten 5-8:',int((d&~(np.isin(o,[5,6,7,8])&np.isin(n,[5,6,7,8]))).sum()))
print('totaal gewijzigde pixels:',int(d.sum()))
