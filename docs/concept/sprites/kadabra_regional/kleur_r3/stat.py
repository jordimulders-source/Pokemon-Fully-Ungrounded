# stat.py raster: aandeel a/b/c (van alle figuurpixels) en gemiddelde helderheid van de grijze vlakpixels (a, b, c; zonder lijnen, wit en zwart)
import sys,pal,numpy as np
R=pal.load(sys.argv[1]); s=''.join(R).replace('.','')
n=len(s); L={c:np.mean(pal.RGB[c]) for c in 'abc'}
g=[L[c] for c in s if c in 'abc']
print(' '.join(f'{c} {100*s.count(c)/n:.1f}%' for c in 'abcdwomkn'),'| grijs gem',round(float(np.mean(g)),1),'px',n)
