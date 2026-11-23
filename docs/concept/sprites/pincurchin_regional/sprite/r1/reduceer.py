# natief_A (100x100) -> kale reductie 64x64: vlakgemiddelde per spritepixel + dichtstbijzijnde modelkleur binnen de eigen kleurgroep
# donkere modellijn wint als ze >= ZW van het vlak beslaat. Niets getekend.
from PIL import Image;import numpy as np,sys
from kaart import P
IN=sys.argv[1] if len(sys.argv)>1 else 'natief_A.png'; UIT=sys.argv[2] if len(sys.argv)>2 else 'kaal.png'
WO=60; X0,Y0,NW,NH=10,13,82,73; ZW=0.34; ALPHA=0.45
a=np.asarray(Image.open(IN).convert('RGB')).astype(float)
bg=a.min(axis=2)>=200
dark=(a.max(axis=2)<40)
lum=a@[0.299,0.587,0.114]; dbr=(~dark)&(lum<62)&~(a[...,0]-a[...,1]>50)&~bg
ZD=0.30
MODUS=len(sys.argv)>3
red=(a[...,0]-a[...,1]>50)
s=NW/WO; HO=int(round(NH/s))
NAMEN=['K','D','s','m','l','r','R','L']; C=np.array([P[k] for k in NAMEN],float)
BR=[1,2,3,4]; RD=[5,6,7]
out=np.full((64,64),-1,int)
ox=(64-WO)//2; oy=63-HO
def w1(lo,hi):
    cells=[];i=int(np.floor(lo))
    while i<hi:
        w=min(hi,i+1)-max(lo,i)
        if w>1e-6: cells.append((i,w))
        i+=1
    return cells
for j in range(HO):
    ys=w1(Y0+j*s,Y0+(j+1)*s)
    for i in range(WO):
        xs=w1(X0+i*s,X0+(i+1)*s)
        tw=0;nb=0;col=np.zeros(3);dk=0;rd=0;br=0;dd=0
        for y,wy in ys:
            for x,wx in xs:
                w=wy*wx; tw+=w
                if bg[y,x]: continue
                nb+=w; col+=w*a[y,x]
                if dark[y,x]: dk+=w
                if dbr[y,x]: dd+=w
                elif red[y,x]: rd+=w
                else: br+=w
        if nb/tw<ALPHA: continue
        if dk/tw>=ZW: out[oy+j,ox+i]=0; continue
        if (dk+dd)/tw>=ZW and rd<br: out[oy+j,ox+i]=1; continue
        # kleur zonder de zwarte lijn
        cm=np.zeros(3);cw=0
        for y,wy in ys:
            for x,wx in xs:
                if bg[y,x] or dark[y,x]: continue
                cm+=wy*wx*a[y,x]; cw+=wy*wx
        if cw==0: out[oy+j,ox+i]=0; continue
        cm/=cw; grp=RD if rd>br else BR
        if MODUS:
            st={}
            for y,wy in ys:
                for x,wx in xs:
                    if bg[y,x] or dark[y,x]: continue
                    d=((C[grp]-a[y,x])**2).sum(1); k=grp[d.argmin()]; st[k]=st.get(k,0)+wy*wx
            out[oy+j,ox+i]=max(st,key=st.get)
        else:
            d=((C[grp]-cm)**2).sum(1); out[oy+j,ox+i]=grp[d.argmin()]
np.save(UIT.replace('.png','.npy'),out)
pal=[(255,0,255)]+[P[k] for k in NAMEN]
p=Image.fromarray((out+1).astype('uint8'),'P'); flat=[v for c in pal for v in c]; p.putpalette(flat+[0]*(768-len(flat))); p.save(UIT,transparency=0)
q=Image.open(UIT).convert('RGBA'); bgc=Image.new('RGBA',q.size,(255,255,255,255)); bgc.alpha_composite(q); bgc.resize((512,512),Image.NEAREST).save(UIT.replace('.png','_8x.png'))
ys_,xs_=np.where(out>=0); print('bbox',xs_.min(),xs_.max(),ys_.min(),ys_.max(),'px',(out>=0).sum())
