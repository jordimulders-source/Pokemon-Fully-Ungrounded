import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+'/..')
import cfg,numpy as np
from bouw import *
g0=cfg.read(os.path.dirname(os.path.abspath(__file__))+'/../r1/glad.txt')
m=g0>0
L2=np.load(os.path.dirname(os.path.abspath(__file__))+'/../lum2.npy')
G=np.zeros((64,64),int)
for y in range(64):
    for x in range(64):
        if m[y,x]:
            l=L2[y,x] or 60
            G[y,x]=2 if l<72 else 3 if l<94 else 4 if l<117 else 5
def P(x,y,ch): G[y,x]=idx(ch)
def row(y,x,s):
    for i,ch in enumerate(s):
        if ch!=' ': G[y,x+i]=idx(ch); m[y,x+i]= ch!='.'
LIJNEN=[
 [(43,27),(58,27)],
 [(36,30),(36,31),(37,32),(38,33),(39,34),(40,35),(41,36),(41,37),(42,38),(42,39),(41,40)],
 [(43,28),(44,29),(45,30),(46,31),(46,32),(47,33),(47,34),(48,35),(48,36),(49,37)],
 [(50,28),(51,29),(52,30),(53,31)],
 [(58,28),(57,29),(56,30),(55,31),(54,32),(53,33),(52,34),(51,35),(51,36)],
 [(24,35),(23,36),(23,37),(23,38),(23,39),(24,40),(24,41),(25,42)],
 [(29,34),(29,35),(29,36)],
 [(41,41),(40,42),(40,50),(41,51),(41,55)],
 [(42,54),(46,54),(50,54),(53,53)],
 [(33,56),(36,56),(40,57),(44,56),(48,55),(52,54),(54,53)],
]
W=np.zeros((64,64),bool)
for l in LIJNEN:
    for p_,q_ in zip(l,l[1:]):
        for x,y in bres(p_,q_): W[y,x]=True
# meerderheidsfilter dat niet over lijnen kijkt
for _ in range(3):
    H=G.copy()
    for y in range(1,63):
        for x in range(1,63):
            if not m[y,x] or W[y,x]: continue
            w=[G[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if m[yy,xx] and not W[yy,xx]]
            c=np.bincount(w,minlength=16)
            if c[G[y,x]]<=2 and c.max()>=4: H[y,x]=c.argmax()
    G[:]=H
for y in range(64):
    for x in range(64):
        if W[y,x] and m[y,x]: G[y,x]=idx('f')
# gat in de donkere boog
for (x,y) in [(46,46),(46,47),(47,47),(48,47)]: m[y,x]=False; G[y,x]=0
# --- buitenlijn ---
omlijn(G,m)
# --- mantel (met de hand, x28-59) ---
MANTEL={
24:"...............fffffffffff......",
25:"..............f5566555555ffffff.",
26:"..............f44455555555555551",
27:"..............f4444ffffffffffff1",
28:"..........fffffffff555f5555555f1",
29:".......fff56655555f5555f55554f51",
30:".....ff5f5555555544f5554f444f551",
31:"...ff5655f334444555f55444f4f5541",
32:"..f5565554f334444455f544443f5541",
33:".f556655544f334444445f4443f5541.",
34:"ff5655554444f33444444f433f55441.",
35:" f55554444444f34444443f33f54441.",
36:" f554444444444f3444433f311443 1.",
37:" 5555444444444f3444333f1..1111..",
38:" 55544444444444f3333221.........",
}
for y,r in MANTEL.items():
    for i,ch in enumerate(r):
        if ch!=' ': G[y,28+i]=idx(ch); m[y,28+i]=ch!='.'
# --- kop: krul, wratten, verre oog ---
row(34,22,'fffffff')
row(35,21,'f55554f')
row(36,20,'f554f444')
row(37,19,'1f54f4443')
row(38,18,'1cb4f43433')
row(39,18,'1ba4f43f44')
row(40,19,'1f4f4fcc45')
row(41,19,'1cbf4fb145')
row(42,19,'1ba3f4ff44')
row(43,19,'11')
# --- bijna-oog ---
row(38,37,'ffff')
row(39,34,'fff6611f')
row(40,32,'ff55111bb1')
row(41,32,'f11bc1ccbf')
row(42,33,'1bcc1cff')
row(43,34,'fffff')
# --- mondkanon (met de hand, x18-32) ---
MOND={
43:"   11111111111 ",
44:"  1999987979781",
45:" 19111187979781",
46:" 191eee87979781",
47:" 19eddе87978781".replace('е','e'),
48:" 18eede87878771",
49:" 181ee177878771",
50:"  18117777777f1",
51:"   1111111111f ",
}
for y,r in MOND.items():
    for i,ch in enumerate(r):
        if ch!=' ': G[y,18+i]=idx(ch); m[y,18+i]=True
# --- kanon linksboven (na de omlijning, met eigen lijnen) ---
row(38,2,'1111')
row(39,1,'1999811')
row(40,1,'191e87511')
row(41,1,'191e8755511')
row(42,1,'181187445551')
row(43,2,'188774444551')
row(44,3,'177344444551')
row(45,5,'13333444551')
row(46,5,'111111113451')
row(47,13,'1345')
row(48,14,'1345')
row(49,15,'1344')
row(50,15,'1334')
# --- onderste kanon ---
row(50,11,'111')
row(51,8,'1111cb1')
row(52,7,'1cb1111111111111')
for x in range(23,32): P(x,52,'1')
row(53,7,'121999987f555665')
row(53,23,'556666555')
row(54,6,'1219111878f55555'); row(54,22,'5555555554')
row(55,6,'1c191e1878f44444'); row(55,22,'4444444443')
row(56,6,'1b191e1878f4444433'); row(56,24,'33111111')
row(57,7,'1191e17787f43333'); row(57,23,'311')
row(58,7,'1291e17773f33331'); row(58,23,'1')
row(59,8,'181e1777331111')
row(60,10,'11177211')
row(61,11,'11111')
# gebogen voeglijn op de loop
for (x,y,c) in [(17,55,'f'),(16,55,'4'),(17,56,'f'),(16,56,'4'),(18,57,'f'),(17,57,'3'),(16,57,'3')]: P(x,y,c)
cfg.write(G,os.path.dirname(os.path.abspath(__file__))+'/raster.txt')
