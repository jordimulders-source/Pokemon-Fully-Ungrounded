# kleurgroepen per cel van het pixelblad (alleen kleurregels op de modelkleur, plus plaats voor buik/staart)
import numpy as np
def klassen(rgb,mask):
    R,G,B=[rgb[...,i].astype(float) for i in range(3)]; L=rgb@np.array([.299,.587,.114])
    mx=rgb.max(2); mn=rgb.min(2); sat=mx-mn
    Y,X=np.mgrid[:64,:64]
    k=np.full((64,64),'',dtype='U6')
    k[mask]='mauve'
    k[mask&(R>B+28)&(R>G+20)&(L<120)&(Y<24)]='bruin'
    k[mask&(sat<26)&(L>=55)]='grijs'
    k[mask&(B>R+25)]='blauw'
    k[mask&(R>B+20)&(R>G+25)&(L>=85)&(Y>=34)&(X<40)]='buik'
    k[mask&(L<45)&(k!='bruin')]='lijn'
    k[mask&(L<75)&(Y>=44)&(X>=34)&(X-0.65*Y>=4)]='staart'   # donkere staartveren onder de vleugel (rechtsonder)
    k[mask&(L<45)&(k=='staart')]='lijn'
    return k,L
