# Gedeelde hulpjes: model laden, achtergrond, Lab-afstand, palet.
from PIL import Image; import numpy as np, os, sys
D=os.path.dirname(os.path.abspath(__file__))+'/'
M=D+'../model/'
sys.path.insert(0,M)
def model():
    return np.asarray(Image.open(M+'model_64_geschrapt.png').convert('RGB')).astype(float)
def achtergrond(a):
    from seg import label
    wit=a.min(2)>=232; l2,n=label(wit)
    rand=set(l2[0,:])|set(l2[-1,:])|set(l2[:,0])|set(l2[:,-1]); rand.discard(0)
    return np.isin(l2,list(rand))
def lab(rgb):
    c=np.asarray(rgb,float)/255
    c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    X=c@np.array([[0.4124,0.2126,0.0193],[0.3576,0.7152,0.1192],[0.1805,0.0722,0.9505]])
    X=X/np.array([0.9505,1,1.089])
    f=np.where(X>0.008856,np.cbrt(X),7.787*X+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
def dichtst(a,pal):
    A=lab(a); P=lab(np.array(pal))
    d=((A[...,None,:]-P)**2).sum(-1); return d.argmin(-1), np.sqrt(d.min(-1))
