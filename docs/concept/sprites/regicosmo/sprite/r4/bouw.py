# Regicosmo r4a/b/c op basis van r3 (Jordi 28 nov, zie NOTITIES.md). Bouwen: python3 sprite/r4/bouw.py && python3 sprite/r4/vel.py
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import gemeen as g, pal, rond as R, saturnus4 as S4
D=g.D
s=R.R3.copy(); DL=R.DL3.copy()
# 1. rondheid: Mars en maan naar de pixelcirkel van hun modelfit, ijs naar een cirkel van 10 px (maat r3) op zijn modelfit
CIRKEL={0:R.sprite_cirkel(0)[:3], 4:R.sprite_cirkel(4)[:3]}
ijs_c=(6.0,30.0,5.0)
def rond_delen():
    delen={}
    for k in range(7):
        if k in CIRKEL:
            img,m=R.rondmaken(s,DL,k,*CIRKEL[k]); delen[k]=(img,m)
        elif k==1:
            delen[k]=S4.ijs(*ijs_c,R)
        else:
            delen[k]=R.deel_beeld(s,DL,k)
    return delen
BASIS=rond_delen()
def variant(arm, groot=False):
    # posities t.o.v. r3: ijs en Saturnus 1 px naar rechts = de rest 1 px naar links (Saturnus zit al tot x63);
    # armen (asteroide, maan) 'arm' px omhoog; voeten 1 px omhoog; daarna alles 1 px omlaag zodat de onderkant op rij 61 blijft.
    OFF={0:(-1,0),1:(0,0),2:(0,0),3:(-1,-arm),4:(-1,-arm),5:(-1,-1),6:(-1,-1)}
    delen={}
    for k,(img,m) in BASIS.items():
        dx,dy=OFF[k]; delen[k]=R.schuif(img,m,dx,dy+1)
    info=''
    if groot:
        delen,info=schouders(delen)
    return R.samen(delen),info
def schouders(delen):
    """r4c: ijs en Saturnusbol 12 px (r=6), uit het model geschaald (S4.ijs / S4.maak). Het ijs past op de r4b-hoogte niet
    naast Mars (x0-11 raakt Mars); de laagste plek met >= 1 px tussenruimte tot Mars en asteroide wordt gezocht (omhoog
    langs de ronding van Mars). Saturnus komt op dezelfde hoogte (schouders gelijk, zoals het model); de ring krijgt de
    grootste lengte (zelfde kanteling en b/a) die binnen x63 en met >= 1 px tot Mars/maan past."""
    andere=lambda ks: np.any([delen[k][1] for k in ks],axis=0)
    vrij=lambda m,ks: not (ndimage.binary_dilation(m,np.ones((3,3)))&andere(ks)).any()
    for dy in range(0,12):
        img,m=S4.ijs(6.0,31.0-dy,6.0,R)
        if vrij(m,[0,3]): break
    delen[1]=(img,m)
    ang=S4.ANG; xb=lambda A: np.sqrt((A*np.cos(ang))**2+(A*S4.B2/S4.A2*np.sin(ang))**2)
    best=None
    for scx in (53.0,54.0,55.0,56.0,57.0):
        for A in np.arange(10.4,6.9,-0.1):
            if scx+xb(A)+1.95>64: continue
            si,sm,_=S4.maak(scx,31.0-dy,6.0,0,63,Avast=A)
            if vrij(sm,[0,4]):
                if best is None or A>best[0]: best=(A,scx,si,sm)
                break
    A,scx,si,sm=best; delen[2]=(si,sm)
    return delen,'ijs en Saturnusbol 12 px, %d px hoger dan r4b (ijs middelpunt (6,%d), Saturnus (%d,%d)); ring a=%.2f (r3: 8,48 bij bol 10)'%(dy,31-dy,scx,31-dy,A)
def compact(idx,P):
    used=[0]+[i for i in range(1,len(P)) if (idx==i).any()]
    m=np.zeros(256,'uint8'); m[used]=np.arange(len(used)); return m[idx],[P[i] for i in used]
if __name__=='__main__':
    print('cirkels:',{g.NAMEN[k]:v for k,v in CIRKEL.items()},'ijs',ijs_c)
    for naam,arm,groot in (('r4a',1,False),('r4b',2,False),('r4c',2,True)):
        (v,dl),info=variant(arm,groot)
        uit,P2=compact(v,g.PAL); pal.opslaan(uit,os.path.join(D,'regicosmo_%s.png'%naam),P2)
        np.save(os.path.join(D,naam+'.npy'),v); np.save(os.path.join(D,naam+'_deel.npy'),dl)
        ys,xs=np.where(v>0); lab,k=ndimage.label(v>0,np.ones((3,3)))
        t=R.tussenruimtes(dl)
        print(naam,'kleuren',len(P2),'bbox x%d-%d y%d-%d'%(xs.min(),xs.max(),ys.min(),ys.max()),'losse delen',k,'| kleinste tussenruimtes',t[:3],info)
