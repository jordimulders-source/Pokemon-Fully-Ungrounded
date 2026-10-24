# Olinguito v2: delen met de hand, (y, x, pixels) absolute coördinaten. Letters: zie PAL in sprite.py.
part('staart', [
    (11, 42, 'BBBBK'),
    (12, 40, 'BBhhbbK'),
    (13, 39, 'BhbKKKsbK'),
    (14, 38, 'BhbK'), (14, 45, 'BhbK'),
    (15, 38, 'BhbK'), (15, 45, 'BhbK'),
    (16, 38, 'BhK'), (16, 46, 'BhbK'),
    (17, 38, 'BhK'), (17, 46, 'BhbK'),
    (18, 39, 'BK'), (18, 46, 'BhsK'),
    (19, 39, 'K'), (19, 46, 'BhsK'),
    (20, 47, 'BbsK'),
    (21, 47, 'BbsK'), (22, 47, 'BbsK'), (23, 47, 'BbsK'),
    (24, 45, 'BBbsK'), (25, 45, 'BhbsK'),
    (26, 45, 'BhbsK'), (27, 45, 'BhbsK'),
    (28, 44, 'BhbsK'), (29, 44, 'BhbsK'),
])
part('lijf', [
    (30, 41, 'BBB'), (30, 44, 'BhbsK'),
    (31, 38, 'BBB' + 'hhhh' + 'bbb' + 'K'),
    (32, 35, 'BBB' + 'h' * 6 + 'bbbb' + 's' + 'K'),
    (33, 30, 'B' + 'h' * 11 + 'b' * 6 + 's' + 'K'),
    (34, 30, 'B' + 'h' * 9 + 'b' * 7 + 'ss' + 'K'),
    (35, 30, 'B' + 'h' * 8 + 'b' * 7 + 'sss' + 'K'),
    (36, 30, 'B' + 'h' * 7 + 'b' * 8 + 'ss' + 'K'),
    (37, 30, 'B' + 'h' * 6 + 'b' * 8 + 'sss' + 'K'),
    (38, 30, 'B' + 'h' * 5 + 'b' * 9 + 'sss' + 'K'),
    (39, 30, 'B' + 'h' * 4 + 'b' * 8 + 'ssss' + 'K'),
    (40, 30, 'B' + 'h' * 4 + 'b' * 8 + 'ssss' + 'K'),
    (41, 30, 'B' + 'h' * 3 + 'b' * 8 + 'sssss' + 'K'),
    (42, 30, 'B' + 'h' * 3 + 'b' * 7 + 'sssss' + 'K'),
    (43, 30, 'B' + 'h' * 2 + 'b' * 7 + 'ssssss' + 'K'),
    (44, 29, 'B' + 'h' * 3 + 'b' * 6 + 'ssssss' + 'K'),
    (45, 33, 'bbbb' + 's' * 7 + 'K'),
    (46, 33, 'bbb' + 's' * 8 + 'K'),
    (47, 33, 's' * 11 + 'K'),
    (48, 41, 'ssssK'),
])
part('dij', [(38, 42, 's'), (39, 41, 's'), (40, 40, 's'), (41, 40, 's'), (42, 40, 's'), (43, 41, 's'), (44, 42, 's')])
part('borst', [(45, 25, 'sss'), (46, 22, 'sssssss'), (47, 25, 'KKKK')])
# verre achterpoot: korte scheen + kleine voet, links van en 1 rij hoger dan de nabije
part('verre_achter', [(46, 36, 'sss'), (47, 35, 'Bsss'), (48, 35, 'KnpnnK'), (49, 35, 'KnpnK'), (50, 36, 'KKK')])
# nabije achterpoot: alleen de voet (bewust bijna verborgen)
part('nabije_achter', [(49, 40, 'BppppnK'), (50, 39, 'KpppKpK'), (51, 39, 'KKKKKKK')])
# verre voorpoot: steiler dan de nabije, klauwen kort en recht omlaag (alleen schaduwtint)
part('verre_voor', [
    (47, 22, 'BsssK'), (48, 22, 'BsssK'), (49, 21, 'BsssK'), (50, 21, 'BnnnK'),
    (51, 21, 'lKlK'), (52, 21, 'lKlK'), (53, 21, 'lKl'), (54, 21, 'K'),
])
part('oor_ver', [(25, 20, 'BB'), (26, 19, 'BlK'), (27, 19, 'BsK')])

# kop: omtrek (y: links, rechts), vulling met licht van linksboven; omlijning B aan de lichte, K aan de schaduwkant
KOP = {26: (23, 27), 27: (21, 29), 28: (20, 30), 29: (18, 31), 30: (17, 32), 31: (16, 33), 32: (16, 33), 33: (15, 34), 34: (15, 34),
       35: (15, 34), 36: (16, 33), 37: (16, 33), 38: (16, 32), 39: (15, 32), 40: (14, 31), 41: (14, 31), 42: (13, 30),
       43: (12, 29), 44: (11, 27), 45: (11, 25), 46: (12, 22), 47: (14, 18)}
rows = []
for y, (L, R) in KOP.items():
    px = ''
    for x in range(L, R + 1):
        inside = lambda yy, xx: yy in KOP and KOP[yy][0] <= xx <= KOP[yy][1]
        up, dn, lf, rt = inside(y - 1, x), inside(y + 1, x), inside(y, x - 1), inside(y, x + 1)
        if not (dn and rt):
            px += 'K'
        elif not (up and lf):
            px += 'B'
        else:
            u = (x - 24) * 0.6 + (y - 34) * 0.8
            px += 'l' if u < -2 else 'f' if u < 6 else 'g'
    rows.append((y, L, px))
part('kop', rows)
# snoet en neus aan de punt, korte mondlijn
part('snoet', [(42, 14, 'mm'), (43, 13, 'mmm'), (44, 12, 'nmmm'), (45, 12, 'nnmm')])
# masker: band, smal bij de snuit, breedst rond het oog, rond eind achter het oog
part('masker', [(36, 22, 'KKKK'), (37, 19, 'K' * 9), (38, 16, 'K' * 14), (39, 15, 'K' * 15), (40, 18, 'K' * 11),
                (41, 22, 'KKKK')])
# oog: pupil tegen de voorrand, glans, donker roodbruin boven, lichter onder
part('oog', [(38, 23, 'Kwee'), (39, 23, 'Krrr')])
part('voorpoot', [
    (45, 28, 'Bhhbbs'), (46, 29, 'Bhhbbs'), (47, 29, 'BhhbbsK'), (48, 30, 'BhhbsK'),
    (49, 29, 'BhhbsK'), (50, 28, 'BhhbsK'), (51, 27, 'BhhbKK'), (52, 25, 'BBhbbK'),
    (53, 24, 'BppppK'), (54, 23, 'BpppnK'),
    # voorste klauw lang, in een haak; achterste korter en steiler: twee verschillende klauwen
    (55, 22, 'clKclK'),
    (56, 21, 'clK'), (56, 25, 'clK'),
    (57, 20, 'clK'), (57, 26, 'lK'),
    (58, 20, 'clK'), (58, 26, 'K'),
    (59, 21, 'lK'),
    (60, 21, 'K'),
])
part('oor', [(23, 27, 'BBB'), (24, 26, 'BlBK'), (25, 25, 'BlllBK'), (26, 25, 'BlllBK'), (27, 25, 'BBBBK')])
part('fix', [(35, 15, 'B'), (44, 28, 'K'), (54, 22, 'K')])
ORDER = ['staart', 'lijf', 'dij', 'borst', 'verre_achter', 'nabije_achter', 'verre_voor', 'oor_ver', 'kop', 'snoet',
         'masker', 'oog', 'voorpoot', 'oor', 'fix']
