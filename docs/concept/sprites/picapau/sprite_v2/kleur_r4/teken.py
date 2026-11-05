"""Ronde 4: afwerking vanaf kleur_r3 (niet opnieuw begonnen).
Bevroren uit r3 (diff 0, zie controle.py): oog, wang, vleugelstippen, staart, palet; de vleugel zelf blijft ook r3.
Nieuw: kuifkegels breed aan de basis, achterkuif als drie afgeronde lobben, kop zonder bruine barsten,
vollere snavel, bolle borst/buik (omtrek tot 2 px buiten het silhouet), ronde buikonderkant, poten + tenen.
Per rij: (x, tekens); de rij wordt eerst gewist van x=CLR[0] tot (niet t/m) CLR[1]."""
R3 = [l.rstrip('\n') for l in open('../kleur_r3/raster.txt')][:64]
G = [list(r) for r in R3]
# wisgrens per rij: tot waar r4 de rij overschrijft (rechts daarvan blijft r3: vleugel en staart)
WING = {25: 36, 26: 35, 27: 34, 28: 34, 29: 33, 30: 33, 31: 33, 32: 34, 33: 35, 34: 36, 35: 41, 36: 43,
        37: 44, 38: 44, 39: 44, 40: 45, 41: 45, 42: 45, 43: 46, 44: 47, 45: 44, 46: 44}
S = {
 3:  [(34, 'k')],
 4:  [(33, 'kk'), (38, 'k')],
 5:  [(32, 'kGk'), (37, 'kk')],
 6:  [(31, 'kGGk'), (36, 'kGk')],
 7:  [(30, '42Gk'), (35, 'kGGk')],
 8:  [(29, '4122k'), (35, '423k')],
 9:  [(28, '4112223333k')],
 10: [(27, '4111222333k')],
 11: [(27, '41112223333kk')],
 12: [(25, '442222222333333k')],
 13: [(23, '44211122222333333k')],
 14: [(21, '4421111122223333' + '3kk')],
 15: [(20, '42111111222223333k')],
 16: [(18, 'k4211111222222333' + '33kk')],
 17: [(14, 'GG'), (17, 'kG2111122222223333333' + '33kk')],
 18: [(15, 'Ghhg21111'), (24, '3kk3'), (28, '2222333333' + '3333k')],
 19: [(16, 'Gghhg122'), (24, 'Gwkk'), (28, '2222333333'), (38, 'kkkk')],
 20: [(17, 'GghGG22'), (24, 'kkGk'), (28, '222333333k')],
 21: [(17, 'kgghG32'), (24, '3kk3'), (28, '22333333k')],
 22: [(18, 'kggGG322222233333333' + 'k')],
 23: [(18, 'kgGGG32'), (25, 'ccc'), (28, '23333333333kk')],
 24: [(19, 'kGGk32'), (24, 'ccccc'), (29, '333333333333k')],
 25: [(20, '4332'), (24, 'ccccC'), (29, '3333333')],
 26: [(21, '433'), (24, 'ccCCC'), (29, '333333')],
 27: [(22, '433'), (25, 'CCC'), (28, '333333')],
 28: [(23, '44443333333')],
 29: [(25, '42222223')],
 30: [(24, '421112223')],
 31: [(24, '411111223')],
 32: [(24, '4111122233')],
 33: [(24, '42112222333')],
 34: [(24, '422222233333')],
 35: [(24, '42222223333333333')],
 36: [(25, '422222333333333333')],
 37: [(25, '4222233333333333333')],
 38: [(26, '422233333333333333')],
 39: [(26, '422322233333333333')],
 40: [(27, '432112233333333333')],
 41: [(27, '422112223333333333')],
 42: [(28, 'k2222333333333333')],
 43: [(29, 'k3333333333333333')],
 44: [(30, 'kkk33333333333333')],
 45: [(31, 'gGkkkkk333333')],
 46: [(31, 'gG'), (34, 'GG'), (38, 'kkkkkk')],
 47: [(31, 'gG'), (34, 'GGGGk')],
 48: [(27, 'kggggG')],
 49: [(32, 'Gggk')],
}
for y, segs in S.items():
    x1 = WING.get(y, 44)
    x0 = 13
    for x in range(x0, x1):
        G[y][x] = '.'
    if y >= 47:                      # onder het lijf: alleen x<44 wissen (staart blijft)
        pass
    for x, s in segs:
        for i, c in enumerate(s):
            G[y][x + i] = c
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in G) + '\n')
print('\n'.join('%2d ' % y + ''.join(G[y][14:54]) for y in range(2, 59)))
