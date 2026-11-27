# r3 stap 8: vruchten als ronde, glanzende bollen (Jordi r2: "hoekig", "geen enkele schaduw").
# Vorm = het model: elke vrucht uit het natieve model (vruchtseg.py: rood vruchtvlees + het oog erin) -> ellips uit de momenten
# (gemiddelde + covariantie, op spriteschaal). Getekend van achter naar voor (geplakte achtertros eerst, daarna de vrucht die in het model
# het meest bedekt is), alleen binnen het trosgebied van r2 (silhouet blijft r2). Elke vrucht: 1 px eigen lijn (lijnrood) waar de
# ellips eindigt, vulling als bol met licht linksboven (hooglicht/licht/midden/schaduw), achtertros een stap donkerder.
import numpy as np
from gemeen2 import *
import vruchtseg as vs, schaduw
LICHT=np.array([-1.0,-1.25,1.1]); LICHT/=np.linalg.norm(LICHT)
DR=[0.08,0.58,0.86]
RAMP={'v':[3,4,5,12],'a':[14,3,4,5]}
LICHTLIJN=int(__import__('os').environ.get('LICHTLIJN','3'))
T2=float(__import__('os').environ.get('ELLIPS_T','6.5'))
def ellipsen():
    E=[]
    for f in vs.VRUCHTEN:
        ys,xs=np.where(vs.VR==f)
        X,Y=naar_sprite(xs+0.5,ys+0.5); P=np.stack([X,Y],1)
        mu=P.mean(0); C=np.cov(P.T)+np.eye(2)*0.05
        area_nat=len(ys)*S*S; ev=np.linalg.eigvalsh(C); area_ell=np.pi*4*np.sqrt(ev[0]*ev[1])
        back=schaduw.BACK[ys,xs].mean()
        E.append(dict(f=f,mu=mu,Ci=np.linalg.inv(C),zicht=area_nat/area_ell,back=back,n=len(ys)))
    E.sort(key=lambda e:(-int(e['back']>0.5),e['zicht']))
    return E
def teken(o,OOG,fg,groep,ZW):
    E=ellipsen()
    TROS=np.zeros((64,64),bool)
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k in (2,3,4,5,12,14) or OOG[Y,X] or (k==1 and groep(Y,X)=='R'): TROS[Y,X]=True
    eig=np.full((64,64),-1); D=np.full((len(E),64,64),99.)
    yy,xx=np.mgrid[0:64,0:64]; P=np.stack([xx+0.5,yy+0.5],-1)
    for i,e in enumerate(E):
        d=P-e['mu']; D[i]=np.einsum('...i,ij,...j->...',d,e['Ci'],d)
        eig[(D[i]<=T2)&TROS]=i
    n=o.copy(); GAT=[0]
    def bg(Y,X,dy,dx): return not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx]
    for Y,X in zip(*np.where(TROS)):
        i=eig[Y,X]
        rand=[(dy,dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if bg(Y,X,dy,dx)]
        if rand:   # buitenrand: lijn (zwart aan de schaduwkant)
            n[Y,X]=1 if any(d in ((1,0),(0,1)) for d in rand) else 2; continue
        if i<0: n[Y,X]=14; GAT[0]+=1; continue
        # eigen lijn: een buur ligt buiten de eigen ellips (en is niet van een vrucht die ervóór ligt -> dan is het diens lijn)
        lijn=[]
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            j=eig[Y+dy,X+dx]
            if D[i,Y+dy,X+dx]>T2 and not (j>i): lijn.append((dy,dx))
        if lijn:   # schaduwkant (buiten ligt rechts/onder) = lijnrood, lichtkant = diep rood (outline highlight, DC-gids)
            n[Y,X]=2 if any(d in ((1,0),(0,1)) for d in lijn) else LICHTLIJN; continue
        e=E[i]; d=np.array([X+0.5,Y+0.5])-e['mu']
        # bolnormaal: punt in eenheidscirkel via de ellips (Ci/4), richting op het scherm = d genormeerd met dezelfde vorm
        r2=d@e['Ci']@d/T2; g=e['Ci']@d; g=g/(np.linalg.norm(g)+1e-9)*np.sqrt(min(r2,1))
        nv=np.array([g[0],g[1],np.sqrt(max(0.05,1-min(r2,1)))]); nv/=np.linalg.norm(nv)
        t=nv@LICHT; ramp=RAMP['a' if e['back']>0.5 else 'v']
        n[Y,X]=ramp[int(np.searchsorted(DR,t))]
    print('vrucht: gaten',GAT[0]); return n
