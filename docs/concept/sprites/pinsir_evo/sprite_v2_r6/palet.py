# Palet r6: tinten gemeten in het model (natief_ruw, per kleurgroep), helderheid per vlak afgestemd (zie helderheid.md).
import numpy as np
# modeltinten bruin (mediaan per helderheidsband): L52 (63,48,36), L95 (111,91,69), L125 (146,120,94), L148 (166,143,118)
ANKER = [(30, (36, 26, 19)), (52, (63, 48, 36)), (95, (111, 91, 69)), (125, (146, 120, 94)), (148, (166, 143, 118)), (180, (198, 178, 148))]
def bruin(L):
    Ls = [a for a, _ in ANKER]; c = np.array([c for _, c in ANKER], float)
    rgb = np.array([np.interp(L, Ls, c[:, i]) for i in range(3)])
    l = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return tuple(int(round(v)) for v in np.clip(rgb * L / l, 0, 255))
NIVEAU = {3: 68, 4: 101, 5: 133, 14: 166}     # stappen 33/32/33, donkerste vultint 20 boven lijnbruin
PALET = {
    0: (152, 208, 160),
    1: (30, 21, 15),                 # buitenlijn (model-lijn (44,30,21) iets donkerder: blijft de donkerste)
    2: bruin(50),                    # lijnbruin = donkerste modelbruin (63,48,36)
    3: bruin(NIVEAU[3]), 4: bruin(NIVEAU[4]), 5: bruin(NIVEAU[5]), 14: bruin(NIVEAU[14]),
    6: (194, 174, 137), 7: (227, 212, 178), 8: (245, 236, 200),    # room: model (192,173,136) (227,212,178) (245,234,192)
    9: (80, 32, 31), 10: (108, 48, 44), 11: (140, 74, 63), 12: (164, 98, 82),  # rood: model (86,36,35) (104,45,42) (160,92,77), minder verzadigd dan r5
    13: (244, 232, 170),             # oog: model (244,232,179)
    15: (0, 0, 0),
}
def lijst():
    out = []
    for i in range(16): out += list(PALET[i])
    return out
if __name__ == '__main__':
    for i in range(16): c = PALET[i]; print(i, c, round(0.299*c[0]+0.587*c[1]+0.114*c[2]))
