# r15: basis r14 (= ek2 + arm/koepel/ringen r14). Opnieuw: koepel bovenop (top 5) en beide benen per ring
# zoals de Gen 3-Hitmonlee (ring = 3 rijen: lichte bovenkant, band, ingekeepte onderkant; 1-px donkere boog als
# scheiding; buitenrand per ring een bolletje). Log = alle pixels die van ek2 afwijken, met zone.
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/'
ek=Image.open(D+'eindkeuring/ek2.png'); e=np.array(ek)
r=np.array(Image.open(D+'sprite/r14/r14.png')).copy()
ZONE={}
def zet(y,x,v,why):
    r[y,x]=v; ZONE[(y,x)]=why

# ---- koepel: model top (subpixel) kol 19-25 op 20,8-20,9, kol 17/18/26 op 21,3-21,4 ----
for x in range(20,25): zet(20,x,2,'koepel: toprij 5 px (modeldekking rij 20 = 0,19; ronder dan 1 vlakke run)')
zet(21,26,2,'koepel: kol 26 terug (modeldekking 0,64)')
zet(21,18,2,'koepel'); zet(21,19,2,'koepel')
for x,v in zip(range(20,25),[12,12,11,11,11]): zet(21,x,v,'koepel: binnenkant onder de nieuwe toprij (tinten van rij 22: glasrand c links, b)')
zet(21,25,2,'koepel')

def leg(rows,naam):
    # rows: y -> (Lout, Rout, spec) ; spec = lijst binnenkleuren van links naar rechts
    for y,(L,R,inner) in rows.items():
        xs=[x for x in range(L-3,R+4) if r[y,x]!=0]
        lo,hi=min(xs),max(xs)
        # wis oude beenpixels in het venster (alleen het been: aaneengesloten run rond L..R)
        x=L
        while x-1>=0 and r[y,x-1]!=0 and x-1>=L-2: x-=1
        x2=R
        while r[y,x2+1]!=0 and x2+1<=R+2: x2+=1
        for xx in range(x,x2+1): zet(y,xx,0,naam+': rand per ring')
        zet(y,L,2,naam+': linkerrand selout (lichtkant)'); zet(y,R,1,naam+': rechterrand zwart (schaduwkant)')
        assert len(inner)==R-L-1,(y,L,R,inner)
        for i,v in enumerate(inner): zet(y,L+1+i,v,naam+': ring (Gen 3-bouw)')

# trapbeen: ringen 3 rijen hoog, boog = inkeping (rij s) + middenlijn (rij s+1); been buigt naar links (model)
KB={
 12:(42,48,[15,7,6,5,4]),
 13:(43,47,[6,5,4]),            # onderkant ring, ingekeept
 14:(42,48,[8,3,2,2,5]),        # boog: uiteinden in de inkeping, midden 1 rij lager
 15:(42,48,[15,7,6,5,4]),
 16:(42,46,[6,5,4]),
 17:(41,47,[8,3,2,2,5]),
 18:(41,47,[15,7,6,5,4]),
 19:(42,46,[6,5,4]),
 20:(40,46,[8,3,2,2,5]),
 21:(40,46,[15,7,6,5,4]),
 22:(41,45,[6,5,4]),
}
leg(KB,'trapbeen')
# rij 23 (begin doorschijnend deel): middenlijn van de laatste boog
for x in (42,43,44): zet(23,x,3 if x==42 else 2,'trapbeen: laatste boog in het doorschijnende deel')
# rij 22 kol 40 / 46: ek2 had daar rand; na de inkeping achtergrond (gezet door leg)

# standbeen: zelfde bouw, been loopt licht naar rechts (model)
SB={
 44:(51,56,[7,6,5,4]),
 45:(52,55,[5,4]),
 46:(51,56,[8,3,2,4]),
 47:(51,56,[7,6,5,4]),
 48:(52,55,[5,4]),
 49:(52,57,[8,3,2,4]),
 50:(52,57,[7,6,5,4]),
 51:(53,56,[5,4]),
 52:(52,57,[8,3,2,4]),
 53:(52,57,[7,6,5,4]),
}
leg(SB,'standbeen')

np.save(D+'sprite/r15/idx.npy',r)
im=Image.fromarray(r.astype('uint8'),'P'); im.putpalette(ek.getpalette())
im.save(D+'sprite/r15/r15.png',transparency=0)
im.convert('RGBA').resize((512,512),0).save(D+'sprite/r15/r15_8x.png')
r14log={}
for l in open(D+'sprite/r14/log.txt'):
    xy=l.split(')')[0][1:]; x,y=map(int,xy.split(',')); r14log[(y,x)]=l.split('  ',1)[1].strip()
with open(D+'sprite/r15/log.txt','w') as f:
    n=0
    for y,x in zip(*np.where(r!=e)):
        why=ZONE.get((y,x)) or r14log.get((y,x),'?')
        f.write('(%d,%d) %d -> %d  %s\n'%(x,y,e[y,x],r[y,x],why)); n+=1
print(n,'px t.o.v. ek2; silhouet',((r>0)!=(e>0)).sum(),'kleuren',len(set(r.ravel())-{0}))
