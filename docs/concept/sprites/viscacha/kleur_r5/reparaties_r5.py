"""Ronde 5: alleen de kop (x0-30, rij 10-42) t.o.v. r4. Gezicht volgens Gemini; het luie oog (r4) blijft. put(zone,y,x,s); '.' = transparant."""
R4='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r4/raster.txt'
rows=[list(l.rstrip('\n')) for l in open(R4)][:64]
ZONE={}
def put(zone,y,x,s):
    for i,c in enumerate(s):
        rows[y][x+i]=c; ZONE.setdefault((x+i,y),zone)
Z='a gele pluk (voorhoofd/neusrug)'
put(Z,25,3,"895"); put(Z,26,1,"88995"); put(Z,27,2,"895"); put(Z,28,1,"8995")
Z='b snuit/neus/mond'
put(Z,29,1,".2"); put(Z,30,2,"25"); put(Z,31,2,"25115"); put(Z,32,3,"215")
put(Z,33,3,"2122")
Z='c kin/keel'
put(Z,34,3,".F777"); put(Z,35,4,"F7766444"); put(Z,36,5,"F77666")
Z='d snorharen'
put(Z,32,0,"BB"); put(Z,33,0,"B")
put(Z,34,2,"BB"); put(Z,35,0,"BB"); put(Z,36,0,"B")
put(Z,36,3,"B"); put(Z,37,2,"B"); put(Z,38,1,"B"); put(Z,39,0,"B")
put(Z,37,11,"FF"); put(Z,38,13,"FF")

# --- aanvulling Jordi: alles zoals Gemini behalve het oog ---
Z='e wangaanhangsel (Gemini)'
put(Z,26,16,"443338881"); put(Z,27,14,"4444389991"); put(Z,28,15,"448AA99132222")
put(Z,29,13,"4448AA991333355"); put(Z,30,13,"448AA9913333355"); put(Z,31,13,"48AA991333335")
put(Z,32,13,"48A991333335"); put(Z,33,12,"444899133345"); put(Z,34,10,"444444899144")
put(Z,35,9,"44433333899914"); put(Z,36,16,"771111")
Z='f snorharen verre kant'
put(Z,39,15,"FF"); put(Z,40,13,"F"); put(Z,41,14,"FF"); put(Z,42,16,"F")
Z='g rug: vachtpiek terug (Gemini-masker)'
put(Z,26,35,"2221"); put(Z,27,28,"2222222551"); put(Z,28,28,"5555555552")
put(Z,29,38,"22."); put(Z,30,40,"22."); put(Z,32,41,"41.."); put(Z,33,41,"441.")
Z='h staart en voet terug naar Gemini-masker'
put(Z,28,51,"BCCCC43311"); put(Z,29,52,"BCCC443331")
put(Z,46,48,"BBCCCCC331"); put(Z,47,47,"CCCCC33311"); put(Z,48,47,"11111111")
put(Z,58,22,"1"); put(Z,58,29,"1"); put(Z,57,29,"3")
Z='i nazorg controle'
put(Z,25,4,"8"); put(Z,31,42,"2"); put(Z,33,22,"3"); put(Z,34,20,"33"); put(Z,36,18,"75")
Z='j lijf/buik als Gemini (smallere buikvlek, minder terracotta op de bil)'
put(Z,40,24,"4"+"5"*12+"4"*7+"33"+"1")
put(Z,41,24,"4455"+"777"+"5"*5+"4"*8+"33"+"1")
put(Z,42,24,"445"+"7"*5+"5"*4+"4"*9+"33"+"1")
put(Z,43,24,"445"+"7"*6+"55"+"4"*10+"33"+"11")
put(Z,44,24,"45"+"7"*8+"5"+"4"*9+"33"+"1")
put(Z,45,23,"455"+"7"*7+"66"+"4"*9+"333"+"1")
put(Z,46,23,"455"+"7"*6+"6666"+"4"*8+"3333")
put(Z,47,23,"444"+"777"+"6"*8+"4"*6+"3333")
put(Z,48,23,"144"+"6"*11+"4"*5+"33333")
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
