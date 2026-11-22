# r3.py: r2-A -> r3 (riem op de Machoke-manier). Zwarte lijn direct boven en onder de band, band zelf vlak donkerbruin (15),
# 1 klein hooglichtstukje links op de bovenste bandrij (14, lichtkant). A: + gesp in het midden (creme 12, glans 13, zwarte omlijning). B: zonder gesp.
# Verder diff 0 t.o.v. r2-A (assert).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); from gemeen import opslaan
R1='../sprite_r1/'
zone=np.load(R1+'zone_af.npy'); L=np.load(R1+'lijn.npy'); riem1=np.load(R1+'riem.npy')
zone[43,26]=5; L[43,26]=False
def top(X): u=(X-25.0)/14.0; return 40.6+3.4*(1-u*u)+0.8*u
body=(np.isin(zone,(5,8))|riem1)&~L
im=Image.open('../sprite_r2/gnomad_A.png'); pal=[tuple(im.getpalette()[3*k:3*k+3]) for k in range(16)]
r2=np.asarray(im).astype(int)
def bouw(gesp):
    o=r2.copy(); riem=np.zeros((64,64),bool)
    for Y,X in zip(*np.where(body)):
        t=int(round(top(X))); u=(X-25)/14; dik=5 if abs(u)<0.55 else 4     # incl. de zwarte lijn boven en onder
        if t<=Y<t+dik:
            riem[Y,X]=True
            if Y==t or Y==t+dik-1: o[Y,X]=1
            elif Y==t+1 and 15<=X<=21: o[Y,X]=14
            else: o[Y,X]=15
        elif Y==t+dik:
            o[Y,X]=10 if X<30 else 9            # broek direct onder de riem in schaduw (zoals r2)
    if gesp:
        t=int(round(top(25)))                   # midden van de band, laagste punt van de boog
        for y in range(t,t+5):
            for x in range(23,28):
                rand=(x in (23,27)) or y in (t,t+4)
                o[y,x]=1 if rand else 12
        o[t+1,24]=13                            # glanspixel linksboven
    d=o!=r2; zm=riem|np.isin(zone,(5,8))|riem1
    assert not (d&~zm).any()
    return o,d.sum()
for var,g in (('A',True),('B',False)):
    o,n=bouw(g); opslaan(o,'gnomad_%s.png'%var,pal); print(var,'diff t.o.v. r2-A:',n,'px (alleen riem/broekrand), elders 0')
