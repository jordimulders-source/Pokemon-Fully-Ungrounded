import r8lib as L, sys
UP1=('arcanine',40,3,42,5); UP2=('arcanine',14,4,17,6); LEFT=('arcanine',4,37,7,42)
DOWN=('arcanine',19,47,23,51); RIGHT=('arcanine',54,16,59,23)
STAMPS=[
 (UP2,22,25,False,'kampunt 1'),(UP2,26,26,False,'kampunt 2'),(UP2,29,28,False,'kampunt 3'),
 (LEFT,7,32,False,'franjepluk 1'),(LEFT,7,37,False,'franjepluk 2'),
 (DOWN,9,41,False,'onderpunt 1'),(DOWN,13,42,False,'onderpunt 2'),(DOWN,17,42,False,'onderpunt 3'),
 (RIGHT,21,31,False,'schouderpunten 1'),(RIGHT,19,36,False,'schouderpunten 2'),
]
def bouw(stamps=STAMPS,veld=('arcanine',33,2,60,26,7,23),ss=False):
    v=L.Vorm(); v.veld(*veld,label='vlak: Arcanine rugpluk')
    for sn,dx,dy,fl,lab in stamps: v.rand(*sn,dx,dy,fl,label=lab)
    return v,v.maak(slagschaduw=ss)
if __name__=='__main__':
    v,g=bouw(); L.toon(g); print(L.rechte(g,L.ZONE))
    L.rgba8(g).crop((2,18,38,52)).resize((288,272),0).save(sys.argv[1])
