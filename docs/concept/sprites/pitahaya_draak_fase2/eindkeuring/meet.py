# meet.py: Gen 3-metingen (rand, zwart, clusters, dambord, losse lichte px, contrast) voor de sprite en referenties
import sys, numpy as np; from PIL import Image; from collections import Counter
def comps(m):
    seen=np.zeros_like(m,bool); out=[]
    for y,x in zip(*np.nonzero(m)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=0
        while st:
            yy,xx=st.pop(); c+=1
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
                v,u=yy+dy,xx+dx
                if 0<=v<m.shape[0] and 0<=u<m.shape[1] and m[v,u] and not seen[v,u]: seen[v,u]=True; st.append((v,u))
        out.append(c)
    return out
def laad(p):
    im=Image.open(p); a=np.array(im)[:64]; pal=np.array(im.getpalette()[:48]).reshape(16,3); return a,pal
def lum(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]
def meet(p,naam):
    a,pal=laad(p); fg=a>0; L=np.array([lum(c) for c in pal]); H,W=a.shape
    pad=np.pad(fg,1); rand=fg&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    zw=L[a]<40
    # buitenrand: aandeel zwart, aandeel licht (L>150)
    rz=(zw&rand).sum()/rand.sum(); rl=((L[a]>150)&rand).sum()
    binnen=fg&~rand; bz=(zw&binnen).sum()/binnen.sum()
    # wisselingen zwart/niet-zwart langs de buitenrand (4-buren binnen de randpixels)
    wis=0; n=0
    for y,x in zip(*np.nonzero(rand)):
        for dy,dx in ((0,1),(1,0)):
            yy,xx=y+dy,x+dx
            if yy<H and xx<W and rand[yy,xx]: n+=1; wis+= zw[y,x]!=zw[yy,xx]
    # clusters < 3 px per index (niet zwart), binnen de figuur
    klein=0
    for i in set(a[fg].ravel()):
        if L[i]<40: continue
        klein+=sum(1 for s in comps(a==i) if s<3)
    # dambord 2x2 (twee kleuren diagonaal, beide niet transparant)
    db=0
    for y in range(H-1):
        for x in range(W-1):
            q=a[y:y+2,x:x+2]
            if q[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q: db+=1
    # losse lichte pixels: L>200 met <=1 buur van dezelfde index
    ll=0
    for y,x in zip(*np.nonzero(fg&(L[a]>200))):
        nb=sum(1 for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)) if 0<=y+dy<H and 0<=x+dx<W and a[y+dy,x+dx]==a[y,x])
        ll+= nb==0
    # zwakke tintgrenzen: buurparen van verschillende niet-zwarte indices met |dL|<20
    zwak=0; tot=0
    for y in range(H):
        for x in range(W):
            for dy,dx in ((0,1),(1,0)):
                yy,xx=y+dy,x+dx
                if yy<H and xx<W and fg[y,x] and fg[yy,xx] and a[y,x]!=a[yy,xx] and L[a[y,x]]>=40 and L[a[yy,xx]]>=40:
                    tot+=1; zwak+= abs(L[a[y,x]]-L[a[yy,xx]])<20
    print(f'{naam:12s} px {fg.sum():5d} kleuren {len(set(a[fg].ravel())):2d} rand zwart {rz:.0%} licht-op-rand {rl:3d} zwart binnen {bz:.1%} '
          f'rand-wissels {wis/max(n,1):.0%} clusters<3 {klein:3d} dambord {db:3d} losse-licht {ll:2d} zwakke grenzen {zwak/max(tot,1):.0%}')
B='/home/user/Pokemon-Fully-Ungrounded/'
meet(sys.argv[1] if len(sys.argv)>1 else B+'docs/concept/sprites/pitahaya_draak_fase2/sprite_r9/pitahaya2_r9A.png','r9A')
for n in ['feraligatr','swampert','salamence','sceptile','lairon','torkoal','croconaw','exploud']:
    meet(B+f'graphics/pokemon/{n}/anim_front.png',n)
