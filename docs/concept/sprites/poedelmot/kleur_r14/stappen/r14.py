# r14 (hand): schulpbogen voorvleugel-onderrand, bogen achtervleugel/E, koepel C, rafelige B-top,
# taps uitlopende binnenlijnen, schubjes in het voorvleugelpatroon, klauwtjes met een lijntint en teentje
F={}
def put(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': F[(x0+i,y)]=c
# 1 voorvleugel-onderrand: 3 bogen (dal y36, knik y35, taps 6 op y34)
put(34,45,"677")
put(35,39,"3666337773 3".replace(' ','')+"=")   # 39 3, 40-42 6, 43-44 33, 45-47 777, 48-49 33
put(36,40,"333AA333AA3333AAA")                  # 40-42 boog1, 45-47 boog2, 50-53 boog3
put(37,43,"AA");  put(37,48,"AA"); put(37,54,"33")
# 2 achtervleugel/E: 2 bogen (dal y47)
put(45,45,"3AAAAAAA3")
put(46,45,"33AA33AA3")
put(47,45,"AA33AA33")
# 3 koepel C, rafelige B-top, taps
put(52,37,"333"); put(53,36,"3AAA3")
put(48,24,"3A3A3"); put(47,25,"3=3")
put(51,21,"7"); put(45,40,"6"); put(46,40,"6")
# 4 schubjes voorvleugel (3 px tan met bruine onderrand), grote vlekken weg
put(23,51,"666"); put(24,51,"444")
put(31,46,"766676667")          # 46 7, 47-49 666, 50 7, 51-53 666, 54 7
put(32,46,"744474446")       # 46 7, 47-49 444, 50 7, 51-53 444, 54 6
# 5 klauwtjes: buitenrand 2, teentje 4 binnenin
put(55,19,"4"); put(56,20,"2"); put(55,23,"4")
put(58,25,"24"); put(59,25,"2")
put(60,35,"24242"); put(61,36,"2222")
put(58,43,"2422"); put(59,43,"222")
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
