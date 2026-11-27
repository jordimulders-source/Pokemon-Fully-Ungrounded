# Gedeeld: palet, klassificatie van het model, opslaan, vel.
import os
from PIL import Image; import numpy as np
from scipy import ndimage as nd
PAL=[(0,0,0),(24,16,12),(96,58,24),(164,112,52),(204,156,70),(232,190,98),(252,226,150),
     (56,84,110),(114,160,186),(170,212,230),(222,244,250),(112,64,34),(154,100,58),(196,146,94),(248,248,248),(192,192,200)]
NAAM=['tr','zwart','zand-lijn','zand-donker','zand-midden','zand-licht','zand-glans','glas-lijn','glas-donker','glas-midden','glas-licht','kap-donker','kap-midden','kap-licht','wit','oog-grijs']
# modelkleur -> klasse (gemeten met kmeans.py op natief.png en handzooms)
REF=[(1,(5,3,2)),(1,(44,26,15)),(1,(72,42,22)),(7,(47,71,91)),(7,(73,102,125)),(8,(96,130,147)),(8,(107,148,165)),(9,(164,189,198)),
     (9,(182,219,232)),(10,(213,240,251)),(10,(229,246,251)),(11,(113,65,34)),(11,(128,80,45)),(12,(152,99,57)),(12,(168,110,66)),
     (13,(198,148,96)),(13,(190,135,85)),(3,(190,144,64)),(3,(161,143,99)),(2,(140,95,45)),(4,(228,183,91)),(5,(248,217,136)),(6,(253,236,175)),(14,(255,255,255)),(14,(235,235,235)),(9,(180,180,180))]
def klasse(rgb):
    a=rgb.astype(float); R=np.array([c for _,c in REF],float); K=np.array([k for k,_ in REF])
    d=((a[...,None,:]-R)**2).sum(-1); return K[d.argmin(-1)]
def model():
    return np.asarray(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../model.png')).convert('RGB'))
def achtergrond(rgb):
    w=(rgb.min(axis=2)>238)
    lab,n=nd.label(w); rand=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    return np.isin(lab,list(rand))
def opslaan(idx,pad):
    im=Image.fromarray(idx.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    im.putpalette(p+[0]*(768-len(p))); im.save(pad,transparency=0); return im
def rgba(idx,bg=None):
    a=np.array([PAL[i] for i in range(16)],'uint8')[idx]
    al=np.where(idx==0,0,255).astype('uint8'); im=Image.fromarray(np.dstack([a,al]),'RGBA')
    if bg is not None:
        b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b
    return im
def klassen_model(rgb):
    bg=achtergrond(rgb); k=klasse(rgb); k[bg]=0
    # kap-tinten buiten de zandloper (onder y=630) = zandlijnen/-schaduw
    boven=np.zeros(k.shape,bool); boven[:630]=True
    k[boven&(k==11)]=2; k[boven&np.isin(k,[12,13])]=3
    return k,bg
# geometrie: model-px <-> sprite-px (gezet door r1_reductie: T, cx, cy, ox, oy)
import json, os
def geo():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'geo.json')))
def m2s(x,y):
    g=geo(); return ((x-g['cx'])/g['T']+g['ox'], (y-g['cy'])/g['T']+g['oy'])
def s2m(i,j):
    g=geo(); return ((i-g['ox'])*g['T']+g['cx'], (j-g['oy'])*g['T']+g['cy'])
NP,NPH=10.24,9.25
def n2m(n): return NPH%NP+n*NP   # linkerrand natieve cel n in model-px
def natief_klassen():
    """Klasse per natieve cel (pitch 10.24): meerderheid van klassen_model in het celmidden."""
    k,bg=klassen_model(model()); n=99; out=np.zeros((n,n),int)
    for j in range(n):
        for i in range(n):
            x=int(n2m(i)+NP/2); y=int(n2m(j)+NP/2)
            b=k[max(0,y-2):y+3,max(0,x-2):x+3].ravel(); out[j,i]=np.bincount(b,minlength=16).argmax()
    return out
CH='.KdDmlgOBMLckCWo'
