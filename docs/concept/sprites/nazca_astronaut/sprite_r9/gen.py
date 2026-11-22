# r9 generator: tunica-patroon ("unku") op romp + dijen, band op de bovenarmen. Rollen -> materiaalraster.
# Stap 1 (dit script): materiaalraster per pixel: stuk (romp/LL/RL/LA/RA), tint (0 licht,1 midden,2 schaduw),
# patroonmateriaal (g grond, a accent, l lijn). Stap 2 (variant.py): palet per variant + handreparaties.
import numpy as np
from basis import r9_basis
B=r9_basis(); H,W=B.shape
TUN=set('123gWGH')
tun=np.zeros((H,W),bool)
for y in range(26,48):
    for x in range(W):
        if B[y,x] in TUN: tun[y,x]=True
tun[29,29]=True                         # losse binnenlijnpixel bij de armaanzet wordt vlak
stuk=np.full((H,W),'',dtype='<U2')
for y in range(H):
    for x in range(W):
        if not tun[y,x]: continue
        if y<=30 and (x<=28 or (y<=27 and x<=29)) and x<30: stuk[y,x]='LA'
        elif 31<=y<=36 and x>=37 and not (y>=34 and x<=37): stuk[y,x]='RA'
        elif y>=34 and x<=31: stuk[y,x]='LL'
        elif y>=34: stuk[y,x]='RL'
        else: stuk[y,x]='RO'
tint=np.ones((H,W),int)
for y in range(H):
    for x in range(W):
        s=stuk[y,x]
        if not s: continue
        if s=='LA':
            col=[j for j in range(H) if stuk[j,x]=='LA']
            tint[y,x]=0 if y==min(col) else (2 if (y==max(col) and len(col)>=3) else 1)
        else:
            row=[i for i in range(W) if stuk[y,i]==s]; a,b=min(row),max(row); w=b-a+1
            if s=='RA': tint[y,x]=1 if x==a else 2
            elif s=='RO':
                rel=(x-a)/max(w-1,1)
                tint[y,x]=0 if rel<0.42 else (2 if rel>0.8 else 1)
            else:
                tint[y,x]=0 if x==a else (2 if x==b else 1)
# romp: bovenste rij (schouders) licht tot het midden, onderste rij (heup) schaduw rechts
for x in range(W):
    if stuk[26,x]=='RO' and x<=33: tint[26,x]=0
def tri(x,per=6,top=29):     # 0 boven de spleet (x32), max op dijmiddens (x29, x35)
    h=per//2; return abs(((x-top)%per)-h)
def patroon(soort, banden, dik=2):
    """soort 'trap' = 4-verbonden getrapte lijnen, 'schuin' = 1-px diagonale lijnen (r8-stijl).
    banden: lijst y0. Per kolom: lijn op y0+z-1, accent y0+z .. y0+z+dik-1, lijn op y0+z+dik."""
    M=np.full((H,W),'',dtype='<U1')
    for y in range(H):
        for x in range(W):
            s=stuk[y,x]
            if not s: continue
            M[y,x]='g'
            if s in ('LA','RA'): continue
            z=3-tri(x)
            for y0 in banden:
                t=y-(y0+z)
                if 0<=t<dik: M[y,x]='a'
                elif t==-1 or t==dik: M[y,x]='l'
                elif soort=='trap':
                    # trapje: lijnpixel ook op de rij van de buurkolom zodat de lijn 4-verbonden is
                    for nx in (x-1,x+1):
                        if stuk[y,nx] in ('RO','LL','RL'):
                            zn=3-tri(nx)
                            if zn<z and (t==-2 and y-(y0+zn)==-1): M[y,x]='l'
                            if zn>z and (t==dik+1 and y-(y0+zn)==dik): M[y,x]='l'
    return M
