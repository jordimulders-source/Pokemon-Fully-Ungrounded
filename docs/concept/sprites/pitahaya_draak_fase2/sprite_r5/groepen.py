# Natieve modelpixels (natief.png, 201x201, pitch 5,08) indelen in kleurgroepen + tonen per groep (k-means op echte modelkleuren).
# Afgeleid van pitahaya_draak/sprite_r1/groepen.py. Niets getekend: alleen classificatie.
# 0 bg | 1 zwart (lijn) | 2 roze | 4 groen | 6 wit/lichtgrijs (vruchtvlees, tand, oogwit) | 7 pit (grijs/zwart vlekje in het wit)
import numpy as np; from PIL import Image; from collections import deque
def laad(pad='natief.png'):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int); H,W=a.shape[:2]
    R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B
    sat=(a.max(2)-a.min(2))/np.maximum(a.max(2),1)
    bg0=(a.min(2)>=238)&((a.max(2)-a.min(2))<25)
    bg=np.zeros(bg0.shape,bool); q=deque((y,x) for y in range(H) for x in (0,W-1) if bg0[y,x])
    # gat in de staartkrul (model: wit achtergrondvlak ingesloten door de staart, x 161-165, y 103-106)
    q+=deque((y,x) for y in range(100,110) for x in range(158,168) if bg0[y,x])
    for y,x in q: bg[y,x]=1
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and bg0[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
    fg=~bg; g=np.zeros((H,W),int)
    g[fg&(lum<42)]=1
    grijs=fg&(g==0)&(sat<0.13)
    g[grijs&(lum>=150)]=6
    mond=np.zeros((H,W),bool); mond[86:124,15:58]=True          # bek (vruchtvlees + tanden), gemeten op groepen.png
    g[grijs&(lum<150)&mond]=7
    g[grijs&(lum<150)&~mond&(lum<100)]=1                          # grijze randpixels buiten de bek: lijn
    halo=grijs&(lum<150)&~mond&(lum>=100); bg|=halo; fg=~bg         # lichte anti-aliasrand buiten de bek: achtergrond
    # zwarte pitjes: zwarte pixel in de bek met >= 4 van 8 buren wit/pit (geen lip- of tandlijn)
    wp=np.pad((g==6)|(g==7),1)
    nb=sum(wp[1+dy:H+1+dy,1+dx:W+1+dx].astype(int) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
    g[(g==1)&mond&(nb>=4)]=7
    # componenten van >= 8 px zijn tandomlijning, geen pit: terug naar lijn
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
    rest=fg&(g==0)
    g[rest&(G>=R)]=4
    g[fg&(g==0)]=2
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
    a,lum,g=laad()
    K={1:(20,16,24),2:(216,84,128),4:(72,120,72),6:(255,255,255),7:(0,0,255)}
    o=np.full(a.shape,240)
    for k,c in K.items(): o[g==k]=c
    Image.fromarray(o.astype('uint8')).crop((5,40,195,155)).resize((760,460),Image.NEAREST).save('groepen.png')
    for k in range(8): print(k,(g==k).sum())
    for grp,K2 in ((2,5),(4,4),(6,2)): print(grp,tonen(a,lum,g,grp,K2).tolist())
