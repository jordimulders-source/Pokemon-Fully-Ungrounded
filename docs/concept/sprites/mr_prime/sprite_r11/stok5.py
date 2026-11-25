# r5 stok: vorm + inkleuring. Alleen modelpixels (r9 natief, na stok.py verbreed), geschaald door natieve rijen/kolommen
# te dupliceren (nearest), verschoven langs de stokas; in de sprite alleen tinten op stokpixels.
import numpy as np; from PIL import Image
FX=2.0; FY=1.75      # handvat (crook) vergroting: natieve rijen/kolommen gedupliceerd (nearest)
T=12        # crook T natieve rijen langs de stokas omlaag (anders valt hij links buiten beeld); schacht erboven vervalt
A=(16.5,57.0)   # aanhechting crook -> schacht (natief x,y; midden van de onderrand van de boog)
def as_x(y): return int(round(15+0.73*(y-56)))+3
def natief_masker():
    a=np.asarray(Image.open('natief_stok.png').convert('L')).astype(int); H,W=a.shape
    D=a<170; m=np.zeros_like(D)
    for y in range(58,126):           # schacht: donkere run rond de as (zoals stok.py)
        c=as_x(y)
        if not D[y,c]:
            cs=[x for x in range(c-4,c+5) if D[y,x]]
            if not cs: continue
            c=cs[len(cs)//2]
        xl=c
        while D[y,xl-1]: xl-=1
        xr=c
        while D[y,xr+1]: xr+=1
        if xr-xl<=12: m[y,xl:xr+1]=1
    from bgmask import bgmask
    fig=~bgmask(np.asarray(Image.open('natief.png').convert('RGB')))   # onverbreed model; binnen de omlijning (ook het witte glimlicht)
    crook=np.zeros_like(D); crook[49:58,6:25]=fig[49:58,6:25]; crook[58:64,6:14]=fig[58:64,6:14]   # boog + neergaand been, zonder schacht
    # alleen de samenhangende crook (vanaf (12,52))
    from collections import deque
    k=np.zeros_like(D); q=deque([(53,10)]); k[53,10]=1
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
            v,u=y+dy,x+dx
            if crook[v,u] and not k[v,u]: k[v,u]=1; q.append((v,u))
    Ax,Ay=A; By=Ay+T; r=np.where(m[int(By)])[0]; Bx=(r.min()+r.max())/2
    out=np.zeros_like(D); glans=np.zeros_like(D)
    L0=np.asarray(Image.open('natief.png').convert('L')).astype(int)
    out[int(By):,:]=m[int(By):,:]          # schacht alleen onder de nieuwe aanhechting
    for y in range(0,H):
        for x in range(0,W):
            sx=int(np.floor(Ax+(x-Bx)/FX+0.5)); sy=int(np.floor(Ay+(y-By)/FY+0.5))
            if 0<=sy<H and 0<=sx<W and k[sy,sx]:
                out[y,x]=1
                if L0[sy,sx]>=170: glans[y,x]=1     # wit glimlicht van de modelcrook
    return out, glans
def sprite_masker(thr=0.45,met_glans=False):
    m,g=natief_masker(); up=np.repeat(np.repeat(m.astype(float),2,0),2,1); ug=np.repeat(np.repeat(g.astype(float),2,0),2,1)
    S=np.zeros((64,64),bool); Gl=np.zeros((64,64),bool)
    for r in range(64):
        for c in range(64):
            y0=int(2*(17.5+2.5*r)); x0=int(2*(7+2.5*c))
            blk=up[y0:y0+5,x0:x0+5]
            if blk.size and blk.mean()>=thr: S[r,c]=1
            if blk.size and ug[y0:y0+5,x0:x0+5].mean()>=0.25: Gl[r,c]=1
    return (S,Gl) if met_glans else S
if __name__=='__main__':
    import sys
    FX=float(sys.argv[1]); FY=float(sys.argv[2]); T=int(sys.argv[3])
    S=sprite_masker()
    for y in range(6,48): print('%2d '%y+''.join('#' if S[y,x] else '.' for x in range(0,26)))

# tonen (indexen in de r5-palet): 0 lijn, 1 schaduw, 2 basis, 3 licht, 5 glans
TL=dict(lijn=0,schaduw=1,basis=2,licht=3,glans=5)
def toepassen(C,log,thr=0.45,glans=True):
    """Oude stok boven de hand weg (rij<=25, x<16), nieuwe vorm uit sprite_masker; over de hand (rij 26-33) blijft de
    r4-uitsnede (stok binnen 1,5 px van de as); dan alleen tinten per stokpixel."""
    C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    S,Gl=sprite_masker(thr,True)
    for y in range(0,26):
        for x in range(0,16):
            if C[y,x]!=-1 and not S[y,x]: zet(y,x,-1,'oude handvat/schacht weg')
    for y in range(26,34):
        ax=12.5+0.75*(y-27)
        for x in range(0,26):
            S[y,x]= abs(x-ax)<=1.5 and 0<=C[y,x]<=3
    ins=lambda y,x: 0<=y<64 and 0<=x<64 and S[y,x]
    crook=lambda y,x: y<=23 or (y==24 and x<6)
    for y in range(64):
        for x in range(64):
            if not S[y,x]: continue
            up,dn,le,ri=ins(y-1,x),ins(y+1,x),ins(y,x-1),ins(y,x+1)
            if crook(y,x):      # boog: licht van boven/links, schaduw onder/rechts (normaal per pixel)
                if not (up and dn and le and ri): t=TL['lijn']
                else:
                    up2,dn2=ins(y-2,x),ins(y+2,x); le2,ri2=ins(y,x-2),ins(y,x+2)
                    if not up2: t=TL['licht']
                    elif not dn2: t=TL['schaduw']
                    elif not le2: t=TL['licht']
                    elif not ri2: t=TL['schaduw']
                    else: t=TL['basis']
                if t!=TL['lijn'] and glans and Gl[y,x]: zet(y,x,TL['glans'],'stok: glans crook (wit glimlicht model)'); continue
            else:               # schacht per rij (zoals het model: lijn, schaduw links-onder, licht rechts-boven)
                a=x
                while ins(y,a-1): a-=1
                b=x
                while ins(y,b+1): b+=1
                if x in (a,b) or b-a<2: t=TL['lijn']
                elif b-a==2: t=TL['basis']
                elif x==b-1: t=TL['licht']
                elif x==a+1: t=TL['schaduw']
                else: t=TL['basis']
                if t==TL['licht'] and glans and 34<=y<=37: zet(y,x,TL['glans'],'stok: hooglichtstreepje schacht'); continue
            zet(y,x,t,'stok: tint per stokpixel (vorm uit model)')
    return C, S
