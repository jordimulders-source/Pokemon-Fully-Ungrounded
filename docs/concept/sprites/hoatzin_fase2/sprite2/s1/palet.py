# palet.py: spritepalet = modeltinten, alleen helderheid uit elkaar getrokken (±30-40 stappen)
PAL = [(255, 255, 255),   # 0 transparant
       (16, 14, 24),      # 1 lijn
       (88, 88, 116),     # 2 vleugel licht = grijs donker (gedeeld)
       (58, 58, 86),      # 3 vleugel midden
       (36, 34, 54),      # 4 vleugel schaduw
       (244, 236, 212),   # 5 creme licht
       (190, 180, 156),   # 6 creme schaduw
       (184, 136, 188),   # 7 krop licht
       (146, 96, 148),    # 8 krop midden
       (98, 58, 104),     # 9 krop schaduw
       (182, 114, 80),    # 10 kuif licht
       (128, 64, 46),     # 11 kuif donker
       (110, 150, 194),   # 12 blauw
       (72, 104, 150),    # 13 blauw donker (selout)
       (196, 60, 52),     # 14 rood
       (156, 154, 146)]   # 15 grijs licht
# modelklasse (klassen.py) -> paletindex
MAP = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 14, 13: 14, 14: 15, 15: 2}
SELOUT = {'creme': 6, 'krop': 9, 'kuif': 11, 'blauw': 13, 'grijs': 2}
DONKER = SELOUT
