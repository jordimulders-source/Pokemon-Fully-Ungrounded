# Olinguito v2: delen met de hand, (y, x, pixels) absolute coördinaten. Letters: zie PAL in sprite.py.
part('lijf', [
    (30, 39, 'BBBBB'), (30, 44, 'BhbbK'),
    (31, 34, 'BBBBB' + 'h' * 6 + 'bbbb' + 'K'),
    (32, 32, 'BB' + 'h' * 10 + 'bbbb' + 's' + 'K'),
    (33, 30, 'B' + 'h' * 11 + 'b' * 6 + 's' + 'K'),
    (34, 30, 'B' + 'h' * 9 + 'b' * 7 + 'ss' + 'K'),
    (35, 30, 'B' + 'h' * 8 + 'b' * 7 + 'sss' + 'K'),
    (36, 30, 'B' + 'h' * 7 + 'b' * 8 + 'sss' + 'K'),
    (37, 30, 'B' + 'h' * 6 + 'b' * 8 + 'sss' + 'K'),
    (38, 30, 'B' + 'h' * 5 + 'b' * 9 + 'sss' + 'K'),
    (39, 30, 'B' + 'h' * 4 + 'b' * 9 + 'ssss' + 'K'),
    (40, 30, 'B' + 'h' * 4 + 'b' * 8 + 'ssss' + 'K'),
    (41, 30, 'B' + 'h' * 3 + 'b' * 8 + 'sssss' + 'K'),
    (42, 30, 'B' + 'h' * 3 + 'b' * 7 + 'sssss' + 'K'),
    (43, 30, 'B' + 'h' * 2 + 'b' * 7 + 'ssssss' + 'K'),
    (44, 29, 'B' + 'h' * 3 + 'b' * 6 + 'ssssss' + 'K'),
    (45, 33, 'bbbb' + 's' * 7 + 'K'),
    (46, 33, 'bbb' + 's' * 8 + 'K'),
    (47, 33, 's' * 10 + 'K'),
    (48, 35, 'KnnKssssK'),
    (49, 35, 'KKK'),
])
part('dij', [(38, 42, 's'), (39, 41, 's'), (40, 40, 's'), (41, 40, 's'), (42, 40, 's'), (43, 41, 's'), (44, 42, 's')])
part('borst', [(45, 25, 'sss'), (46, 25, 'ssss'), (47, 27, 'KK')])
part('nabije_achter', [(49, 38, 'BppppnK'), (50, 37, 'KppppnK'), (51, 37, 'KKKKKK')])
part('verre_voor', [
    (47, 22, 'BsssK'), (48, 21, 'BsssK'), (49, 20, 'BsssK'), (50, 19, 'BnnnK'),
    (51, 18, 'dcKdcK'), (52, 17, 'dcKdcK'), (53, 17, 'dKKdK'), (54, 17, 'K..K'),
])
part('oor_ver', [(26, 20, 'BBK'), (27, 19, 'BsK')])
part('kop', [
    (27, 22, 'BBBBBBB'),
    (28, 20, 'BllllllllfK'),
    (29, 19, 'BllllllllfffK'),
    (30, 18, 'BlllllllffffffK'),
    (31, 18, 'BllllllffffffffK'),
    (32, 17, 'BllllllfffffffffK'),
    (33, 17, 'BllllffffffffffffK'),
    (34, 17, 'BlllfffffffffffffK'),
    (35, 16, 'BlllfffffffffffffgK'),
    (36, 16, 'BlffffffffffffffgK'),
    (37, 16, 'BfffffffffffffgggK'),
    (38, 15, 'BfffffffffffffgggK'),
    (39, 15, 'BffffffffffffggggK'),
    (40, 14, 'BfffffffffffgggggK'),
    (41, 14, 'BffffffffffggggggK'),
    (42, 13, 'BffffffffffggggggK'),
    (43, 13, 'BffffffffgggggggK'),
    (44, 13, 'ffffffffgggggggK'),
    (45, 13, 'fffffffggggggK'),
    (46, 14, 'ffffggggggK'),
    (47, 15, 'KKKKKKKK'),

])
part('snoet', [(42, 13, 'Bmm'), (43, 13, 'Kmmm'), (44, 13, 'Knmm'), (45, 13, 'Knnm'), (46, 14, 'KnKKK')])
part('masker', [(37, 19, 'K' * 9), (38, 15, 'K' * 15), (39, 15, 'K' * 15), (40, 15, 'K' * 14)])
part('oog', [(38, 24, 'wee'), (39, 24, 'eee')])
part('voorpoot', [
    (45, 28, 'Bhhbbs'), (46, 29, 'Bhhbbs'), (47, 29, 'BhhbbsK'), (48, 30, 'BhhbsK'),
    (49, 29, 'BhhbsK'), (50, 28, 'BhhbsK'), (51, 27, 'BhbbsK'), (52, 26, 'BhbbsK'),
    (53, 25, 'BppppK'), (54, 24, 'BpppnK'),
    (55, 23, 'dcKdcK'), (56, 22, 'dcKdcK'), (57, 21, 'dcKdcK'), (58, 21, 'dcKdcK'),
    (59, 21, 'dK.dK'), (60, 21, 'K..K'),
])
part('oor', [(23, 27, 'BBB'), (24, 26, 'BllBK'), (25, 25, 'BlllBK'), (26, 25, 'BllllK'), (27, 25, 'BllllK')])
ORDER = ['staart', 'lijf', 'dij', 'borst', 'nabije_achter', 'verre_voor', 'oor_ver', 'kop', 'snoet', 'masker', 'oog',
         'voorpoot', 'oor']
