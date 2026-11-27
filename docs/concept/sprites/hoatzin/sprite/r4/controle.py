# Gen 3-controles hoatzin r1
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
for f in ('hoatzin_r4.png','hoatzin_r4_variant_teken.png'):
    im=Image.open(os.path.join(HIER,f)); o=np.array(im)
    print(f,im.size,im.mode,'transparency',im.info.get('transparency'),'gebruikte kleuren excl. transparant',len(set(o.ravel())-{0}))
    fg=o>0; yy,xx=np.where(fg); print(' bbox x%d-%d y%d-%d (%dx%d), %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
    licht=0
    for Yy,X in zip(yy,xx):
        if o[Yy,X] in (4,7,9,11,12) and any(not(0<=Yy+dy<64 and 0<=X+dx<64 and fg[Yy+dy,X+dx]) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): licht+=1
    print(' lichte tint op de buitenrand:',licht,'(geelgroene punten tellen mee: bewust)')
    los=[]
    for k in range(2,13):
        lab,n=label(o==k,acht=True)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()<3: los.append((k,int(m.sum())))
    from collections import Counter
    print(' tintvlekjes <3 px (8-samenhang) per index:',dict(Counter(k for k,_ in los)))
    zw=0
    for Yy,X in zip(*np.where(o==1)):
        nb8=[o[Yy+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=Yy+dy<64 and 0<=X+dx<64]
        if 0 not in nb8 and 1 not in nb8: zw+=1
    print(' losse zwarte pixels:',zw,'| zwart %.1f %% van de figuur'%(100*(o==1).sum()/fg.sum()))
