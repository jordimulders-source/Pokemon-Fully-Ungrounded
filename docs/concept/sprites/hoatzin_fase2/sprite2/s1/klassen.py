# klassen.py: modeltinten (gemeten in MODEL.png, histogram per zone) en hun spritekleur.
# index 0 = lijn. ZONE groepeert tinten; TOON 0 = licht, 1 = midden, 2 = schaduw.
MODELTINT = [
    (8, 8, 14),        # 0 lijn
    (72, 72, 98),      # 1 vleugel licht
    (48, 48, 70),      # 2 vleugel midden
    (28, 28, 44),      # 3 vleugel schaduw
    (240, 232, 210),   # 4 creme licht
    (176, 168, 150),   # 5 creme schaduw
    (164, 118, 168),   # 6 krop licht
    (144, 94, 144),    # 7 krop midden
    (90, 56, 94),      # 8 krop schaduw
    (158, 102, 80),    # 9 kuif licht
    (136, 72, 52),     # 10 kuif donker
    (104, 142, 182),   # 11 gezicht blauw
    (142, 50, 48),     # 12 oog rood
    (206, 126, 114),   # 13 oog licht (rood)
    (146, 144, 138),   # 14 grijs licht
    (90, 90, 86),      # 15 grijs donker
]
NAMEN = ['lijn', 'vl_l', 'vl_m', 'vl_s', 'cr_l', 'cr_s', 'kr_l', 'kr_m', 'kr_s', 'ku_l', 'ku_d',
         'blauw', 'rood', 'rood_l', 'gr_l', 'gr_d']
ZONE = {0: 'lijn', 1: 'vleugel', 2: 'vleugel', 3: 'vleugel', 4: 'creme', 5: 'creme', 6: 'krop', 7: 'krop',
        8: 'krop', 9: 'kuif', 10: 'kuif', 11: 'blauw', 12: 'oog', 13: 'oog', 14: 'grijs', 15: 'grijs'}
