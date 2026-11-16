# Pitahaya-draak fase 2, r7 op r6. Jordi: "ja kijk, en dan moet wat boven dat grijs zit dezelfde tint krijgen of nog zelfs
# een tint donkerder, binnenkant bovenkant mond". Wig (boven de donkergrijze plooi) -> A: plooitint v; B: een tint donkerder.
import numpy as np; from PIL import Image
R=Image.open('pitahaya2_r6.png'); r6=np.asarray(R).astype(int); pal0=R.getpalette()
WIG=[(10,44),(12,44),(13,44),(11,45)]          # pit (11,44) blijft
lum=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2]
V=(155,154,159); X=(120,119,125)               # B: zelfde koele toon (B-G +5/+6), helderheid 155 -> 120 (stap 35)
for naam,idx,extra in (('A',13,None),('B',14,X)):
    o=r6.copy(); pal=list(pal0); log=[]
    if extra: pal[42:45]=list(extra)
    for x,y in WIG: log.append((x,y,o[y,x],idx)); o[y,x]=idx
    p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(f'pitahaya2_r7{naam}.png',transparency=0)
    d=set((x,y) for y,x in zip(*np.where(o!=r6))); assert d<=set(WIG); assert ((o>0)==(r6>0)).all()
    # geen dambord / losse pixel van de nieuwe tint
    for y in range(42,50):
        for x in range(7,18):
            q=o[y:y+2,x:x+2]; assert not (q[0,0]==q[1,1]!=q[0,1]==q[1,0] and {q[0,0],q[0,1]}<={10,11,13,14}),(naam,x,y)
    for x,y in WIG:
        assert any(o[y+dy,x+dx]==idx for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) or (naam=='A'), ('los',x,y)
    s=pal[36:39]; c=pal[3*idx:3*idx+3]
    print(naam,'gewijzigd',len(d),'(alleen wig; buiten 0; silhouet gelijk)','kleuren',len(set(o.flatten())),
          'contrast pit/wig',round(lum(c)-lum(s)),'wig',tuple(c),'lum',round(lum(c)))
    open(f'pitahaya2_r7{naam}_afwijkingen.txt','w').write('\n'.join(f'{x}\t{y}\tidx {a}->{b}\twig -> '+('plooitint v (155,154,159)' if naam=='A' else 'donkerst (120,119,125)') for x,y,a,b in log)+'\n')
