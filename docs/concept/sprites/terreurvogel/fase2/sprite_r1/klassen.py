# Kleurgroep per natieve modelpixel: 0 bg, 1 zwart, 2 lijf, 3 snavel, 4 gezicht, 5 poten, 6 oog
import numpy as np; from PIL import Image
def klassen(a):
    a=a.astype(float); R,G,B=a[...,0],a[...,1],a[...,2]
    L=0.299*R+0.587*G+0.114*B; mx=a.max(2); mn=a.min(2); sat=(mx-mn)/np.maximum(mx,1)
    k=np.full(R.shape,2)
    k[mn>=225]=0
    k[(L<48)&(k!=0)]=1
    gr=G/np.maximum(R,1); bg_=B/np.maximum(G,1)
    snav=(gr>0.70)&(sat>0.38)&(k==2)
    poot=(gr>0.68)&(sat<=0.38)&(k==2)
    gez=(gr>0.50)&(bg_>0.88)&(R>185)&(k==2)
    k[snav]=3; k[poot]=5; k[gez]=4
    return k,L
if __name__=='__main__':
    a=np.asarray(Image.open('natief.png').convert('RGB'))
    k,L=klassen(a)
    col=np.array([[255,255,255],[0,0,0],[180,60,60],[240,200,0],[255,140,200],[120,200,120],[0,120,255]],'uint8')
    Image.fromarray(col[k]).resize((796,796),Image.NEAREST).save('klassen.png')
