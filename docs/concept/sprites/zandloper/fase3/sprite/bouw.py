# Bouwt varianten van de zand-djinn: alles uit r5/r8/r10 verkleind, alleen weghalen/verschuiven/tinten kiezen.
import numpy as np; from PIL import Image; import bewerk, reduceer, reduceer2, kleur, schoon, lijnweg, materiaal as mt
KL=kleur.modelkleuren(bewerk.R5)
# glastinten = alleen het glas van de zandloper in r5 (lichtblauw), ook voor boeien (Jordi: "Boeien lichtblauw prima")
def glaskleuren():
    a=bewerk.R5; hr=np.zeros(a.shape[:2],bool); hr[150:,:]=True
    M,L=mt.kaart(a,hr); b=np.searchsorted(kleur.GLAS,L); zone=np.zeros_like(hr); zone[150:,:]=True
    for t in range(4):
        sel=(M==3)&(b==t)&zone
        if sel.sum(): KL[20+t]=tuple(np.median(a[sel],axis=0).astype(int))
glaskleuren()
Z_HOOFD=np.zeros((201,201),bool)
for y,(l,r) in bewerk.HOOFD.items(): Z_HOOFD[y,l:r+1]=True
Z_LIJF=np.zeros((201,201),bool); Z_LIJF[47:150,30:160]=True; Z_LIJF&=~Z_HOOFD
def natief(brein='B',fles=(-8,-14),trechter=(0,-8),spier=12,hoofd_min=20):
    a=bewerk.maak(fles,trechter)
    if brein=='A': a=bewerk.brein_r8(a)
    else: a=lijnweg.weg(a,Z_HOOFD,hoofd_min,drempel=125)
    if spier: a=lijnweg.weg(a,Z_LIJF,spier,drempel=100)
    return a
def basis(**kw):
    a=natief(**kw)
    return reduceer2.reduceer(a,(2,2),lijn_k=kw.get('lijn_k',2) if False else 2)[2:66,0:64].copy()
def buitenlijn(lab):
    """Randpixels van het silhouet krijgen de lijnkleur. Gladde normaal (5x5) wijst naar linksboven -> selout
    (donkerste eigen tint), anders zwart; zo geen zwart/selout om en om op een trap."""
    H,W=lab.shape; out=lab.copy(); leeg=(lab==0)
    for y in range(H):
        for x in range(W):
            if lab[y,x]==0 or lab[y,x]==2: continue
            if not any(not(0<=y+dy<H and 0<=x+dx<W) or leeg[y+dy,x+dx] for dy,dx in schoon.N4): continue
            if lab[y,x]==1: continue
            ny=nx=0
            for dy in range(-2,3):
                for dx in range(-2,3):
                    Y,X=y+dy,x+dx
                    if not(0<=Y<H and 0<=X<W) or leeg[Y,X]: ny+=dy; nx+=dx
            n=(ny*ny+nx*nx)**0.5 or 1
            if (-ny-nx)/n/1.414>0.55: out[y,x]=(lab[y,x]//10)*10
            else: out[y,x]=1
    return out
def binnenlijnen(lab):
    """Lijnpixels binnen het silhouet: donkerste tint van het omringende materiaal (geen zwart)."""
    H,W=lab.shape; out=lab.copy()
    for y in range(H):
        for x in range(W):
            if lab[y,x]!=1: continue
            if any(not(0<=y+dy<H and 0<=x+dx<W) or lab[y+dy,x+dx]==0 for dy,dx in schoon.N4): continue
            c={}
            for dy,dx in schoon.N8:
                v=lab[y+dy,x+dx]
                if v>=10: c[v//10]=c.get(v//10,0)+1
            if c: out[y,x]=max(c,key=c.get)*10
    return out
