# Lijnen overnemen uit het natieve raster (niets tekenen): elke natieve lijncel (1 cel = 0,4 spritepx) wordt op zijn
# middelpunt naar de spritepixel afgebeeld. Zo blijven de modellijnen 1 px dun, doorlopend (8-samenhangend) en op hun plek.
# soorten: 'sneeuw' (donkere vachtlijnen, L<140), 'K' (zwarte binnenlijnen), 'hand' (donkere handlijnen L<105),
#          'gloed' (scheuren/rand in de stenen), 'geel' (hete kern van de scheuren)
import os, sys, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *; from klassen import klassen, label as nlabel
def lijnkaarten(minlen=3):
    a,c,L=klassen(); H,W=c.shape
    from klassen import dil
    buiten=dil(c==0,1)
    m={'sneeuw':(c==2)&(L<140),'K':(c==1)&~buiten,'hand':(c==8)&(L<105),'gloed':(c==6)|(c==7),'geel':(c==7)}
    out={}
    for k,mask in m.items():
        if k in ('sneeuw','hand'):
            lab,n=nlabel(mask)
            for i in range(1,n+1):
                if (lab==i).sum()<minlen: mask=mask&(lab!=i)
        hits=np.zeros((64,64),int)
        for y,x in zip(*np.where(mask)):
            X=int(np.floor((x+0.5-MX0)/F)); Y=int(np.floor((y+0.5-MY0)/F))
            if 0<=X<64 and 0<=Y<64: hits[Y,X]+=1
        out[k]=hits
    return out
