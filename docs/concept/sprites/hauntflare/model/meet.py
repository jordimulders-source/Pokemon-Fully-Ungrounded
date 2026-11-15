# Meet bol (cirkel) in de Gemini-plaatjes: roze pixels met hoge blauwwaarde
import sys; from PIL import Image; import numpy as np
for n in sys.argv[1:]:
    a=np.asarray(Image.open(n).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    pink=(r>200)&(b>120)&(b<235)&(g<200)
    ys,xs=np.where(pink)
    # randen per rij -> cirkelfit (kleinste kwadraten) op linker/rechterrand van de grootste roze vlek
    pts=[]
    for y in range(ys.min(),ys.max()+1):
        row=xs[ys==y]
        if len(row)>40: pts+= [(row.min(),y),(row.max(),y)]
    P=np.array(pts,float); A=np.c_[2*P,np.ones(len(P))]; bb=(P**2).sum(1)
    cx,cy,c=np.linalg.lstsq(A,bb,rcond=None)[0]; R=np.sqrt(c+cx*cx+cy*cy)
    print(n,'centrum',round(cx),round(cy),'R',round(R),'pinkbbox',xs.min(),xs.max(),ys.min(),ys.max())
