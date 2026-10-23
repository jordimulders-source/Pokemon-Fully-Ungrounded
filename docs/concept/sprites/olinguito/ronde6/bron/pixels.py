# Olinguito ronde 6, per pixel met de hand. Per regel: (y, x, 'pixels'); '_' = laat staan, '.' = transparant.
# Lagen: staart, lijf, voeten, hoofd (incl. oren, masker, ogen, snuit).
# Skelet: Teddiursa (zithouding, ronde kop, verhouding kop/lijf); kop iets gekanteld (dichtbij-oor lager, masker schuin).

# ---- staart: haak bovenaan (krult naar links, rechts van het verre oor), daarna een flauwe S naar de rug
HOOK = [
    (2, 38, "55555"),
    (3, 36, "552112255"),
    (4, 35, "52221122335"),
    (5, 35, "5223FFFF334F"),
    (6, 35, "5233F..5234F"),
    (7, 35, "5233F..5234F"),
    (8, 35, "59AAF..5234F"),
    (9, 35, "F9AAAF.5234F"),
    (10, 36, "FAAF"),
    (11, 37, "FF"),
]
HOOK2 = [  # frame 2: de haak zwaait open, klaar om te grissen
    (2, 38, "55555"),
    (3, 36, "552112255"),
    (4, 35, "52221122335"),
    (5, 35, "5223FFFF334F"),
    (6, 35, "5233F..5234F"),
    (7, 34, "F59AF...5234F"),
    (8, 33, "F9AAF....5234F"),
    (9, 32, "FAAF......5234F"),
    (10, 32, "FF"),
]

def tail_x(y):
    if y <= 20: return 42
    if y <= 35: return 43
    if y <= 38: return 42
    if y <= 40: return 41
    return 40 - (y - 41)

RINGS = {13, 20, 27, 34, 41}
TAILV = []
for _y in range(10, 46):
    if _y in RINGS:
        _f = "29A"          # ring loopt schuin: links een rij lager
    elif _y - 1 in RINGS:
        _f = "9AA"
    elif _y - 2 in RINGS:
        _f = "934"
    elif _y % 7 == 0:
        _f = "134"
    else:
        _f = "234"
    _x = tail_x(_y)
    if _y >= 24:                     # staart wordt naar de basis toe dikker (4 i.p.v. 3 vacht)
        _f = {"29A": "299A", "9AA": "99AA", "934": "9334", "134": "1334", "234": "2334"}[_f]
        _x -= 1
    TAILV.append((_y, _x, ("5" if _y < 30 else "F") + _f + "F"))
TAILV += [(46, 33, "F4445F"), (47, 34, "FFFF")]
SHIFT = (3, 5)

# ---- lijf (zit, driekwart naar links): armen schuin naar de gevouwen klauwen, dijen links en rechts
def R(t):
    return t.replace(' ', '')

# lijf in driekwart: buik naar links verschoven, rug/zijkant rechts in de schaduw, grote dichtbij-dij linksonder,
# dichtbij-arm schuin naar de poten, verre poot half erachter. Elke regel met de hand, per pixel.
BODY = [
    (34, 17, R("4 2 2 2 2 2 2 2 4 4 4 4 4 5 F")),
    (35, 16, R("4 2 2 1 2 7 7 7 7 3 3 3 4 4 4 5 F")),
    (36, 15, R("4 2 2 2 5 6 7 7 7 8 3 3 3 3 4 4 4 5 F")),
    (37, 14, R("4 2 2 3 2 2 5 6 7 7 8 3 5 3 3 4 4 4 5 F")),
    (38, 13, R("5 2 2 3 3 2 3 2 F F F F 5 3 3 3 4 4 4 4 5 F")),
    (39, 13, R("5 2 3 3 3 2 3 F 9 9 9 A F 9 A F 3 4 4 4 5 F")),
    (40, 13, R("5 2 3 3 3 3 4 F 9 9 A A F A A F 3 3 4 4 5 F")),
    (41, 13, R("5 3 3 3 3 4 7 F 6 E 6 F 7 6 F 8 3 3 4 4 5 F")),
    (42, 13, R("F 2 2 2 3 3 5 7 6 F 6 7 7 F 8 8 3 3 4 4 5 F")),
    (43, 13, R("F 2 2 3 3 3 3 5 F 7 F 7 8 8 8 8 5 3 4 4 5 F")),
    (44, 13, R("F 2 3 3 3 3 4 4 5 8 8 8 8 8 8 5 3 3 4 4 4 F")),
    (45, 14, R("F 3 3 4 4 4 4 5 8 8 8 8 8 5 4 4 4 4 5 F")),
    (46, 15, R("F 4 4 4 4 5 F 8 8 8 5 F 4 4 4 5 5 F")),
    (47, 17, "F" * 15),
]

FEET = [
    (45, 10, "FFFF"),
    (46, 9, "F9999AF"),
    (47, 8, "F99999AAF"),
    (48, 8, "F6A6A6AAF"),
    (49, 9, "FFFFFFF"),
    (46, 25, "FFFF"),
    (47, 24, "F999AF"),
    (48, 24, "F6A6AF"),
    (49, 25, "FFFF"),
]

# ---- hoofd: ronde teddybeerkop, licht gekanteld; masker = schuine vachtband (bovenrand licht, onderrand donker);
#      ogen kijken opzij (naar de staart); korte creme snuit met scheve grijns en hoektand
HEAD = [
    (9, 29, "4445"),
    (10, 28, "52334F"),
    (11, 28, "537884F"),
    (12, 13, "4444"), (12, 28, "537884F"),
    (13, 12, "422335"), (13, 28, "538844F"),
    (14, 11, "5277835"), (14, 20, "44445555"), (14, 28, "38444F"),
    (15, 11, "527883"), (15, 17, "45221122223345"), (15, 31, "44F"),
    (16, 11, "52884"), (16, 16, "422111122233334F"), (16, 32, "4F"),
    (17, 12, "528"), (17, 15, "52221122223333344F"),
    (18, 13, "5"), (18, 14, "5222222232333333444F"),
    (19, 14, "5222232333339999999F"),
    (20, 13, "5222223" + "999999" + "FFF" + "999" + "AF"),
    (21, 13, "A99FFF9" + "99999" + "FDBFF" + "999AF"),
    (22, 13, "A9FDBFF" + "99999" + "FBCFF" + "99AAF"),
    (23, 13, "A9FBCFF" + "99999" + "AFFA" + "AAAAF"),
    (24, 13, "A99FFF9" + "AAAAAA" + "3333" + "4444F"),
    (25, 10, "555AAAAAAA33233333344445F"),
    (26, 9, "56666777" + "3333333333343" + "4445F"),
    (27, 8, "FF6677778" + "333333333434" + "44455F"),
    (28, 8, "FF77777F8" + "33333333434" + "444455F"),
    (29, 9, "57FFFF88" + "333333434" + "4444455F"),
    (30, 10, "57D8884" + "4333343" + "444444555F"),
    (31, 11, "558844" + "43334" + "4444444" + "555F"),
    (32, 13, "55F" + "444444544444" + "555F"),
    (33, 17, "F55" + "4" * 6 + "5555F"),
    (34, 20, "F" * 8),
]

# ---- losse accentpixels (glans, vachtvlekjes, neusglans), met de hand gezet
POLISH = [
    (13, 14, "1"), (27, 9, "D"),
    (27, 31, "3"), (29, 28, "4"), (31, 20, "4"), (30, 24, "3"), (25, 29, "4"),
    (26, 18, "22"), (27, 19, "2"), (17, 24, "2"),
]

# kop 2 px naar voren (links) t.o.v. het lijf: de houding wordt een S (kop vooruit, lijf, staart naar achteren)
HEAD_DX = -2
HEAD = [(y, x + HEAD_DX, s) for y, x, s in HEAD]
POLISH = [(y, x + (HEAD_DX if y <= 33 else 0), s) for y, x, s in POLISH]

FRAME1 = [HOOK, TAILV, BODY, FEET, HEAD, POLISH]
FRAME2 = [HOOK2, TAILV, BODY, FEET, HEAD, POLISH]
