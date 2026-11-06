# r16 (hand): haarstreken in de kraag; voorvleugel: vlakken in nieuwe zachte tan D, krul- en schulplijnen in 5; middenpootje-teentje
F={}
def put(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': F[(x0+i,y)]=c
# 1 kraag: haarplukjes die aan de kinschaduw (y43) hangen, plus een tweede rij korte streken
put(44,16,"AAAAA7AAAA7AAA7AA7AAAAA")
put(45,19,"AA77AAA7AAA77A77A7AAA")
put(46,19,"7AAAAAAAA7AAAAAAA")
put(47,19,"77"); put(47,28,"77"); put(47,32,"A")
# 3 middenpootje: teentje
put(57,33,"4")
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
# 2 voorvleugel (x40-57, y21-34): tan vlakken -> D (gemeten op het model), lijnen (krul_lijnen + krullen) -> 5
LIJN={(48,27),(49,27),(47,28),(46,29),(47,30),(48,30),(49,30),(52,30),(52,26),(53,26),(54,26),(54,27),(51,27),(53,29)}
import os
KL=set(tuple(map(int,l.split(','))) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'krul_lijnen.txt')))
R=[l.rstrip('\n') for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'basis.txt'))]
for y in range(21,35):
    for x in range(40,58):
        if R[y][x]=='6' and (x,y) not in {(58,24)}:
            W.setdefault(y,[]).append((x,'5' if ((x,y) in KL or (x,y) in LIJN) else 'D'))
W.setdefault(33,[]).append((39,"D"))

# achtervleugel ook in D/5 (zelfde tint als de voorvleugel, zoals het model)
H={(46,38),(47,38),(45,39),(46,40),(47,40),(47,42),(48,42),(51,42),(52,42),(45,43),(46,43),(49,43),(50,43),(51,38),(52,39),(52,40),(51,41)}
for y in range(36,45):
    for x in range(40,58):
        if R[y][x]=='6' and (x,y) not in {(55,43),(54,44)}:
            W.setdefault(y,[]).append((x,'5' if (x,y) in H else 'D'))
