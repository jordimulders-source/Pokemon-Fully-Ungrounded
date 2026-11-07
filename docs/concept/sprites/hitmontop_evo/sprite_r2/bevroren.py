# Bevroren delen uit ronde 1 (Jordi/keurder): gezicht (ogen, wenkbrauwen, mond, kleine hoorn), steunarm met hand,
# cordão (knoop + hangende einden + eind van de tailleband). Ronde 2 schuift de hele sprite 1 px omhoog (marge onder),
# dus bevroren = pixel voor pixel gelijk met verschuiving (0,-1).
# Maskers in r1-coördinaten.
R1='../sprite_r1/raster.txt'
DY=-1
def r1rows(): return [r.rstrip('\n') for r in open(R1)]
def mask():
    r=r1rows(); m={}
    # gezicht: kop.py lokale rijen 11-21 (gezichtssegmenten) en hoorn (lok. rij 4-6, kol 18-21); r1 = lokaal + (-2,+21)
    import sys; sys.path.insert(0,'../sprite_r1')
    from kop import SEG
    face={11:[(20,"f44445ff")]}
    for y in range(12,22):
        segs=SEG[y]
        # het gezichtssegment is het langste segment dat met 'f' begint en 2/3 bevat
        s=max(segs,key=lambda t:len(t[1].replace(' ','')))
        face[y]=[s]
    face[4]=[(19,"ff")]; face[5]=[(18,"f23f")]; face[6]=[(18,"2334")]
    for y,segs in face.items():
        for x0,s in segs:
            s=s.replace(' ','')
            for i,c in enumerate(s):
                if c!='.': m[(x0+i-2,y+21)]=r[y+21][x0+i-2]
    # steunarm + hand: r1 rijen 46-63, x 31-39
    for y in range(46,64):
        for x in range(31,40):
            if r[y][x]!='.': m[(x,y)]=r[y][x]
    # cordão: knoop en einden (x52-57, y30-41) + rood/donkerrood van de tailleband x>=48, y27-31
    for y in range(27,42):
        for x in range(48,58):
            c=r[y][x]
            if c in 'ab' or (x>=52 and y>=30 and c!='.'): m[(x,y)]=c
    return m
def check(r2file):
    m=mask(); rows=[r.rstrip('\n') for r in open(r2file)]
    diff=[(x,y,c,rows[y+DY][x]) for (x,y),c in m.items() if rows[y+DY][x]!=c]
    return len(m),diff
if __name__=='__main__':
    import sys
    if len(sys.argv)>1:
        n,d=check(sys.argv[1]); print('bevroren pixels:',n,' verschillen:',len(d)); print(d[:20])
    else:
        m=mask(); g=[['.']*64 for _ in range(64)]
        for (x,y),c in m.items(): g[y+DY][x]=c
        open('bevroren.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
