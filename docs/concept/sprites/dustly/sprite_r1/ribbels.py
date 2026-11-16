# Bultlijnen uit het model: natieve pixels die donkerder zijn dan hun buren aan twee overstaande kanten (dunne lijn).
import sys; sys.path.insert(0,'basis'); from bgmask import bgmask; from PIL import Image; import numpy as np
def ridges(D=14):
    a=np.asarray(Image.open('basis/natief.png').convert('RGB')).astype(float); bg=bgmask(); l=a@[.299,.587,.114]
    l2=l.copy(); l2[bg]=255
    r=np.zeros(l.shape,bool)
    for y in range(1,99):
        for x in range(1,99):
            if bg[y,x]: continue
            v=l2[y,x]
            for (dy,dx) in ((0,1),(1,0),(1,1),(1,-1)):
                p,q=l2[y-dy,x-dx],l2[y+dy,x+dx]
                if p<250 and q<250 and min(p,q)-v>=D: r[y,x]=True
    return r,l
if __name__=='__main__':
    r,l=ridges()
    for y in range(17,82): print('%2d'%y,''.join(('#' if r[y,x] else '.') for x in range(16,86)))
