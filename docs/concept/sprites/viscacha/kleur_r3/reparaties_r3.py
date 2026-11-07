"""Ronde 3: handwerk op het r2-raster, gestuurd door de Gemini-onderlaag (onderlaag.txt). put(zone,y,x,s); '.' = transparant."""
R2='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r2/raster.txt'
rows=[list(l.rstrip('\n')) for l in open(R2)][:64]
ZONE={}
def put(zone,y,x,s):
    for i,c in enumerate(s):
        rows[y][x+i]=c; ZONE.setdefault((x+i,y),zone)
# A nabij oor: grote binnenschelp zoals Gemini
Z='A oor (Gemini)'
put(Z,14,18,"255B1"); put(Z,15,17,"255CB1"); put(Z,16,16,"255CCB1"); put(Z,17,16,"25BCCB1")
put(Z,18,15,"254BCCB1"); put(Z,19,15,"254BCCB1"); put(Z,20,15,"5544441")
# B wangpluk als sikkel op de kop, kop eigen tapse contour, kaakschaduw
Z='B wangpluk/kopcontour'
put(Z,26,14,"54443398881"); put(Z,27,14,"5444489991"); put(Z,28,14,"5448A992")
put(Z,29,13,"4448AA942"); put(Z,30,13,"448AA9442"); put(Z,31,13,"44AA99442")
put(Z,32,12,"544999442"); put(Z,33,12,"4448832")
put(Z,34,10,"44444433"); put(Z,35,8,"444433333")
# C snuit: wrat weg, mondlijn, neus op de punt
Z='C snuit/kin'
put(Z,33,5,"5"); put(Z,31,4,"2"); put(Z,28,1,"15"); put(Z,29,1,"15"); put(Z,36,5,"FF7777777777")
put(Z,34,3,"2555555"); put(Z,35,4,"2555")
# D rug als boog, lijf licht (Gemini 5), schaduw als sikkel om de bil, buik
Z='D rug/lijf/buik'
put(Z,27,28,"222222..."); put(Z,28,21,"2442222"+"555555"+"2222."); put(Z,29,21,"244"+"5"*14+"222")
put(Z,30,19,"44"); put(Z,30,21,"244"+"5"*17+"22"); put(Z,31,21,"24"+"5"*19+"4"+"2")
put(Z,32,20,"244"+"5"*18+"444"+"2"); put(Z,33,18,"2444"+"5"*19+"444"+"1")
put(Z,34,18,"444"+"5"*19+"4444"+"1"); put(Z,35,16,"3"); put(Z,35,17,"4444"+"5"*19+"4444"+"1")
put(Z,36,17,"4444"+"5"*18+"44444"+"3"+"1")
put(Z,37,24,"5"*15+"4444"+"33"+"1"); put(Z,38,24,"5"*14+"44444"+"33"+"1"); put(Z,39,24,"5"*14+"4444"+"333"+"1")
put(Z,40,24,"4"+"5"*12+"44444"+"3333"+"1")
put(Z,41,24,"44"+"55"+"777"+"55555"+"44444"+"33333"+"1")
put(Z,42,24,"44"+"5"+"77777"+"5555"+"44444"+"333333"+"1")
put(Z,43,24,"44"+"7"*7+"55"+"44444"+"3"*7+"11")
put(Z,44,24,"4"+"7"*9+"5"+"4444"+"3"*7+"1")
put(Z,45,23,"4"+"7"*9+"66"+"4444"+"3"*8+"1")
put(Z,46,23,"4"+"7"*8+"6666"+"44"+"3"*10)
put(Z,47,23,"7"*6+"6"*8+"3"*10)
put(Z,48,23,"1"+"777"+"6"*10+"3"*10)
put(Z,49,23,"1"+"6"*9+"33"+"1"+"44444"+"33333"+"1")
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
