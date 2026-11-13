# klasseer modelpixels naar paletindex (onderlaag)
import numpy as np
def klas(c):
    c=c.astype(float); r,g,b=c[...,0],c[...,1],c[...,2]; L=c.mean(-1); sat=c.max(-1)-c.min(-1)
    out=np.zeros(c.shape[:-1],int)
    yel=(g>0.68*r)&(r>110)&(b<g-25)
    gray=(sat<30)&~yel
    pink=(~yel)&(~gray)&(g/np.maximum(r,1)>0.47)
    red=~(yel|gray|pink)
    # rood
    out[red&(L<38)]=1; out[red&(L>=38)&(L<52)]=15; out[red&(L>=52)&(L<66)]=2
    out[red&(L>=66)&(L<86)]=3; out[red&(L>=86)&(L<112)]=4; out[red&(L>=112)&(L<140)]=5; out[red&(L>=140)]=6
    out[pink&(L<90)]=7; out[pink&(L>=90)&(L<135)]=7; out[pink&(L>=110)&(L<150)]=8; out[pink&(L>=150)]=9
    out[yel&(L<130)]=10; out[yel&(L>=130)&(L<175)]=11; out[yel&(L>=175)]=12
    out[gray&(L<34)]=1; out[gray&(L>=34)&(L<75)]=14; out[gray&(L>=75)]=13
    out[(L>235)&(sat<20)]=0
    return out
