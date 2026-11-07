"""Ronde 4: handwerk op het r3-raster (r3 PASS, bevroren buiten deze zones). put(zone,y,x,s); '.' = transparant."""
R3='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r3/raster.txt'
rows=[list(l.rstrip('\n')) for l in open(R3)][:64]
ZONE={}
def put(zone,y,x,s):
    for i,c in enumerate(s):
        rows[y][x+i]=c; ZONE.setdefault((x+i,y),zone)
# 1 oog: Drowzee-oog (anim_front x26-32, rij 16-19) pixel voor pixel, herkleurd: 6->1 lidlijn, 7->2/3, C->E (donker oog), F->1 pupil, A->5 vacht
Z='1 oog (Drowzee)'
put(Z,25,10,"52112")
put(Z,26,9,"51EDEE2")
put(Z,27,9,"2E1EE4")
put(Z,28,10,"53333")
put(Z,29,10,"554")
# 2 oren: rondere, bredere schelp (Gemini)
Z='2 oren'
put(Z,12,19,"222.")
put(Z,13,18,"25551")
put(Z,14,17,"255BB1")
put(Z,15,17,"25BCCB1")
put(Z,16,16,"255CCCB1")
put(Z,17,16,"25BCCCB1")
put(Z,12,6,"222"); put(Z,13,5,"25551"); put(Z,14,5,"255C1")
# 3 gele pluk op de snuitpunt (Gemini), klein en vast aan de snuit
Z='3 snuitpluk'
put(Z,26,2,"88"); put(Z,27,2,"899"); put(Z,28,3,"9")
# 4 kleine reparaties
Z='4a staartaanzet'
put(Z,46,54,"1111"); put(Z,47,50,"1111..."); put(Z,48,47,"111.....")
Z='4b verre voet'
put(Z,58,22,"."); put(Z,58,29,"."); put(Z,57,29,"1")
Z='4c scheen'
put(Z,56,45,"24431"); put(Z,57,45,"24431"); put(Z,58,44,"244431")
Z='4d schouder'
put(Z,34,21,"4"); put(Z,35,21,"4"); put(Z,36,21,"44"); put(Z,37,24,"4"); put(Z,38,24,"4"); put(Z,39,24,"4")
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
