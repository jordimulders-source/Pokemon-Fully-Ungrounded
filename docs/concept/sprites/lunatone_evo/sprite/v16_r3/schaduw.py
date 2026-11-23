# Ronde 3 (opdracht Claude): alleen de rechterkant, vanaf v16_r2 (silhouet en gezicht ongewijzigd).
# 1. doorlopende verticale naad tussen lijf en donkere band weg (-> tint van de schaduwbaan);
#    dwarsbarsten (horizontaal lopend, uit het model) blijven, als twee tinten donkerder dan hun baan.
# 2. schaduw als sikkel: banen 4 -> 3 -> 2 naar de rand, breedte volgt cos(hoek) (breed in het midden, smal boven/onder),
#    afstand = afstand tot de echte buitenrand (volgt dus de ronde omtrek).
# 3. brokje rechtsboven los: (52,18) en (53,18) weg (1 px lucht, ook diagonaal).
import sys, numpy as np; from scipy import ndimage; import tool
src,dst=sys.argv[1],sys.argv[2]
o0=np.load(src); o=o0.copy()
J,I=np.mgrid[0:64,0:64]
# 3. brokje
for x,y in [(52,18),(53,18)]: o[y,x]=0
fig=o>0
lab,n=ndimage.label(fig); s=np.bincount(lab.ravel()); s[0]=0; main=lab==np.argmax(s)
cx,cy=35.2,30.5
ring=(o==1)&(I>=24)&(I<=40)&(J>=20)&(J<=38)
eye=ndimage.binary_dilation(ndimage.binary_fill_holes(ring),iterations=2)
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
d=ndimage.distance_transform_edt(fig)          # rand = 1
th=np.arctan2(J+.5-cy,I+.5-cx)
w=np.clip(np.cos(th),0,1)**0.7
zone=main&~rim&~eye&(I>=40)&(J>=10)&(J<=42)&(np.abs(th)<np.radians(78))
u=(d-1)/np.maximum(w,1e-3)
band=np.zeros((64,64),int)
band[zone&(u<1.6)]=2; band[zone&(u>=1.6)&(u<4.2)]=3; band[zone&(u>=4.2)&(u<7.4)]=4
inband=band>0
# barsten in de zone: zwart/selout binnenin
C=(o==1)&zone
# verticale runs >= 3 = naad; pixels met een horizontale barstbuur zijn dwarsbarst
hn=np.zeros((64,64),bool); hn[:,1:]|=C[:,:-1]; hn[:,:-1]|=C[:,1:]
vrun=np.zeros((64,64),bool)
for x in range(64):
    y=0
    while y<64:
        if C[y,x]:
            y2=y
            while y2<64 and C[y2,x]: y2+=1
            if y2-y>=3: vrun[y:y2,x]=True
            y=y2
        else: y+=1
naad=C&vrun&~hn
dwars=C&~naad
# in de zone, buiten de banen: naadpixels krijgen de lijftint ernaast
DONK={4:2,3:1,2:1}   # dwarsbarst twee stappen donkerder dan zijn baan, zodat hij blijft lezen
for y,x in zip(*np.where(zone)):
    if inband[y,x]:
        o[y,x]=DONK[band[y,x]] if dwars[y,x] else band[y,x]
    elif naad[y,x]:
        st=[v for v in o[y-1:y+2,x-1:x+2].ravel() if v in (3,4,5,7)]
        o[y,x]=max(set(st),key=st.count) if st else 4
    elif o[y,x] in (2,3) and not dwars[y,x]:
        # donkere bandresten binnen de sikkel-binnenrand -> 4 (overgang lijf -> schaduw)
        o[y,x]=4
# overgebleven korte verticale stompjes van de naad (<=2 px, niet aan een dwarsbarst) -> baantint
L,nl=ndimage.label((o==1)&zone)
for c in range(1,nl+1):
    m=L==c
    ys,xs=np.where(m)
    if m.sum()<=2 and not (ndimage.binary_dilation(m,np.ones((3,3)))&~m&(o==1)&~zone).any():
        o[m]=np.where(band[m]>0,band[m],4)
# losse zwarte blokjes (geen lijnvorm, <=4 px, raken geen andere lijn) in de zone -> donkere tint 3
L,nl=ndimage.label((o==1)&zone,structure=np.ones((3,3))); blok=0
for c in range(1,nl+1):
    m=L==c; ys,xs=np.where(m)
    if m.sum()<=4 and np.ptp(ys)>=1 and np.ptp(xs)>=1 and not (ndimage.binary_dilation(m,np.ones((3,3)))&~m&(o==1)).any():
        o[m]=3; blok+=int(m.sum())
print('losse zwarte blokjes -> 3:',blok)
# vlekjes < 3 px in de zone -> meest voorkomende buurtint
for _ in range(2):
  for v in (2,3,4,5):
    L,nl=ndimage.label((o==v)&zone)
    for c in range(1,nl+1):
        m=L==c
        if m.sum()>=3: continue
        if v==2 and (ndimage.binary_dilation(m)&rim).any(): continue
        rr=ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m&zone
        st=[t for t in o[rr] if t in (2,3,4,5) and t!=v]
        if st: o[m]=max(set(st),key=st.count)
np.save(f'{dst}/idx.npy',o); tool.save(o,f'{dst}/sprite.png'); tool.save(o,f'{dst}/sprite_8x.png',8)
dif=o!=o0
gez=eye|((I<=24)&(J>=23)&(J<=34))
print(dst,'gewijzigd t.o.v. r2:',int(dif.sum()),'| gezicht:',int((dif&gez).sum()),'| silhouet:',int(((o>0)!=(o0>0)).sum()),
      '| buiten de rechterzone (excl. brokje):',int((dif&~zone&~((J==18)&((I==52)|(I==53)))).sum()),
      '| naadpixels weg:',int(naad.sum()),'| dwarsbarstpixels:',int(dwars.sum()))
