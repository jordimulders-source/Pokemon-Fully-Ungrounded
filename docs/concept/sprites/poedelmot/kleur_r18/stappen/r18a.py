# r18a: golflijn onder de witte rand van de achtervleugel op de modelperiode (±2,5 px, dalen op x47 en x49-50),
# rand erboven in 7; tan plaatje x37-44 y44-51 naar het model (bovenlijn y44, linkerrand diagonaal, rechterrand x44/x43, stippen D)
F={}
def put(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': F[(x0+i,y)]=c
put(44,40,"333")
put(45,45,"77777777")
put(46,44,"3337377333")
put(47,38,"7366DD3AA3A33AA2")
put(48,36,"736666DD3A"); put(48,51,"A"); put(49,51,"D"); put(50,51,"D")
put(49,36,"33666663AA")
put(50,37,"3666663AA")
put(51,36,"66363663")
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
# wortel van de vleugelnaad: model zwart op (38-41,34) en (40,35)
for x in (39,40,41): W.setdefault(34,[]).append((x,'3'))
W.setdefault(35,[]).append((40,'3'))
W.setdefault(33,[]).extend([(41,'D'),(42,'D')])
