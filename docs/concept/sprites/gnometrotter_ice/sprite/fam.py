# fam.py (Ice): familie per modelpixel. 0 achtergrond (masker.py), 1 zwart/lijn, 2 ijs (muts, haar, baard, riem, stok, zolen, rugkam), 3 roze, 4 blauw (broek)
# Omtrek = Rock r8, dus de Rock-onderdelen (../../gnometrotter_rock/sprite/model_zone.npz) zijn de plaatsgids:
#  zwart: max(R,G,B) < 62 (als Rock)
#  roze:  in een Rock-rozezone (neus, lijf, armen, handen) als R >= B-2 (ijs is altijd blauwer dan rood); elders R-B > 18 en R-G > 18 (als Rock)
#  blauw: in de Rock-broekzone alles behalve zwart en neutraal/ijswit (sneeuwrand van de zolen); elders geen blauw (ijskristallen in stok en rugkam zijn ook blauw, maar ijs)
#  ijs:   de rest
import numpy as np; from PIL import Image
from masker import masker
MODEL='../r3/gemini_r3_lijf.png'
def familie(path=MODEL):
    a,fg=masker(path); r,g,b=[a[...,i] for i in range(3)]; L=0.3*r+0.59*g+0.11*b
    RZ=np.load('../../gnometrotter_rock/sprite/model_zone.npz')['z'].astype(int)
    yy=np.arange(r.shape[0])[:,None]+0*r
    f=np.full(r.shape,2)
    rz=np.isin(RZ,[5,6,7,8,9])
    f[(rz&(r>=b-2))|(~rz&(r-b>18)&(r-g>18))]=3
    bz=RZ==12
    f[bz&(b-r>=12)&(f!=3)]=4
    f[a.max(2)<62]=1
    f[~fg]=0
    return a,f
if __name__=='__main__':
    a,f=familie()
    np.savez_compressed('model_fam.npz',f=f.astype('uint8'))
    C=np.array([(255,255,255),(0,0,0),(170,200,230),(230,140,160),(40,90,200)],'uint8')
    Image.fromarray(C[f]).crop((260,30,760,530)).save('model_fam.png')
    print([(k,(f==k).sum()) for k in range(5)])
