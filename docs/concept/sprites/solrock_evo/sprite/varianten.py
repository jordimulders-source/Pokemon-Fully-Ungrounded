# Jordi's toegestane afwijking (bovenlaag): breuk in de plaat tussen de ogen.
# A = linkerdeel van de plaat blijft (linkeroog op de plaat, rechteroog op de kern); B = andersom.
# Breuklijn = de barsten die het model al in de plaat heeft: barst van de bovenpiek schuin naar links-onder (24,28)->(22,31),
# langs de neusrug (x 22) en de onderste barst schuin naar rechts-onder (22,37)->(25,39)->(25,42).
# Per rij: eerste kolom van het rechterdeel.
import numpy as np; from npy2png import save
o=np.load('basis.npy')
XB={**{r:24 for r in range(18,29)},29:23,30:23,31:22,32:22,33:22,34:22,35:22,36:22,37:23,38:24,
    **{r:25 for r in range(39,47)}}
PLAAT=[7,8,9,10]
# plaatzone: alle plaatpixels + de oogkassen (rood en het zwart dat aan rood grenst)
zone=np.isin(o,PLAAT+[11,12])
def oog(o,x0,x1):
    m=np.zeros_like(o,bool)
    for j in range(30,40):
        for i in range(x0,x1):
            if o[j,i] in (11,12): m[j,i]=True
    # zwart van de oogkas: K die aan rood grenst (8-buren)
    k=np.zeros_like(m)
    for j,i in zip(*np.where(m)):
        for dj in (-1,0,1):
            for di in (-1,0,1):
                if o[j+dj,i+di]==1: k[j+dj,i+di]=True
    return m|k
oogL=oog(o,15,22); oogR=oog(o,25,33)
def maak(houd_links):
    v=o.copy(); n_weg=0
    for j in range(64):
        for i in range(64):
            if o[j,i] in PLAAT and j in XB:
                rechts=i>=XB[j]
                if rechts==houd_links:   # dit deel breekt af
                    v[j,i]=3; n_weg+=1     # kern zichtbaar: middengrijs van de kern rond de plaat
    # breukrand: kernpixel (nieuw) dat aan de overgebleven plaat grenst -> zwart (plaatrand zoals elders in het model)
    nieuw=(v==3)&(o!=3)
    rand=np.zeros_like(nieuw)
    for j,i in zip(*np.where(nieuw)):
        nb=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
        if any(v[y,x] in PLAAT for y,x in nb): rand[j,i]=True
    v[rand]=1
    return v,n_weg,int(rand.sum())
A,na,ra=maak(True); B,nb_,rb=maak(False)
np.save('A_ruw.npy',A); np.save('B_ruw.npy',B)
print('A: plaat weg',na,'breukrand',ra,' B: plaat weg',nb_,'breukrand',rb)
save(A,'A_ruw.png'); save(B,'B_ruw.png')
