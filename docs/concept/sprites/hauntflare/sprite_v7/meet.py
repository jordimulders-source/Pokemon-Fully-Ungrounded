# Controles: (1) diff t.o.v. v6 alleen in de gezichtszone, (2) palet/transparantie, (3) tintvlakjes < 3 px rond het gezicht
import glob,os
import numpy as np
from PIL import Image
import kandidaten as K
from gezicht import F,a6,D
from scipy import ndimage
for f in sorted(glob.glob(D+'/kandidaat_*.png')):
    n=os.path.basename(f)[10:-4]; im=Image.open(f); a=np.array(im).astype(int)
    o,m,t=K.KANDIDATEN[n]
    # nieuwe gezichtspixels = alles wat bouw() plakt
    zone=F.copy()
    leeg=K.basis()
    import copy
    b=leeg.copy(); 
    oo=K.OGEN[o]; g=K.oog(oo['schrap'],oo['pupil_naar'],oo.get('rijschrap',()))
    w=len(g[0]); wr=5-len([r for r in oo.get('rijschrap',()) if r<5]); x0,y0=23-(w-1),28-wr
    for j,r in enumerate(g):
        for i,v in enumerate(r):
            if v is not None: zone[y0+j,x0+i]=True
    mm=K.MONDEN[m]; mg=K.mond(mm['kol'],mm.get('rij',()),t); x0,y0=mm['rechts']-(len(mg[0])-1),mm['boven']
    for j,r in enumerate(mg):
        for i,v in enumerate(r):
            if v is not None: zone[y0+j,x0+i]=True
    d=(a!=a6); buiten=d&~zone
    sil=((a==0)!=(a6==0)).sum()
    # tintvlakjes: bolkleuren 6-9 in x12-42,y16-42
    klein=[]
    for k in (6,7,8,9):
        lab,nn=ndimage.label(a==k,structure=np.ones((3,3)))
        for L in range(1,nn+1):
            ys,xs=np.nonzero(lab==L)
            if len(ys)<3 and all(12<=x<=42 and 16<=y<=42 for x,y in zip(xs,ys)) and any(zone[y,x] or any(zone[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2)) for x,y in zip(xs,ys)):
                klein.append((k,list(zip(xs.tolist(),ys.tolist()))))
    print(n,'gewijzigd',int(d.sum()),'| buiten zone',int(buiten.sum()),'| silhouet',int(sil),'| kleuren',len(np.unique(a)),'| mode',im.mode,'transp',im.info.get('transparency'))
    print('   tintvlakjes<3 bij gezicht:',klein)
