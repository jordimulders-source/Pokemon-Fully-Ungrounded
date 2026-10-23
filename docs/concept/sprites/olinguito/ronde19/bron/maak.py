"""Bouwt ../anim_front.png (64x128, geïndexeerd) uit samen_f1.txt + samen_f2.txt en controleert open randen.
Omlijningskleuren: 1 (zwart), 2 (bruin/masker), 9 (klauw-omlijning)."""
from PIL import Image
S='.123456789abcdef'
pal=[tuple(int(v) for v in r.split('#')[0].split()[1:4]) for r in open('palet.txt') if r.split('#')[0].split()]
im=Image.new('P',(64,128)); im.putpalette([c for p in pal for c in p])
tot=[]
for f,naam in enumerate(['samen_f1.txt','samen_f2.txt']):
    L=[l.rstrip('\n') for l in open(naam)]
    assert len(L)==64 and all(len(r)==64 for r in L)
    n=0; lek=[]
    for y in range(64):
        for x in range(64):
            c=L[y][x]
            im.putpixel((x,y+64*f),S.index(c))
            if c=='.': continue
            n+=1
            if c in '129': continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                X,Y=x+dx,y+dy
                if not(0<=X<64 and 0<=Y<64) or L[Y][X]=='.': lek.append((x,y)); break
    print(naam,'oppervlak',n,'open randen',lek)
im.save('../anim_front.png')
