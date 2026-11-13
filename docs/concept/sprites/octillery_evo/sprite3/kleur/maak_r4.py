# r4 = r3 + MOET-punten 2-5 uit EINDKEURING_r3.md. Variant r4_B: paletstap idx5 (MOET 1, keuze Jordi). Gebruik: python3 maak_r4.py
from PIL import Image; import numpy as np
im=Image.open('r3.png'); a=np.array(im); pal=im.getpalette(); b=a.copy()
def zet(px,van,naar):
    for x,y in px:
        assert a[y,x]==van,(x,y,a[y,x]); b[y,x]=naar
zet([(57,47),(58,47)],1,4)          # dubbele lijn
zet([(51,8),(7,48)],2,1)            # losse lijnkleur
zet([(21,22),(54,24)],11,10)        # lichtgeel op de buitenrand
zet([(11,33),(11,34),(12,34),(11,35),(12,35)],5,4)   # schaduwstreep linkerarm
# MAG 6-9
zet([(21,32)],12,11); zet([(21,33)],11,10)
zet([(26,44),(27,44),(26,45),(27,45)],6,5)
zet([(50,26),(51,26),(51,27)],6,5)
zet([(8,32),(8,33),(8,34)],1,2)
def bewaar(arr,p,naam):
    o=Image.fromarray(arr,'P'); o.putpalette(p); o.save(naam,transparency=0)
bewaar(b,pal,'r4.png')
pB=list(pal); print('idx5 was',pal[15:18]); pB[15:18]=[168,56,72]; bewaar(b,pB,'r4_B.png')
print('gewijzigd t.o.v. r3:',int((a!=b).sum()),'px; silhouet-diff',int(((a>0)!=(b>0)).sum()))
