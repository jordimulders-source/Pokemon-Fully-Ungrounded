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
 7: [(30, '42Gk'), (35, 'kGGk')],
 8: [(29, '4123k'), (35, '433k')],
 9: [(28, '41123k'), (35, '433k')],
 10: [(27, '411223' + '3k33k')],
 11: [(27, '4' + '2'*6 + '3333kk')],
 12: [(25, '44' + '2'*7 + '3'*6 + 'k')],
 13: [(23, '44' + '1' + '11' + '2'*6 + '3'*6 + 'k')],
 14: [(21, '44' + '1' + '1111' + '2'*6 + '3'*4 + 'kk')],
 15: [(20, '41' + '11111' + '2'*6 + '3'*4 + 'k')],
 16: [(18, 'k41' + '1111' + '2'*8 + '3'*4 + 'kk')],
 17: [(14, 'Ggg'), (17, 'kG2' + '11' + '2'*11 + '3'*6 + 'kk')],
 18: [(15, 'Ghhg22222'), (24, '3kk3'), (28, '2'*5 + '3'*8 + 'k')],
 19: [(16, 'Ghhhg222'), (24, 'Gwkk'), (28, '2'*5 + '3'*5), (38, 'kkk')],
 20: [(17, 'GhhhG22'), (24, 'kkGk'), (28, '2'*4 + '3'*5 + 'k')],
 21: [(17, 'kghhG22'), (24, '3kk3'), (28, '2'*4 + '3'*4 + 'k')],
 22: [(18, 'kggG33' + '2'*7 + '3'*6 + 'kk')],
 23: [(18, 'kggG332'), (25, 'ccc'), (28, '22' + '3'*9 + 'kk')],
 24: [(19, 'kGG33'), (24, 'ccccc'), (29, '3'*12 + 'k')],
 25: [(20, '4333'), (24, 'ccccC'), (29, '3333333')],
 26: [(21, '433'), (24, 'ccCCC'), (29, '333333')],
 27: [(22, '433'), (25, 'CCC'), (28, '333333')],
 28: [(23, '44443333333')],
 29: [(25, '4' + '2'*6 + '3')],
 30: [(24, '42' + '11' + '2'*4 + '3')],
 31: [(24, '42' + '111' + '2'*3 + '3')],
 32: [(24, '42' + '111' + '2'*4 + '3')],
 33: [(24, '42' + '11' + '2'*5 + '33')],
 34: [(24, '4' + '2'*8 + '3'*3)],
 35: [(24, '4' + '2'*8 + '3'*8)],
 36: [(25, '4' + '2'*8 + '3'*9)],
 37: [(25, '4' + '2'*8 + '3'*10)],
 38: [(26, '4' + '2'*7 + '3'*10)],
 39: [(26, '4' + '2'*6 + '3'*11)],
 40: [(27, '4' + '2'*5 + '3'*12)],
 41: [(27, '4' + '2'*4 + '3'*13)],
 42: [(28, 'k' + '2'*2 + '3'*14)],
 43: [(29, 'k' + '3'*16)],
 44: [(30, 'kkk33333333333333')],
 45: [(31, 'gGkkkkk333333')],
 46: [(31, 'gG'), (34, 'GG'), (38, 'kkkkkk')],
 47: [(31, 'gG'), (34, 'GGGk')],
 48: [(27, 'Gggg'), (31, 'gG')],
 49: [(32, 'GggG')],
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
