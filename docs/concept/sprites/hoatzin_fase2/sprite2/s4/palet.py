# palet.py: spritepalet = modeltinten, alleen helderheid uit elkaar getrokken (±30-40 stappen)
PAL = [(255, 255, 255),   # 0 transparant
       (16, 14, 24),      # 1 lijn
       (106, 106, 144),   # 2 vleugel licht (penrand)
       (70, 70, 104),     # 3 vleugel midden (vlak)
       (40, 38, 62),      # 4 vleugel schaduw
       (244, 236, 212),   # 5 creme licht
       (190, 180, 156),   # 6 creme schaduw
       (184, 136, 188),   # 7 krop licht
       (146, 96, 148),    # 8 krop midden
       (98, 58, 104),     # 9 krop schaduw
       (168, 100, 68),    # 10 kuif (hoofdtint)
       (116, 56, 40),     # 11 kuif schaduw
       (110, 150, 194),   # 12 blauw
       (112, 110, 104),   # 13 grijs midden (schaduw/selout snavel en poten)
       (196, 60, 52),     # 14 rood
       (156, 154, 146)]   # 15 grijs licht
# modelklasse (klassen.py) -> paletindex
MAP = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 14, 13: 14, 14: 15, 15: 13, 16: 1, 17: 14, 18: 14, 19: 14}
SELOUT = {'creme': 6, 'krop': 9, 'kuif': 11, 'grijs': 13}
DONKER = SELOUT
