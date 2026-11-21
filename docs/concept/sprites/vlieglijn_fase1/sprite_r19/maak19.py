# r19 = r18 met de twee linker voorpoten als geheel s px naar achteren (rechts) verschoven
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
GRENS={40:24,41:24,42:23,43:22,44:21,45:21,46:21,47:21,48:21,49:21,50:21,51:20,52:20,53:19,54:19,55:19,56:19,57:19}
def poten(a):
    A=set();B=set()
    for (x,y) in ((22,39),(23,39),(24,39)): A.add((x,y))
    for y in range(40,58):
        for x in range(8,28):
            if a[x,y]==0: continue
            if y<=42 and x>=27: continue          # middenpoot
            if y==40 and x==27: continue          # rand
            (B if x>=GRENS[y] else A).add((x,y))
    return A,B
def maak(sA,sB,vanaf=46):
    src=Image.open('sprite_r18/vlieg_r18.png'); a=src.load()
    im=src.copy(); b=im.load()
    A,B=poten(a)
    vast={(x,y) for x in range(64) for y in range(64) if a[x,y] and (x,y) not in A|B}
    for p in A|B: b[p]=0
    # volgorde: verre voorpoot A, dan nabije voorpoot B ervoor; lijf/rand/middenpoot altijd ervoor
    # B: bovendeel + knieband blijven staan (zit al tegen de middenpoot), alleen onderbeen vanaf rij `vanaf` schuift
    for L,sf in ((A,lambda y:sA),(B,lambda y:sB if y>=vanaf else 0)):
        for (x,y) in L:
            q=(x+sf(y),y)
            if q in vast: continue
            b[q]=a[x,y]
    # kabeltop van A loopt door tot direct onder de rand (geen zwart streepje ertussen)
    for x in range(21,27):
        if b[x,39]==1 and b[x,40] in (9,3) and b[x,38] in (3,4): b[x,39]=b[x,40]
    # vrijgekomen randjes: lijf/rand dat nu boven transparant ligt krijgt omlijning
    for x in range(20,28):
        for y in range(38,41):
            if b[x,y]==0 and any(b[x+dx,y+dy] in (2,3,4) and (x+dx,y+dy) in vast for dx,dy in ((0,-1),(1,0),(-1,0))): b[x,y]=1
    return im,A,B
if __name__=='__main__':
    for n,sA,v in (('p1',1,46),('p2',2,43)):   # p2: knieband van B schuift mee, anders botst hij op die van A
        im,A,B=maak(sA,1,v)
        im.save('sprite_r19/vlieg_r19_%s.png'%n,transparency=0)
        onbg(im).resize((512,512),Image.NEAREST).save('sprite_r19/vlieg_r19_%s_8x.png'%n)
