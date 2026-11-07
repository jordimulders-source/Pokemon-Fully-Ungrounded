"""Ronde 2: handreparaties op het r1-raster, per zone (zie keuring r1). put(y,x,s): s vanaf kolom x, '.' = transparant."""
R1='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r1/raster.txt'
rows=[list(l.rstrip('\n')) for l in open(R1)][:64]
ZONE={}
def put(zone,y,x,s):
    for i,c in enumerate(s):
        rows[y][x+i]=c; ZONE.setdefault((x+i,y),zone)
# 1 wangpluk naar de wang + achterkant kop zonder banden
Z='1 wangpluk/achterkop'
put(Z,20,15,"5544441"); put(Z,21,10,"555555444441"); put(Z,22,7,"25555555544441")
put(Z,23,6,"255555555444441"); put(Z,24,5,"255555555444441"); put(Z,25,14,"44444")
put(Z,26,14,"54443398881"); put(Z,27,14,"5444399991"); put(Z,28,14,"5444AA9233")
put(Z,29,13,"4444AA99233"); put(Z,30,13,"444AA99233"); put(Z,31,13,"44AA99233")
put(Z,32,12,"4899992334"); put(Z,33,12,"4444442334"); put(Z,34,12,"4444444334")
put(Z,35,12,"4444444444"); put(Z,36,19,"444")
# 2 snuit zonder geel, neus 2 px
Z='2 snuit'
put(Z,26,1,".."); put(Z,27,2,"22555555"); put(Z,28,1,"255555555"); put(Z,29,1,"115555555"); put(Z,31,3,"2")
put(Z,36,6,"F")
# 3 rug: bult en dip weg, een boog, selout aan de lichtkant
Z='3 rug'
put(Z,26,35,"...."); put(Z,27,28,"222222222.")
put(Z,28,22,"33222255555555522")
put(Z,29,21,"233"+"5"*13+"4422")
put(Z,30,20,"2334"+"5"*12+"44444"+"22")
put(Z,31,19,"23344"+"5"*10+"4"*9+"2")
put(Z,32,18,"233"+"4444"+"5"*7+"4444"+"5555"+"4444"+"2")
put(Z,33,18,"2"+"33"+"44444"+"5555"+"444444"+"5555"+"44"+"33"+"1")
put(Z,34,19,"33"+"4"*14+"3"+"4"+"55"+"444"+"33"+"1")
put(Z,35,21,"4"*13+"33"+"4"*6+"33"+"1")
put(Z,36,21,"4"*13+"3"+"4"*8+"33"+"1")
put(Z,37,24,"4"*9+"33"+"4"*8+"33"+"1")
for y in (38,39): put(Z,y,24,"4"*9+"3"+"4"*9+"33"+"1")
put(Z,40,24,"4"*9+"3"+"4"*9+"333"+"1")
put(Z,41,24,"4"*9+"33"+"4"*7+"3333"+"1")
put(Z,42,24,"4"*10+"3"+"4"*7+"33333"+"1")
put(Z,43,24,"4"*11+"3"+"4"*5+"3"*7+"1")
# 4 creme buik als strook langs de onderrand
Z='4 buik'
put(Z,44,24,"444"+"7"*7+"4"+"3"+"4444"+"333333"+"1")
put(Z,45,23,"4"+"4"+"7"*11+"3"+"444"+"3"*7+"1")
put(Z,46,23,"4"+"7"*11+"66"+"3"*11)
put(Z,47,23,"7"+"7"*10+"6666"+"3"*9)
put(Z,48,23,"1"+"7"*8+"66666"+"3"*10)
put(Z,49,23,"1"+"77777"+"6666"+"33"+"1"+"44444"+"33333"+"1")
put(Z,50,24,"1666"+"3"*7+"1"+"44444"+"33333"+"1")
# 5 oren rond, ver oor met binnentint
Z='5 oren'
put(Z,12,6,".22"); put(Z,13,6,"2551"); put(Z,14,6,"25C1"); put(Z,15,5,"255C1")
put(Z,16,5,"254C1"); put(Z,17,5,"244C1"); put(Z,18,5,"24431")
put(Z,12,20,"22."); put(Z,13,19,"2551")
# 6 nabije voorpoot met pols en poot
Z='6 voorpoot'
put(Z,37,17,"6555443"); put(Z,38,17,"6255443"); put(Z,39,17,"6255433")
put(Z,40,17,"6254431"); put(Z,41,17,"6625431"); put(Z,42,17,"6625431")
put(Z,43,18,"625414"); put(Z,44,17,"6254144"); put(Z,45,17,"2554414")
put(Z,46,18,"255414"); put(Z,47,17,"255441"); put(Z,48,17,"25441")
put(Z,49,17,"2421"); put(Z,50,17,"1441")
# 7 staart en voet
Z='7 staart/voet'
put(Z,42,55,"B"); put(Z,43,54,"B"); put(Z,44,53,"B")
put(Z,28,51,"BCCCC4331."); put(Z,29,52,"BCCC44331.")
put(Z,12,57,"A")
put(Z,57,22,"244423331")
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
# nazorg na controle: open rand en dijlijn doorlopend
Z='3 rug'
put(Z,43,47,"1"); put(Z,43,34,"3")
Z='4 buik'
put(Z,44,34,"73")
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
put('3 rug',45,36,"4")
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
