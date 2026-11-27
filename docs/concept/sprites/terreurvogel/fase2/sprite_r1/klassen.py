# Kleurgroep per natieve modelpixel: 0 bg, 1 zwart, 2 lijf, 3 snavel, 4 gezicht, 5 poten, 6 oog (iris), 7 oogring
# Kleur + plek (snavel/gezicht alleen in de kop, poten alleen onder het lijf, oog = cirkel rond het modeloog).
import numpy as np; from PIL import Image
OOG=(63.5,48.0); OOGR=6.3
def klassen(a):
    a=a.astype(float); R,G,B=a[...,0],a[...,1],a[...,2]; H,W=R.shape
    yy,xx=np.mgrid[0:H,0:W]
    L=0.299*R+0.587*G+0.114*B; mx=a.max(2); mn=a.min(2); sat=(mx-mn)/np.maximum(mx,1)
    k=np.full(R.shape,2)
    k[mn>=225]=0
    k[(L<48)&(k!=0)]=1
    gr=G/np.maximum(R,1); bg_=B/np.maximum(G,1)
    kop=(xx<82)&(yy<92)
    pootzone=(yy>=124)|((xx>=140)&(yy>=118))
    k[(gr>0.62)&(bg_<0.80)&kop&(k==2)]=3
    k[(gr>0.58)&pootzone&(k==2)]=5
    k[(gr>0.57)&kop&(k==2)&(L<110)&(xx<74)]=3   # bruine snavellijnen
    k[(gr>0.57)&pootzone&(k==2)&(L<110)]=5      # bruine pootlijnen
    k[(gr>0.50)&(bg_>0.88)&(R>185)&(xx>=40)&(xx<80)&(yy>=35)&(yy<66)&(k==2)]=4
    oog=(xx-OOG[0])**2+(yy-OOG[1])**2<=OOGR**2
    k[oog&(k!=1)&(L>=105)]=6
    k[oog&(k!=1)&(k!=6)&(L<105)]=7
    k[oog&(k==4)]=4
    return k,L
if __name__=='__main__':
    a=np.asarray(Image.open('natief.png').convert('RGB'))
    k,L=klassen(a)
    col=np.array([[255,255,255],[0,0,0],[180,60,60],[240,200,0],[255,140,200],[120,200,120],[0,120,255],[0,0,140]],'uint8')
    Image.fromarray(col[k]).resize((796,796),Image.NEAREST).save('klassen.png')
