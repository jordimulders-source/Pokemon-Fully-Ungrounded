# Klassen per natieve modelpixel (geen tekenen: alleen indelen van modelkleuren).
import numpy as np
from PIL import Image
NAMEN=['bg','K','T0','T1','T2','T3','O0','O1','O2','O3','R0','R1','RW']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    c=np.zeros(a.shape[:2],int)
    bg=a.min(2)>=215
    red=(R>G+50)&(R>B+50)
    glint=(R>200)&(G>150)&(B>140)&(R>G+12)&~bg
    teal=(G>R+25)&(B>R+10)&~red
    for (y,x) in zip(*np.where(~bg)):
        l=L[y,x]
        if glint[y,x]: c[y,x]=12
        elif red[y,x]: c[y,x]=10 if l<85 else 11
        elif l<40: c[y,x]=1
        elif teal[y,x]: c[y,x]=2 if l<108 else 3 if l<135 else 4 if l<168 else 5
        else: c[y,x]=6 if l<80 else 7 if l<123 else 8 if l<175 else 9
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN): print(n,(c==i).sum())
    ch='.K0123abcdrRw'
    for y in range(17,82): print(''.join(ch[v] for v in c[y,22:88]))
