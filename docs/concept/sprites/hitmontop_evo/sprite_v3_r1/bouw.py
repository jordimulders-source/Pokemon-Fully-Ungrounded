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
            if (y<37 and not (38<=x<=43 and y>=34)) or (y in (37,38) and 21<=x<=37): g[y][x]=0
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
    # 3a. bovenste deel van Hitmontops rand (naast kaak/wang, boven ooghoogte) weg: daar is het wang, de rand wordt huidlijn
    for y in (36,37,38):
        for x in range(0,15): g[y][x]=0
    for y,b in {39:15,40:14,41:14,42:13,43:13}.items():
        for x in range(0,b): g[y][x]=0
        g[y][b]=5
    for y in range(44,62):
        for x in range(0,13): g[y][x]=0
    # 3b. de onderkant van de rand wordt drie dikke gedraaide lokken die naar de grond hangen (links),
    #     de kegel onder het gezicht wordt kruinhaar met korte lokken, de rechterrand wordt één lok.
    #     Zelfde bruintinten als Hitmontops rand: 3 licht, 4 midden, 5 donker/streep, F lijn.
    H=[ # (rij, x, pixels)   L1 x5-9 | L2 x9-13 | L3 x13-18
     (44, 7,"555555F"),
     (45, 6,"534F344F"),
     (46, 5,"5344F354F"),
     (47, 5,"5345F544F"),
     (48, 5,"5354F344F3"),
     (49, 5,"5544F345F34"),
     (50, 5,"5344F354F34F"),
     (51, 5,"5345F544F344F"),
     (52, 5,"5354F344F3544F"),
     (53, 5,"5544F345F34544"),
     (54, 5,"5344F354F3445F"),
     (55, 5,"5345F544F3454F"),
     (56, 5,"5354F344F3544F"),
     (57, 5,"F445F345FF44F"),
     (58, 6,"FF_5354F_FF"),
     (59, 9,"544F"),
     (60,10,"FF"),
     # kruin: Game Freaks kegel (44455/4544) blijft de basis, loopt nu uit in korte lokken; hoorn klein en licht
     (55,19,"F4544F"),
     (56,19,"F5453F"),
     (57,20,"F44F"),
     (58,21,"FF"),
     (55,25,"F23F"),
     (56,25,"F3F"),
     (57,26,"F"),
     (55,28,"F4454F"),
     (56,28,"F4544F"),
     (57,29,"F45F"),
     (58,30,"FF"),
     # rechterkant: Hitmontops rechterrand wordt één lok tussen kop en steunarm (schaduwkant: donkerder)
     (44,33,"F55F"),
     (45,32,"F445F"),
     (46,32,"F454F"),
     (47,32,"F544F"),
     (48,32,"F444F"),
     (49,32,"F445F"),
     (50,32,"F454F"),
     (51,32,"F544F"),
     (52,32,"F444F"),
     (53,31,"FF445F"),
     (54,31,"FF454F"),
     (55,32,"F544F"),
     (56,32,"F445F"),
     (57,32,"F45F"),
     (58,33,"FF"),
    ]
    for y,x,p in H: txt(g,x,y,[p])
    return g

if __name__=='__main__':
    g=stap1(); save(g,os.path.join(HERE,'stap1.png'))
    g=stap2(); save(g,os.path.join(HERE,'stap2.png'))
    g=stap3(); save(g,os.path.join(HERE,'stap3.png'))
    print(dump(g))
