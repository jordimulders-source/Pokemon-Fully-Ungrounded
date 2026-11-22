# Pinsir-evolutie: modelklassen per pixel van het 1024-model (geen natief raster: Gemini tekende tanden/zaagtanden
# fijner dan zijn eigen 10,24-raster, de natieve mediaan verloor de tanden) en de kale reductie naar het spriteraster
# met "de modelklasse met de meeste pixels wint" per spritecel (GEMINI.md, onweerswolk-Swablu: meerderheidsband, geen gemiddelde tint).
import numpy as np; from PIL import Image
MODEL='referenties/gemini_gekozen_r4B.png'
# klassen: 0 bg | 1 zwart (lijn) | lijf 2 donkerst 3 donker 4 midden 5 licht | kaak 6 donker 7 midden 8 licht
#          | dekschild 9 vlek/donker 10 midden 11 licht | 12 tand/oog (crème)
NK=13
def label(mask,acht=True):
    from scipy import ndimage
    st=np.ones((3,3)) if acht else None
    return ndimage.label(mask,structure=st)
def klassen():
    from scipy import ndimage
    a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=a.mean(2); sat=a.max(2)-a.min(2)
    fg=a.min(2)<215
    warm=fg&((R-B)/(L+1)>0.55)&(L>40)
    yy,xx=np.mgrid[:1024,:1024]
    # materiaalgebieden: warme componenten, gaten gevuld; kaken links van x 500, dekschild rechts ervan
    lab,n=label(warm)
    kaak=np.zeros_like(fg); schild=np.zeros_like(fg)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()<400: continue
        cx=xx[m].mean()
        if cx<500: kaak|=m&~((xx>380)&(yy>560))      # buikvlek (warm bruin lijf) onder de kaakbasis is geen kaak
        else: schild|=m
    kaak=ndimage.binary_fill_holes(ndimage.binary_closing(kaak,iterations=4))&fg
    schild=ndimage.binary_fill_holes(ndimage.binary_closing(schild,iterations=6))&fg
    c=np.zeros(L.shape,np.uint8)
    c[fg&(L>=72)]=5; c[fg&(L<95)]=4; c[fg&(L<72)]=3; c[fg&(L<50)]=2
    # lijf licht: >=95
    c[fg&(L>=95)]=5
    k=kaak&(L>=25)
    c[k]=7; c[k&(L<62)]=6; c[k&(L>=92)]=8
    s=schild&(L>=25)
    c[s]=10; c[s&(L<75)]=9; c[s&(L>=128)]=11
    c[fg&(L<25)]=1
    c[fg&(L>165)&(sat<50)&(yy<560)&(xx<560)]=12      # tanden en ogen
    return a,c,fg
def reduceer(c,fg,x0,y0,cel,W,H,wzwart=1.0,alpha=0.45):
    o=np.zeros((H,W),np.uint8); frac=np.zeros((H,W,NK))
    for j in range(H):
        for i in range(W):
            ya,yb=int(round(y0+j*cel)),int(round(y0+(j+1)*cel)); xa,xb=int(round(x0+i*cel)),int(round(x0+(i+1)*cel))
            ya,xa=max(ya,0),max(xa,0)
            blk=c[ya:yb,xa:xb]; f=fg[ya:yb,xa:xb]
            if blk.size==0: continue
            h=np.bincount(blk[f].ravel(),minlength=NK).astype(float)/blk.size
            frac[j,i]=h
            if f.mean()<alpha: continue
            h=h.copy(); h[1]*=wzwart
            o[j,i]=h[1:].argmax()+1
    return o,frac
def platen(a,c,fg,glans_min=95,glans_d=20,minpx=40):
    # r2: lijf als PLATEN. De zwarte modellijnen (klasse 1) scheiden het lijf in platen (4-samenhangend); elke plaat krijgt de
    # band van zijn mediane modelhelderheid (2 <50, 3 <72, 4 <95, 5 >=95), alleen de glans (helderheid >= max(95, mediaan+20))
    # wordt licht (5). Zo worden de dij-/knieplaten één vlak met de gemeten middentint i.p.v. een gestreepte textuur.
    from scipy import ndimage
    L=a.mean(2); m=np.isin(c,(2,3,4,5))
    lab,n=ndimage.label(m)
    med=ndimage.median(L,lab,index=np.arange(1,n+1)); cnt=ndimage.sum(m,lab,index=np.arange(1,n+1))
    med=np.concatenate([[0],med]); cnt=np.concatenate([[0],cnt])
    M=med[lab]
    t=np.where(M<50,2,np.where(M<72,3,np.where(M<95,4,5)))
    g=m&(L>=np.maximum(glans_min,M+glans_d))
    t[g]=5
    small=m&(cnt[lab]<minpx)
    c2=c.copy(); c2[m&~small]=t[m&~small]
    return c2,lab,M
