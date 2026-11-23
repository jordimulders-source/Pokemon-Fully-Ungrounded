# kaart.py: licht/midden/schaduw-kaart per pixel (geel = licht/hooglicht, grijs = midden, blauw = schaduw, donker = lijn)
import numpy as np; from PIL import Image
KL={'L':(45,40,55),'S':(70,95,185),'M':(175,175,170),'H':(250,232,120)}
def baardmasker():
    m=np.zeros((64,64),bool)
    m[13:19,11:18]=True        # plukje links
    m[15:22,32:41]=True        # haar rechts
    m[21:37,15:32]=True        # baard
    m[36:,15:21]=False         # riemuiteinde links
    return m
def niveaus_gnome(a):
    b=baardmasker(); N=np.full(a.shape,'',object)
    for y in range(64):
        for x in range(64):
            v=int(a[y,x])
            if v==0: continue
            if v==1: N[y,x]='L'; continue
            if v in (2,6,9): N[y,x]='L'
            elif v in (7,10,3): N[y,x]='S'
            elif v in (8,11): N[y,x]='M'
            elif v in (15,12,14): N[y,x]='H'
            elif v==13: N[y,x]='M'
            elif v==4: N[y,x]='L' if b[y,x] else 'M'
            elif v==5: N[y,x]='S' if b[y,x] else 'H'
    return N
def niveaus_gnomad(a):
    T={1:'L',2:'L',3:'S',4:'M',5:'H',6:'L',7:'S',8:'M',9:'L',10:'S',11:'M',12:'S',13:'H',14:'M',15:'L'}
    N=np.full(a.shape,'',object)
    for y in range(64):
        for x in range(64):
            v=int(a[y,x])
            if v: N[y,x]=T[v]
    return N
def beeld(N,bg=(255,255,255)):
    im=np.zeros((64,64,3),np.uint8); im[:]=bg
    for y in range(64):
        for x in range(64):
            if N[y,x]: im[y,x]=KL[N[y,x]]
    return Image.fromarray(im)
