# Natieve modelpixels (natief.png, 255x255, pitch 3,998) indelen in kleurgroepen. Afgeleid van fase 2 groepen.py.
# Niets getekend: alleen classificatie.
# 0 bg | 1 zwart (lijn) | 2 roze | 4 groen | 6 wit/lichtgrijs (vruchtvlees, tand, oogwit) | 7 pit | 8 geel (tong)
import numpy as np; from PIL import Image; from collections import deque
def laad(pad='natief.png'):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int); H,W=a.shape[:2]
    R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B
    sat=(a.max(2)-a.min(2))/np.maximum(a.max(2),1)
    bg0=(a.min(2)>=228)&((a.max(2)-a.min(2))<28)
    bg=np.zeros(bg0.shape,bool); q=deque((y,x) for y in range(H) for x in (0,W-1) if bg0[y,x])
    q+=deque((y,x) for x in range(W) for y in (0,H-1) if bg0[y,x])
    for y,x in q: bg[y,x]=1
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and bg0[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
    # ingesloten achtergrondgaten (tussen poten/staart): wit, groot (>= 6 px) en buiten de bek
    mond=np.zeros((H,W),bool); mond[95:135,30:75]=True            # bek (vruchtvlees, tanden, tong-aanzet), gemeten op groepen.png
    oog=np.zeros((H,W),bool); oog[78:94,42:60]=True              # oog (wit + pupil), gemeten op natief.png
    seen=bg.copy()
    for y0,x0 in zip(*np.where(bg0&~bg)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            y,x=st.pop(); cl.append((y,x))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and bg0[yy,xx] and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
        if len(cl)>=6 and not any(mond[y,x] or oog[y,x] for y,x in cl):
            for y,x in cl: bg[y,x]=1
    fg=~bg; g=np.zeros((H,W),int)
    hue=np.zeros((H,W))
    mx=a.max(2); mn=a.min(2); d=np.maximum(mx-mn,1)
    hr=((G-B)/d)%6; hg=(B-R)/d+2; hb=(R-G)/d+4
    hue=np.where(mx==R,hr,np.where(mx==G,hg,hb))*60
    geel=fg&(sat>=0.3)&(hue>=30)&(hue<=62)&(R>=110)
    g[fg&(lum<45)]=1
    g[geel&(g==0)]=8
    grijs=fg&(g==0)&(sat<0.16)
    g[grijs&(lum>=150)]=6
    g[grijs&(lum<150)&mond]=7
    g[grijs&(lum<150)&~mond&(lum<100)]=1
    halo=grijs&(lum<150)&~mond&(lum>=100); bg|=halo; fg=~bg
    g[halo]=0
    wp=np.pad((g==6)|(g==7),1)
    nb=sum(wp[1+dy:H+1+dy,1+dx:W+1+dx].astype(int) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
    g[(g==1)&mond&(nb>=4)]=7
    seen=np.zeros((H,W),bool)
    for y0,x0 in zip(*np.where(g==7)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            y,x=st.pop(); cl.append((y,x))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if g[yy,xx]==7 and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
        if len(cl)>=8:
            for y,x in cl: g[y,x]=1
    # geel alleen in de tong: componenten < 20 px (mengtint op roze/groen-grenzen) terug naar roze/groen
    seen=np.zeros((H,W),bool)
    for y0,x0 in zip(*np.where(g==8)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            y,x=st.pop(); cl.append((y,x))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<H and 0<=xx<W and g[yy,xx]==8 and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
        if len(cl)<20:
            for y,x in cl: g[y,x]=0
    # lichte anti-aliasrand (wit/grijs met >= 3 achtergrondburen) = achtergrond; tanden/oogwit hebben een zwarte rand
    for _ in range(2):
        bp=np.pad(bg,1)
        nbg=sum(bp[1+dy:H+1+dy,1+dx:W+1+dx].astype(int) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
        h2=(g==6)&(nbg>=3); bg|=h2; g[h2]=0
    # ingesloten wit gat (staart/poot), lichtgrijs door compressie: component wit (g==6) >= 10 px buiten bek en oog
    seen=np.zeros((H,W),bool)
    for y0,x0 in zip(*np.where(g==6)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            y,x=st.pop(); cl.append((y,x))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and g[yy,xx]==6 and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
        if len(cl)>=10 and not any(mond[y,x] or oog[y,x] for y,x in cl):
            for y,x in cl: g[y,x]=0; bg[y,x]=1
    fg=~bg
    rest=fg&(g==0)
    g[rest&(G>=R)]=4
    g[fg&(g==0)]=2
    # tongrand: olijf/bruine en crème randpixels rond de tong (hue 15-70) horen bij de tong; crème met achtergrondburen = halo
    tb=np.zeros((H,W),bool); tb[105:147,12:50]=True
    for _ in range(2):
        gp=np.pad(g==8,1); bp=np.pad(bg,1)
        ng=sum(gp[1+dy:H+1+dy,1+dx:W+1+dx].astype(int) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
        nbg=sum(bp[1+dy:H+1+dy,1+dx:W+1+dx].astype(int) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
        kand=tb&(g!=8)&(g!=0)&(ng>=1)&(hue>=15)&(hue<=70)&(g!=7)
        h3=kand&(lum>=190)&(nbg>=2); bg|=h3; g[h3]=0
        g[kand&~h3]=8
    return a,lum,g
def tonen(a,lum,g,grp,K):
    px=a[g==grp].astype(float); l2=px@[0.299,0.587,0.114]
    cen=np.array([px[np.argsort(l2)[int(q*(len(px)-1))]] for q in np.linspace(0.05,0.95,K)])
    for _ in range(50):
        lab=((px[:,None]-cen[None])**2).sum(2).argmin(1)
        cen=np.array([px[lab==k].mean(0) if (lab==k).any() else cen[k] for k in range(K)])
    uq=np.unique(a[g==grp],axis=0); cen=np.array([uq[((uq-c)**2).sum(1).argmin()] for c in cen])
    return cen[np.argsort(cen@[0.299,0.587,0.114])]
if __name__=='__main__':
    import sys
    a,lum,g=laad(sys.argv[1] if len(sys.argv)>1 else 'natief.png')
    K={1:(20,16,24),2:(216,84,128),4:(72,120,72),6:(255,255,255),7:(0,0,255),8:(255,220,0)}
    o=np.full(a.shape,200)
    for k,c in K.items(): o[g==k]=c
    Image.fromarray(o.astype('uint8')).crop((10,45,248,240)).resize((238*4,195*4),Image.NEAREST).save('groepen.png')
    for k in range(9): print(k,(g==k).sum())
    for grp,K2 in ((2,5),(4,5),(6,3),(8,4)): print(grp,tonen(a,lum,g,grp,K2).tolist())
