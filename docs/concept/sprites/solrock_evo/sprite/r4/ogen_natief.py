# Ogen uit het natieve modelraster (5,12 px) met de kleinste reductie die de lens houdt: 2x2 -> 1 spritepixel
# (de rest van de sprite is 2,32x verkleind; de ogen worden daardoor ±15 % groter dan op schaal).
# Regels per 2x2-blok: >=2 rood -> rood (licht als de lichte roodtint meerderheid heeft); anders >=2 zwart -> zwart; anders plaattint.
import numpy as np; from PIL import Image; import sys
n=np.asarray(Image.open('../natief512.png')).astype(int)
def klas(px):
    r,g,b=px; l=(r+g+b)/3
    if r-g>70 and g<90: return 'r' if r>=175 else 'R'
    if l<35: return 'K'
    if l<70 and r-b<25: return 'g'
    if r-b>40: return 'a' if l>150 else ('b' if l>105 else ('c' if l>70 else 'L'))
    return 'g'
def red(x0,y0,w,h):
    out=[]
    for j in range(h):
        row=''
        for i in range(w):
            ks=[klas(n[y0+2*j+a,x0+2*i+b]) for a in (0,1) for b in (0,1)]
            nr=sum(k in 'rR' for k in ks); nk=sum(k=='K' for k in ks)
            if nr>=2: row+='r' if sum(k=='r' for k in ks)>sum(k=='R' for k in ks) else 'R'
            elif nk>=2: row+='K'
            else:
                pl=[k for k in ks if k in 'abcLg']; row+=max(set(pl),key=pl.count) if pl else 'K'
        out.append(row)
    return out
if __name__=='__main__':
    for nm,(x0,y0,w,h) in {'L':(62,92,7,6),'R':(83,95,9,6)}.items():
        for fy in (0,1):
            for fx in (0,1):
                print(nm,'fase',fx,fy); [print('  ',r) for r in red(x0+fx,y0+fy,w,h)]
