# Klassen per natieve modelpixel (geen tekenen: alleen indelen van modelkleuren).
# groepen: K zwart, R lijf (rood/bordeaux), S lavasteen (grijs), G gloed (oranje), O kelp (olijf/bruin)
import numpy as np; from PIL import Image
NAMEN=['bg','K','S','R','G','O']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    mx=a.max(2); mn=a.min(2); sat=mx-mn
    c=np.zeros(a.shape[:2],int)
    bg=mn>=215
    glow=(R>=150)&(R-B>=100)&~bg
    red=(R>G+35)&(R>B+12)&~glow&~bg
    olive=(G>=B+12)&(R>=B+12)&(np.abs(R-G)<45)&(sat>=18)&~bg&~red&~glow
    for (y,x) in zip(*np.where(~bg)):
        if glow[y,x]: c[y,x]=4
        elif red[y,x]: c[y,x]=3 if L[y,x]>=38 else 1
        elif olive[y,x]: c[y,x]=5 if L[y,x]>=40 else 1
        elif L[y,x]<26: c[y,x]=1
        elif sat[y,x]<=24: c[y,x]=2
        else: c[y,x]=5 if (R[y,x]>=B[y,x]+10 and G[y,x]>=B[y,x]+5) else (3 if R[y,x]>G[y,x]+15 else 2)
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/50/90', np.percentile(L[m],[10,50,90]).astype(int) if m.any() else '')
    ch='.KSRGO'
    for y in range(18,124): print('%3d '%y+''.join(ch[v] for v in c[y,19:129]))
