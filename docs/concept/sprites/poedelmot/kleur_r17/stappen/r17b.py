# r17b: rechts: vleugelnaad recht (y35), linkerrand achtervleugel naar het model, plaatrand, poot C/D-naad (x40) en D-rechterrand
F={}
def put(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': F[(x0+i,y)]=c
# 3 naad voor-/achtervleugel: rechte lijn y35 x41-51, dan (52-53,36); daaronder vlak dons (geen schulpbogen)
put(35,40,"533333333333")
put(36,40,"3DDAA777AAAA33")
# 4 linkerrand achtervleugel: (41,38),(42,39-41),(41,42),(42,43),(43,44),(44,45)
put(39,41,"73")
put(42,41,"3DD")
put(43,42,"3D")
put(44,42,"A3A")
put(45,40,"3===3A")
put(46,39,"3")
# 5 C/D-naad op x40 (model), C x35-39, D x41-46; D-rechterrand (46,53) dicht
put(52,35,"3663663")
put(53,34,"33333337AAA73")
put(54,34,"3AAAA737AAA773")
put(55,34,"3AAAA737AA666")
put(56,34,"3AAAA73776662")
put(57,39,"77")
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
