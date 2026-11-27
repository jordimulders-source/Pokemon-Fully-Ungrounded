# Klassen per natieve modelpixel (alleen indelen van modelkleuren): 0 bg, 1 K zwart, 2 R rood, 3 G groen, 4 W oogwit (wit/grijs, ingesloten)
# Zelfde regels als ../guarana/gereedschap/klassen.py, maar oogwit = ingesloten licht dat aan rood/zwart grenst (de trossen liggen nu overal).
import numpy as np; from PIL import Image; from collections import deque
def klassen(path='sprite_r4/natief_model.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    H,W=L.shape; c=np.zeros((H,W),int)
    wt=a.min(2)>=200
    bg=np.zeros(wt.shape,bool); q=deque()
    for y in range(H):
        for x in range(W):
            if (y in (0,H-1) or x in (0,W-1)) and wt[y,x]: bg[y,x]=True; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and wt[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; q.append((yy,xx))
    sat=a.max(2)-a.min(2)
    zw=(L<45)&~bg
    rood=(R>G+40)&~bg&~zw
    groen=(G>R+8)&~bg&~zw&~rood
    wit=~bg&~zw&~rood&~groen&(sat<40)&(L>=110)
    c[rood]=2; c[groen]=3; c[wit]=4; c[zw]=1
    rest=~bg&(c==0); c[rest]=np.where(L[rest]<110,1,4)
    # ingesloten wit zonder rood/zwart in de buurt (gaatjes tussen ranken) = achtergrond
    lab=np.zeros((H,W),int); k=0
    for y,x in zip(*np.where(c==4)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k; pts=[]
        while st:
            cy,cx=st.pop(); pts.append((cy,cx))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<H and 0<=xx<W and c[yy,xx]==4 and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
        rond=set()
        for cy,cx in pts:
            for dy in (-2,-1,0,1,2):
                for dx in (-2,-1,0,1,2):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<H and 0<=xx<W: rond.add(c[yy,xx])
        puur=np.mean([a[cy,cx].min()>=245 for cy,cx in pts])
        if 2 not in rond or len(pts)>70 or (puur>0.8 and len(pts)>12):
            for cy,cx in pts: c[cy,cx]=0 if a[cy,cx].min()>=200 else 3
    return a,c,L
