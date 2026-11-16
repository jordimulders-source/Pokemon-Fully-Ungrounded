# Stap 2-3: model (natief raster) -> 64x64. Alleen: losse vliegende onderdelen gummen (Jordi), verkleinen met
# oppervlak-middeling per kleurgroep, lijnen bewaren ("donkerste wint" bij voldoende dekking), kwantiseren naar
# modelkleuren. Variant A: alles uniform. Variant B: hoogte vult 64, alleen de staart (rechts van XC) horizontaal ingedrukt.
import sys; from PIL import Image; import numpy as np; from comp import label
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
import os; MODE=os.environ.get('MODE','mode')
TL=float(sys.argv[2]) if len(sys.argv)>2 else 0.30; TN=float(sys.argv[3]) if len(sys.argv)>3 else 0.25
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int).copy()
fg=a.min(2)<225
lab,n=label(fg)
# gummen: de losse onderdelen rechts achter de wagon (componenten niet-groen, los van het lijf)
gum=0
for k in range(1,n+1):
    m=lab==k; c=a[m].mean(0)
    if m.sum()<200 and not (c[1]>c[0]+25):   # niet-groen = bout/plaatje
        a[m]=255; fg[m]=False; gum+=m.sum()
print('gegumd natieve px',gum)
H=lambda s:int(s.strip('#'),16)
PAL=['#292018',                                    # 1 omlijning
     '#b5f3b6','#72d779','#67b370','#467e4b',      # 2-5 geest (fase 3)
     '#3f6036',                                    # 6 donkergroen (model)
     '#9cf08d',                                    # 7 neonbarst (model)
     '#a0846a','#725641','#3d3827',                # 8-10 hout (model)
     '#8c6246',                                    # 11 roest (model)
     '#aba09a','#7b7c7e','#4a443c']                # 12-14 staal (model)
P=np.array([[H(c[1:3]),H(c[3:5]),H(c[5:7])] for c in PAL],float)
GROUP={1:'O',2:'G',3:'G',4:'G',5:'G',6:'G',7:'N',8:'W',9:'W',10:'W',11:'W',12:'S',13:'S',14:'S'}
# model-clustercentra -> paletindex (klassering per natieve pixel op de modelkleuren)
CEN={'#1e1b10':1,'#271f16':1,'#3d3827':10,'#4a443c':14,'#3f6036':6,'#437e45':5,'#725641':9,'#4e774f':5,
     '#8c6246':11,'#539555':4,'#589d5c':4,'#7b7c7e':13,'#67ac66':4,'#a0846a':8,'#72c071':3,'#7cc777':3,
     '#aba09a':12,'#8cd585':3,'#9cf08d':7,'#b9f3b0':2}
CC=np.array([[H(k[1:3]),H(k[3:5]),H(k[5:7])] for k in CEN],float); CI=np.array(list(CEN.values()))
d=((a[...,None,:]-CC[None,None])**2).sum(-1); cls=CI[d.argmin(-1)]; cls[~fg]=0
ys,xs=np.where(fg); X0,X1,Y0,Y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
print('inhoud natief',X1-X0,'x',Y1-Y0)
if VAR=='A': s=64/(X1-X0); XC=X1; k=1.0
else:
    s=63/(Y1-Y0); XC=int(sys.argv[4]) if len(sys.argv)>4 else 168
    k=(64/s-(XC-X0))/(X1-XC)            # indrukfactor staart
print('schaal',round(s,4),'XC',XC,'staartfactor',round(k,3))
def inv(u):  # sprite-x (in natieve eenheden na indrukken) -> natieve x
    return np.where(u<XC-X0, X0+u, XC+(u-(XC-X0))/k)
SS=8
W=64; Hh=int(np.ceil((Y1-Y0)*s))
out=np.zeros((64,64),int); BLK={}; oy=64-Hh-0  # onderaan uitlijnen
oy=max(0,(64-Hh)//2+ (64-Hh)//4)
for j in range(Hh):
    for i in range(W):
        us=(i+(np.arange(SS)+0.5)/SS)/s; vs=Y0+(j+(np.arange(SS)+0.5)/SS)/s
        xx=inv(us).astype(int); yy=vs.astype(int)
        xx=np.clip(xx,0,198); yy=np.clip(yy,0,198)
        c=cls[np.ix_(yy,xx)].ravel()
        cov=(c>0).mean()
        if cov<0.5: continue
        cc=c[c>0]; BLK[(oy+j,i)]=cc
        if (cc==1).mean()*cov>=TL*cov and (cc==1).mean()>=TL: out[oy+j,i]=1; continue
        if (cc==7).mean()>=TN: out[oy+j,i]=7; continue
        g=[GROUP[v] for v in cc]; gs,gc=np.unique(g,return_counts=True); G=gs[gc.argmax()]
        sel=np.array([GROUP[v]==G for v in cc])
        if MODE=='mode':   # meest voorkomende modelkleur binnen de groep
            u,uc=np.unique(cc[sel],return_counts=True); out[oy+j,i]=u[uc.argmax()]
        else:              # vlakgemiddelde -> dichtstbijzijnde modelkleur in de groep
            rgb=P[cc[sel]-1].mean(0); idx=[q for q in GROUP if GROUP[q]==G]
            out[oy+j,i]=idx[int(np.argmin(((P[np.array(idx)-1]-rgb)**2).sum(1)))]
# randregel (buitenlijn uit het model): randpixel -> donkerste modelkleur in zijn blok
LUM=P@[0.3,0.59,0.11]; nr=0
fgm=out>0; pad=np.pad(fgm,1)
edge=fgm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
for (y,x) in zip(*np.where(edge)):
    cc=BLK[(y,x)]; v=cc[np.argmin(LUM[cc-1])]
    if v!=out[y,x]: out[y,x]=v; nr+=1
print('randpixels naar donkerste modelkleur',nr)
np.save(f'basis_{VAR}.npy',out); open(f'basis_{VAR}.meta','w').write(f'{s} {X0} {Y0} {oy} {XC} {k}')
pal=[0,0,0]+[int(v) for v in P.ravel()]; pal+= [0]*(768-len(pal))
im=Image.fromarray(out.astype(np.uint8),'P'); im.putpalette(pal); im.save(f'basis_{VAR}.png',transparency=0)
rgb=np.where(out[...,None]>0,P[np.maximum(out,1)-1],255).astype(np.uint8)
Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(f'basis_{VAR}_8x.png')
ys,xs=np.where(out>0); print('sprite bbox',xs.min(),xs.max(),ys.min(),ys.max(),'kleuren',len(np.unique(out))-1)
