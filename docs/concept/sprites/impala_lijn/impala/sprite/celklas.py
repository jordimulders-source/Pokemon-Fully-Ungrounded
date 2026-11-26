# Per spritecel: meest voorkomende celklasse (toonband van de modelhelderheid) over de niet-lijnpixels van het model.
# Het model is cel-shaded (vlakke tonen 126/146/156/~198/~206/250 in het lijf); de meerderheid per cel geeft harde
# toongrenzen zoals in het model. Ook: kaal_flum (helderheid van alleen de flankpixels), kaal_sf (aandeel hoorn),
# kaal_dk (aandeel zwart, voor de plukjes). Toongrenzen, zonder mengtinten op de grens. Uit: kaal_cel.npy (lijst van banden per zone in build.py)
import numpy as np, json
from PIL import Image
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float)
lum=(a*[.299,.587,.114]).sum(2)
wl=np.load('witlab.npz')['a']; fg=~((wl==-2)|(wl==1)); seg=np.load('seg.npz')['a']
ids,cnt=np.unique(seg[seg>=0],return_counts=True); klein=ids[cnt<150]
lijn=fg&((seg<0)|np.isin(seg,klein))
km=json.load(open('kaal_meta.json')); x0,y0,p,W,H=km['x0'],km['y0'],km['p'],km['W'],km['H']
GR=[100,135,170,197,226]   # grenzen: <100 | 100-135 | 135-170 | 170-197 | 197-226 | >=226  -> klasse 0..5
cls=np.digitize(lum,GR)
out=-np.ones((H,W),int); frac=np.zeros((H,W)); flum=np.zeros((H,W)); sf=np.zeros((H,W)); dk=np.zeros((H,W)); al=np.zeros((H,W))
hoorn=np.isin(seg,[14,49])
for j in range(H):
    for i in range(W):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
        f=fg[ya:yb,xa:xb]&~lijn[ya:yb,xa:xb]
        ff=fg[ya:yb,xa:xb]; al[j,i]=ff.mean()                                  # modeldekking (r3: strengere silhouetdrempels)
        sf[j,i]=hoorn[ya:yb,xa:xb].mean()                                    # aandeel hoornvlak in de cel
        dk[j,i]=(lum[ya:yb,xa:xb][ff]<60).mean() if ff.any() else 0           # aandeel zwart (lijn/plukjes)
        if not f.any(): continue
        bc=np.bincount(cls[ya:yb,xa:xb][f],minlength=6); out[j,i]=bc.argmax(); frac[j,i]=bc.max()/bc.sum()
        fl=cls[ya:yb,xa:xb][f]; ll=lum[ya:yb,xa:xb][f]; k=(fl==3)|(fl==4)
        if k.any(): flum[j,i]=ll[k].mean()     # helderheid van alleen de flankpixels (geen menging met zadel/wit)
np.save('kaal_cel.npy',out); np.save('kaal_celfrac.npy',frac); np.save('kaal_flum.npy',flum); np.save('kaal_sf.npy',sf); np.save('kaal_dk.npy',dk); np.save('kaal_alpha.npy',al)
Z=np.load('kaal_zone.npy'); lf=np.load('kaal_lf.npy')
for j in range(H): print('%2d '%j+''.join('.' if Z[j,i]<0 else '#' if lf[j,i]>=.5 else 'DSMNLW'[out[j,i]] for i in range(W)))
