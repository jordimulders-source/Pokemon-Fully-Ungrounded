# Hitmontop-evolutie v3: elke stap is een bewerking op de vorige, vertrekpunt = Hitmontops eigen pixels.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

def stap1():
    g=ht()
    # 1a. kop (alles onder de romp) los halen; rechterhand blijft achter en wordt gewist
    def headm(x,y,v):
        if x>=42 and y<=40: return False
        if y in (33,34): return 17<=x<=23
        if y==35 and x<=15: return False
        return y>=35 and x>=8
    head=blank()
    for y in range(64):
        for x in range(64):
            if g[y][x] and headm(x,y,g[y][x]): head[y][x]=g[y][x]; g[y][x]=0
    # hoorn klein: de punt (rij 52-56) eraf, kort stompje terug
    for y in range(52,57):
        for x in range(64): head[y][x]=0
    txt(head,28,51,["F4544F", "_F34F_", "__FF"])
    # rechterrand van de kop (x>44) weg: daar komt de steunarm naast
    for y in range(35,50):
        for x in range(45,64): head[y][x]=0
    # 1b. rechterarm (voor de romp langs) wissen, romp dichtmaken
    for y in range(27,41):
        for x in range(32,52):
            if g[y][x] in (2,3,4,5,1,12,13,14,15): g[y][x]=0
    for y in range(33,35):
        for x in range(15,42):
            if g[y][x] not in (6,7,8,9): g[y][x]=0
    txt(g,31,26,[
      "77777779_",
      "777777779",
      "6777777779",
      "67777777F",
      "77777777F",
      "7777777F",
      "777788F",
      "88888F",
      "FFFF"])
    txt(g,26,34,["FFFF"])
    # 1c. kop verplaatsen: 7 naar links, 6 omlaag (laag naast de steunarm)
    DX,DY=-9,4
    for y in range(64):
        for x in range(64):
            if head[y][x] and 0<=x+DX<64 and 0<=y+DY<64: g[y+DY][x+DX]=head[y][x]
    # kin dicht (waar de oude romp op de kop zat) en een nek naar de romp
    txt(g,15,38,["FFFFFF"])
    for y,x in zip(range(35,39),(28,27,26,24)):
        txt(g,x,y,["F2334F"])
    # 1d. steunarm recht omlaag vanaf de rechterschouder, met Hitmontops eigen hand en polsband
    for y in range(34,56):
        txt(g,38,y,["F5334F"])
    txt(g,38,52,["FC11DF","FCDDEF"])
    hand=["__5555__", "_52233F_", "5222233F", "5222233F", "53223335", "5333334F", "_F3334F_", "__FFFF__"]
    txt(g,37,56,hand)
    return g

def stap2(g=None):
    g=g or stap1()
    # romp, staart, benen, voeten en linkerarm van Hitmontop eraf; de nek en steunarm blijven
    for y in range(0,41):
        for x in range(64):
            if not (38<=x<=43 and y>=37) and y<37 or (y>=35 and 23<=x<=35): g[y][x]=0
    # 2a. lange aansluitende broek: heup (Hitmontops romp, langer) + twee lange benen in V
    txt(g,8,7,[
    ".....99....................................99....",    #7
    "....96699................................99669...",    #8
    "...F66777999...........................99667789..",    #9
    "...F6777777799.......................996677788F..",    #10
    "....F87777777799...................9966777788F...",    #11
    ".....F877777777799...............99667777788F....",    #12
    "......FF877777777799...........996677777788F.....",    #13
    "........F8777777777799.......9966777777888F......",    #14
    ".........FF8777777777799...9966777777788FF.......",    #15
    "...........F877777777777999667777777788F.........",    #16
    "............F8777777777777777777777888F..........",    #17
    ".............FF877777777777777777788FF...........",    #18
    "...............F8777777777777777788F.............",    #19
    "................F87777777777777788F..............",    #20
    ".................F877777777777788F...............",    #21
    "..................F8777777777778F................",    #22
    "...................F87777777778F.................",    #23
    "...................F67777777888F.................",    #24
    "....................9F88888888F..................",    #25
    "......................98888884F..................",    #26
    ])
    # 2b. cordao om de taille (gedraaide rode koord)
    txt(g,27,24,[
      "F6777777888F",
      "_FBAABAABAABF",
      "__FABAABAABAF",
    ])
    # 2c. borst (blote bruine huid, Hitmontops tinten), smal bij de taille, breed bij de schouders
    txt(g,26,27,[
      "..52222333334F....",
      ".5222223333334F...",
      ".52222333343334F..",
      "5222233333433344F.",
      "52222333334333444F",
      "52224444334444344F",
      "52233333443333344F",
      "52223333433333344F",
      "F522233343333344F.",
      ".F5334F2334FFFF4F.",
    ])
    txt(g,22,37,["__F233334F"])
    txt(g,20,38,["__F2333334F"])
    # 2d. Hitmontops eigen voeten, met de hand verkleind (±0,68), met zijn grijze enkelband
    txt(g,0,0,[
      ".........DE..",
      "........DC1E.",
      ".....8887CE..",
      "....86666669.",
      "...8665556669",
      "...8653325669",
      "..86533335679C",
      "..865533456791",
      "..876555567799",
      ".FC97777777F9C",
      "F1CF7777889F1",
      "EFF.F9EC1FF..",
      ".....EC1E....",
      "......EF.....",
    ])
    txt(g,50,3,[
      "....8899......",
      ".EEF666788C11F",
      ".ECF66667911F.",
      "..E9767778C1EF",
      "...9877888CEF.",
      "....F899FF....",
    ])
    return g

def stap3(g=None):
    g=g or stap2()
    O=-2   # kop staat 2 px verder links dan in de analyse (DX -9 i.p.v. -7)
    def X(x): return x+O
    # 3a. het bovenste deel van Hitmontops rand (naast kaak/kin) is wang: haar daar weg, rand wordt huidlijn
    bx={41:17,42:16,43:16,44:15,45:15}
    for y in (38,39,40):
        for x in range(X(4),X(17)): g[y][x]=0
    for y,b in bx.items():
        for x in range(X(4),X(b)): g[y][x]=0
        g[y][X(b)]=5
    # 3b. het onderste deel van de rand blijft (Game Freaks pixels), alleen links ingekort: daaruit groeien de lokken
    rootL={46:12,47:11,48:10,49:10,50:11,51:12,52:14,53:16}
    for y,r in rootL.items():
        for x in range(X(4),X(r)): g[y][x]=0
        if g[y][X(r)] not in (15,): g[y][X(r)]=5
    txt(g,X(12),45,["555"])
    # 3c. dikke gedraaide lokken die met de zwaartekracht naar de grond hangen (afro/Eddy Gordo), zelfde bruintinten
    lock(g,X(8),48,58,phase=0)
    lock(g,X(11),51,60,phase=2,left=15)
    lock(g,X(14),53,59,phase=1,left=15)
    return g

if __name__=='__main__':
    g=stap1(); save(g,os.path.join(HERE,'stap1.png'))
    g=stap2(); save(g,os.path.join(HERE,'stap2.png'))
    g=stap3(); save(g,os.path.join(HERE,'stap3.png'))
    print(dump(g))
