# r7 natief (100x100): armen/handen, rughaar en okselhaar weg (Jordi 27 nov). Alleen weghalen + gat dichten met lijfkleur + omlijning.
import numpy as np
from PIL import Image
a=np.array(Image.open('natief.png')).astype(int)
W=np.array([255,255,255]); s=a.sum(2)
wit=s>700; zwart=s<120
lijf=np.median(a[(s>120)&(s<200)&(np.abs(a[...,0]-a[...,2])<20)][:,:],0).astype(int)
gewijzigd=np.zeros(wit.shape,bool)
def zet(y,x,c): a[y,x]=c; gewijzigd[y,x]=True
# 1. rughaar: rijen 17-34, vanaf x=50 naar rechts tot de eerste witte pixel, daarna alles wit
for y in range(17,35):
    x=50
    while x<100 and not wit[y,x]: x+=1
    for xx in range(x,100):
        if not wit[y,xx]: zet(y,xx,W)
# 2. linkerarm + okselhaar: rijen 36-48 links van lijn (34,36)->(40,48); rijen 48-66 x<40
for y in range(36,67):
    e = 34+(y-36)*6/12 if y<=48 else 40
    for x in range(0,100):
        if x<e:
            if not wit[y,x]: zet(y,x,W)
        elif x<e+8 and y<=48 and (wit[y,x] or a[y,x].sum()>330 or zwart[y,x]):
            zet(y,x,lijf)  # okselgat dichten met lijfkleur
# 3. rechterarm/hand: grijs over het lijf (rijen 35-41, x 49-74) -> lijfkleur
for y in range(35,42):
    for x in range(49,75):
        if not wit[y,x]: zet(y,x,lijf)
#    rechterrand: rijen 33-57 rechts van lijn (66,33)->(60,57) wit; rijen 54-61 x>=66 wit (klauwen naast de poot)
for y in range(33,62):
    e = 66+(y-33)*(60-66)/24 if y<=57 else 66
    for x in range(int(round(e))+1,100):
        if y>=58 and x<66: continue
        if not wit[y,x]: zet(y,x,W)
# 4. omlijning op de nieuwe randen
s2=a.sum(2); w2=s2>700
for y in range(1,99):
    for x in range(1,99):
        if w2[y,x]: continue
        nb=w2[y-1,x] or w2[y+1,x] or w2[y,x-1] or w2[y,x+1]
        near=gewijzigd[max(0,y-1):y+2,max(0,x-1):x+2].any()
        if nb and near and s2[y,x]>=120: a[y,x]=[16,16,16]
a[a.sum(2)>600]=255
out=a.astype(np.uint8)
Image.fromarray(out).save('basis_natief.png')
Image.fromarray(out).resize((1000,1000),Image.NEAREST).save('krabbelbasis_r7.png')
vs=np.concatenate([np.array(Image.open('natief.png')),out],1)
Image.fromarray(vs).resize((1600,800),Image.NEAREST).save('voor_na.png')
