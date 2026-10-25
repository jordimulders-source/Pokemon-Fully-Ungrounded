"""Beeldt de kleurklassen van de onderlaag (256) af op het 64-raster van het bevroren silhouet (4x4-meerderheid).
Alleen hulpmiddel om te zien waar wat hoort; het eindraster is met de hand getypt."""
import os
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'../../../silhouet/onderlaag_b1c_256.png')).convert('RGB')
sil=[l.rstrip('\n') for l in open(os.path.join(H,'../../../silhouet/ronde1.txt')) if l.strip()]
def cls(p):
    r,g,b=p; L=(r*3+g*6+b)/10
    if r>240 and g>240 and b>240: return '.'
    if r>180 and r-b>60 and g<120: return 'E'
    if r>150 and g>100 and r-b>50 and r-b<110 and L<185: return 'T'
    if L>170: return 'C'
    if r>150 and g<110 and b<90: return 'E'
    if L<28: return 'K'
    if r-b>40 and L>70: return 'B' if L>85 else 'S'
    return 'D'
out=[]
for y in range(64):
    row=''
    for x in range(64):
        c=Counter(cls(im.getpixel((x*4+i,y*4+j))) for i in range(4) for j in range(4))
        k=[k for k,_ in c.most_common() if k!='.']
        ch=k[0] if k else '.'
        if 'E' in c: ch='E'
        if sil[y][x]=='#': row+=ch if ch!='.' else '?'
        else: row+='.' if ch=='.' else ' '
    out.append(row)
open(os.path.join(H,'klassen.txt'),'w').write('\n'.join(out)+'\n')
print('\n'.join('%2d %s'%(i,r) for i,r in enumerate(out)))
