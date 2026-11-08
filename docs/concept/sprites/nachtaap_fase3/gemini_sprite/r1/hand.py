"""Handwerk op de onderlaag s64.npy: per zone rijen met de hand gezet (elke pixel afgelezen op i128 via pb.py).
'_' = onderlaag houden. Uitvoer: raster.txt"""
import numpy as np, os
from tools import *
a=np.load(os.path.join(G,'s64.npy')).copy(); a[a==10]=11
def put(x0,y0,rows):
    for k,r in enumerate(rows):
        for j,c in enumerate(r):
            if c!='_': a[y0+k,x0+j]=CH.index(c)
# --- KOP (x2..), y25-46
put(2,25,["...11"])
put(2,26,["..191......."])
put(2,27,[".191...11111.191",
          ".191.13333344191",
          ".199122223335991",
          ".1995333333599c1",
          ".19995555559991",
          ".1c9999999999c1",
          "131b999999ccc1",
          "1331b9999ccc1",
          "133661bbb1661",
          "13666666666661",
          "1369f666669fa1",
          "136ae66666aee1",
          "14466888666661",
          "14417777786613",
          ".1417171778133",
          ".1417787778144",
          "..117787788144",
          "...18111881444",
          "....188881",
          ".....11114"])
# --- HAND LINKSBOVEN (x0..), y13-23: topvinger, vinger A, vinger B, duim
put(0,13,[".............",
          "...11111111..",
          "..1bbd999c1..",
          ".111199d9cc1.",
          ".1bb99999ccc.",
          ".1111c9ccccc1",
          ".....1ccccc",
          "...11.1cccc",
          "..1cccccc11",
          "...11ccc114",
          ".....111..11"])
# --- HAND BOVEN (x30..), y4-13: korte vinger x32, vinger 1 x34, vinger 2 x36-37, duim x40, manchet y12
put(30,3,[".............",
          "....1.11.....",
          "...191991....",
          "..11919c1....",
          ".191cdcc1.11.",
          ".19ccdccc191.",
          "..1cccccccc1.",
          "...1ccccccc1.",
          "....1ccccc1..",
          "....111111...",
          "...1444441..."])
# --- GLOEDHAND (x6..x24), y46-62. Tokens per pixel vanaf x6, '_' = houden
def tok(y,x0,s):
    put(x0,y,[s.replace(' ','')])
G6={
46:". 1 1 1 1 4 f f f f f f f f 1",
47:". . 1 1 f f e e 1 1 e e e e f 1",
48:". . . f e e 1 1 9 9 1 1 1 e e f 4",
49:". . . f e 1 9 1 b b 1 9 1 e e e f 3",
50:". . . f e 1 b c 1 b 1 b b 1 1 e e f",
51:". . . f e e 1 c 1 c c 1 c 1 9 1 e f",
52:". . . f e e e 1 c 1 c 1 c 1 9 1 e f",
53:". . f e e e e 1 c 1 c 1 c 1 c 1 e f",
54:". f e e e e e 1 c d b d c d c 1 e f",
55:". f e 1 1 1 e 1 c c c c c c c 1 e f",
56:"f e 1 9 9 b 1 b b c c c c c c 1 e f",
57:"f e e 1 b b b b b b c c b b b 1 e f",
58:". f e e 1 1 b b b b c b b b 1 4 e f",
59:". . f f e e 1 1 b b c b b b 1 4 e f 1",
60:". . . . f e e e 1 1 1 1 1 1 1 1 e f .",
61:". . . . . f f e e e e e e e e f f . .",
62:". . . . . . . f f f f f f f f . . . .",
}
for y,s in G6.items(): tok(y,6,s)
# --- RUGPATROON: modelbogen weg (vacht volgens buren), dan 3 sikkels op de plek van het origineel (af/), +2 px naar rechts
from collections import Counter
R=(slice(29,46),slice(23,44))
for it in range(3):
    for y in range(29,46):
        for x in range(23,44):
            if a[y,x] in (9,10,11,12):
                c=Counter(int(v) for v in a[y-2:y+3,x-2:x+3].ravel() if v in (2,3,4,5))
                if c: a[y,x]=c.most_common(1)[0][0]
def T(rows): return [[(k,c) for k,c in enumerate(r) if c!='.'] for r in rows]
BIG=T(["b99....",".b99...","...99..","...b99.","....b99","....b99","....b99","....99.","...b9..","..b9..."])
SMALL=T(["b99...",".b99..","..b99.","...b99","...b99","...b99","...99.","..b9..",".b9..."])
def boog(x0,y0,Tb):
    for r,row in enumerate(Tb):
        for dx,c in row: a[y0+r,x0+dx]=CH.index(c)
BOGEN=[(23,32,BIG),(29,31,BIG),(35,30,SMALL)]
for b in BOGEN: boog(*b)
# --- VOET (x55..x62), y51-60
G55={56:"1 c b b b b 1 .", 57:". 1 b d b b c 1", 58:". . 1 1 b d c 1",
     59:". . . . 1 b 1 .", 60:". . . . . 1 . ."}
for y,s in G55.items(): tok(y,55,s)
# gloedhand vingers ronde 2: binnenlijnen tussen vingers in handdonker (d), zwart alleen buitenrand/toppen
G11={47:"e e e 1 1 e e e e e",
     48:"e 1 1 9 9 1 1 1 e e",
     49:"1 9 d b b d 9 b 1 e",
     50:"1 b d b c d b c 1 1",
     51:"e 1 c d c c d c d 9 1",
     52:"e e 1 c d c d c d 9 1",
     53:"e e 1 c d c d c d c 1",
     54:"e e 1 c c b c c c c 1"}
for y,s in G11.items(): tok(y,11,s)
# --- ronde 2 reparaties
put(5,25,["11"]); put(3,26,[".191"]); put(3,27,["1991"]); put(3,28,["1991"])   # linkerhoorn maan 2 px
put(7,41,["8"]); put(9,41,["8"])   # neusgaten donkerroze i.p.v. zwart
for y in range(49,61):
    if a[y,22]==14: a[y,22]=10     # rechterkant gloed: middencyaan zoals model (kolom 44-45)
# gloedhand vingers ronde 3: lichte linkerkant per vinger, zwarte lijn rechts (schaduwkant), waaier naar de palm
G11b={47:"e e e 1 1 e e e e e e",
      48:"e 1 1 9 9 1 1 1 e e e",
      49:"1 9 1 9 b 1 9 b 1 e e",
      50:"1 b 1 b c 1 b c 1 1 e",
      51:"e 1 b 1 c 1 b c 1 9 1",
      52:"e e 1 b 1 c 1 c 1 b 1",
      53:"e e 1 b 1 c 1 c 1 c 1",
      54:"e e 1 c d c d c d c 1"}
for y,s_ in G11b.items(): tok(y,11,s_)
# hand linksboven ronde 3: knokkels wit, scheidingslijnen taps (zwart aan de top, d naar binnen)
put(0,15,["..1bb9999c1", ".11dd999ccc1", ".1bb99999ccc", ".1111c99cccc1"])
# --- ronde 3 opschonen (check.py)
def px(x,y,c): a[y,x]=CH.index(c)
for x in range(8,15): px(x,27,'1')            # ovaal bovenrand dicht
px(5,20,'1')                                   # duimnotch dicht
px(4,32,'b'); px(7,34,'b'); px(15,31,'c')      # maanschaduw als doorlopende banden
px(41,34,'4'); px(27,31,'3'); px(12,19,'4'); px(17,25,'4'); px(5,18,'9')
for x,c in zip(range(50,60),"4411144cc1"): px(x,25,c)
px(57,24,'c'); px(47,31,'3'); px(51,35,'3'); px(58,36,'4')
put(7,46,["14444"])                            # vachtband onder de kin (model y46)
for x in range(51,56): px(x,25,'1')
# achterhoofdlijn als doorlopende ')' (model: x18-19 y29-31 -> x20 y32-33 -> x21 y34-39 -> x20 y40-41 -> x19 y42-43 -> x17-18 y44)
for (x,y) in [(18,30),(19,31),(20,32),(20,33),(20,40),(20,41),(19,42),(19,43)]: px(x,y,'1')
# --- OGEN (varianten); hoofdversie = OOG
OGEN={'A':{37:("9f","9fa"),38:("ae","aee")},
      'B':{37:("9f","9ff"),38:("fa","faa"),39:("ae","aee")},
      'C':{37:("9f","9ff"),38:("fa","faa"),39:("e6","6e6")}}
def ogen(v):
    for y,(l,r) in OGEN[v].items():
        put(5,y,[l]); put(12,y,[r])
