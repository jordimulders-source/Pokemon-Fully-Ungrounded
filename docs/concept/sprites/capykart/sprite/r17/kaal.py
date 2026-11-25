# Kale reductie Capykart r17: oppervlakteweging per spritepixel over het natieve raster van model_r5.
# zwart wint vanaf 30 %; anders de klasse met het grootste oppervlak; tint uit het model:
#  bruin: drempels op de gemiddelde modelhelderheid (clusters 69/85 | 107 | 125 | 146 | 162 -> grenzen 96/116/136/154)
#  hoepel: L<110 donker; toren (blokken/dak): gemiddelde modelkleur -> dichtstbijzijnde modeltoon van dat blok.
import sys, numpy as np
sys.path.insert(0,'sprite/r17'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
# torenklassen per natieve pixel (alleen toren-gebied x>=62, y<=48): op tint, niet op positie getekend
T=np.zeros(c.shape,bool); T[10:49,62:81]=True
R_,G_,B_=a[...,0],a[...,1],a[...,2]
fgm=(a.min(2)<225)&(c!=1)&(c!=3)   # hoepelgrijs hoort niet bij de toren
rows=np.arange(99)[:,None]+0*np.arange(99)[None]
tc=np.zeros(c.shape,int)   # 0 niet-toren | 4 geel-blok | 5 rood | 6 blauw | 7 groen
tc[T&fgm&(G_>R_)&(G_>B_)]=7
tc[T&fgm&(B_>R_+15)&(tc==0)]=6
tc[T&fgm&(R_-G_>80)&(tc==0)&(rows<=40)]=5   # rood blok loopt in het model tot rij 40; daaronder is oranje hout
tc[T&fgm&(tc==0)&(rows<=29)]=4   # geel vlak + bruine zijkant + olijfranden onder het dak tot de rode rand
tc[T&fgm&(tc==0)&(rows<=40)]=5   # restjes (bruine schaduw onder geel op rode bovenkant) -> rood-blok
cls=c.copy(); tm=T&fgm&(tc>0); cls[tm]=tc[tm]; cls[T&fgm&(tc==0)]=2
cls[(c==5)&~T]=2      # oranje vacht die als 'rood' telde buiten de toren = bruin
cls[c==8]=2           # oogglans (1 px) telt als bruin; oog komt uit de bovenlaag
# toontabellen (modeltonen -> paletindex)
TONEN={4:[((240,208,84),9),((195,132,86),5),((154,117,32),2),((104,72,22),2)],
       5:[((246,99,90),10),((205,61,65),11),((155,39,49),11),((104,74,24),2)],
       6:[((122,172,222),12),((87,140,202),13),((76,109,168),14),((51,85,140),14)],
       7:[((123,193,124),15),((92,163,92),15),((74,135,83),16),((51,103,59),16)]}
def tbruin(l): return 2 if l<96 else 3 if l<116 else 4 if l<136 else 5 if l<154 else 6
def reduce():
    o=np.zeros((64,64),int)
    for Y in range(64):
        for X in range(64):
            f=np.zeros(9); rgbs=np.zeros((9,3)); lum=np.zeros(9)
            for u,v,w in overlap(X,Y):
                k=cls[v,u]; f[k]+=w; rgbs[k]+=w*a[v,u]; lum[k]+=w*L[v,u]
            if f[1:].sum()<0.5: continue
            if f[1]>=0.30: o[Y,X]=1; continue
            g=2+int(np.argmax(f[2:]))
            if g==2: o[Y,X]=tbruin(lum[2]/f[2])
            elif g==3: o[Y,X]=8 if lum[3]/f[3]<110 else 7
            else:
                m=rgbs[g]/f[g]; o[Y,X]=min(TONEN[g],key=lambda t:((np.array(t[0])-m)**2).sum())[1]
    return o
if __name__=='__main__':
    o=reduce(); opslaan(o,'sprite/r17/kaal.png'); toon(o)
    for k in range(1,17): print(k,CH[k],(o==k).sum(),end=' | ')
