# Natief indexraster -> onderdelen (4-samenhangende vlakken tussen de zwarte lijnen). Print zonekaart.
import numpy as np
idx=np.load('natief_idx.npy')
ZWART={1,2}  # modelpalet 0 en 1 (bijna zwart) -> index 1,2 in natief_idx
fg=idx>0; vlak=fg&~np.isin(idx,list(ZWART))
lab=np.zeros(idx.shape,int); n=0
for y,x in zip(*np.where(vlak)):
    if lab[y,x]: continue
    n+=1; st=[(y,x)]; lab[y,x]=n
    while st:
        cy,cx=st.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=cy+dy,cx+dx
            if vlak[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
for i in range(1,n+1):
    yy,xx=np.where(lab==i); print(i,(lab==i).sum(),'x',xx.min(),xx.max(),'y',yy.min(),yy.max())
CH='.abcdefghijklmnopqrstuvwxyz'
for y in range(20,77): print('%2d '%y+''.join(('#' if idx[y,x] in ZWART else '.') if lab[y,x]==0 else CH[min(lab[y,x],26)] for x in range(26,74)))
np.save('natief_lab.npy',lab)
