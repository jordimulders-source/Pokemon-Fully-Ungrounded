# Klassen per natieve modelpixel (natief raster 5,12 px).
import numpy as np; from PIL import Image
import os
N=np.asarray(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','natief512.png'))).astype(int)
p,ph=5.12,4.25; S=11.87; X0=138-0.5*S; Y0=107-1.2*S
def klas(px):
    r,g,b=px; l=(r+g+b)/3
    if r-g>70 and g<90: return 'r' if r>=175 else 'R'
    if l<35: return 'K'
    if l<70 and r-b<25: return 'g'
    if r-b>40: return 'A' if l>175 else 'a' if l>150 else ('b' if l>105 else ('c' if l>70 else 'L'))
    if l>200: return 'w'
    return 'g'
def sx(i): return (ph+p/2+i*p-X0)/S
def sy(j): return (ph+p/2+j*p-Y0)/S
