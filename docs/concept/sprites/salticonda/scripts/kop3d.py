"""Onderlaag voor de 3/4-kop: afgeplatte ei-vorm (brede, platte anacondakop) die naar links-voor kijkt,
met dezelfde projectie als onderlaag2. Geeft toon per pixel + schermposities van oog, neusgat, mondlijn.
Alleen onderlaag; het eindraster wordt met de hand getekend."""
import math
import onderlaag2 as O
def head(cx=24.0, cy=4.0, cz=44.0, yaw=38, pitch=-12, Lh=15.5, W=10.5, Hh=7.0):
    a=math.radians(yaw); p=math.radians(pitch)
    f=(-math.cos(a)*math.cos(p), math.sin(a)*math.cos(p), math.sin(p))     # snuitrichting
    s=(math.sin(a), math.cos(a), 0.0)                                       # naar de kijker-kant
    up=(f[1]*s[2]-f[2]*s[1], f[2]*s[0]-f[0]*s[2], f[0]*s[1]-f[1]*s[0])
    if up[2]<0: up=tuple(-v for v in up)
    def P(u,v,w):
        return (cx+u*f[0]+v*s[0]+w*up[0], cy+u*f[1]+v*s[1]+w*up[1], cz+u*f[2]+v*s[2]+w*up[2])
    zb={}
    N=260
    for i in range(N+1):
        th=math.pi*i/N            # langs de snuit
        for j in range(N):
            ph=2*math.pi*j/N
            uu=math.cos(th)       # +1 = snuitpunt
            r=math.sin(th)
            wf=1-0.18*max(0,uu)   # snuit iets smaller
            hf=1-0.30*max(0,uu)   # en lager
            v=W*r*math.cos(ph)*wf; w=Hh*r*math.sin(ph)*hf
            if w<-Hh*0.55: w=-Hh*0.55 - (w+Hh*0.55)*0.25   # kaak plat van onder
            u=Lh*uu
            X,Y,Z=P(u,v,w)
            # normaal ~ gradient van ellipsoide
            g=(uu/Lh, r*math.cos(ph)/(W*wf), r*math.sin(ph)/(Hh*hf))
            n=[g[0]*f[k]+g[1]*s[k]+g[2]*up[k] for k in range(3)]
            nn=math.sqrt(sum(q*q for q in n)); n=[q/nn for q in n]
            sx,sy,dep=O.proj(X,Y,Z)
            k=(int(sx*O.SS),int(sy*O.SS))
            if k not in zb or zb[k][0]<dep: zb[k]=(dep,sum(n[q]*O.L[q] for q in range(3)),u/Lh,v/W,w/Hh)
    px={}
    for x in range(64):
        for y in range(64):
            k=(x*O.SS+O.SS//2,y*O.SS+O.SS//2)
            if k in zb: px[(x,y)]=zb[k]
    pts={}
    def sp(u,v,w): X,Y,Z=P(u*Lh,v*W,w*Hh); sx,sy,_=O.proj(X,Y,Z); return (round(sx,1),round(sy,1))
    pts['oog']=sp(0.30,0.62,0.55); pts['oog_ver']=sp(0.30,-0.62,0.55)
    pts['neus']=sp(0.92,0.25,0.20); pts['neus_ver']=sp(0.92,-0.25,0.20)
    pts['mond']=[sp(u,0.85*math.sqrt(max(0,1-u*u)),-0.25) for u in (0.98,0.8,0.5,0.2,-0.1,-0.35)]
    return px,pts
