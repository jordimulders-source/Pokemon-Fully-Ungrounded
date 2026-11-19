# r5 stap 2: wolbogen in de omtrek, alleen op de gemeten plekken (profiel.py op model_v3; NOTITIES.md).
# + = pixel erbij (boog naar buiten), - = pixel weg (inkeping tussen twee bogen). Nieuwe pixels krijgen vacht 5 (stap 3 zet tonen/lijnen).
import numpy as np
a = np.load('stap1.npy')
PLUS = {
    'rug (kleed over een wolbult, model top 26,90/26,71/26,71 bij x 35-37)': [(35, 26), (36, 26), (37, 26)],
    'rug (wolboog x 44-45, model top 26,90/26,71)': [(44, 26), (45, 26)],
    'halsvoor (boog rij 24-25, model 12,50/12,53)': [(12, 25)],
}
MIN = {
    'rug (inkeping x 42-43, model 27,44/27,76)': [(42, 27)],
    'rug (inkeping x 49 voor de staart, model 27,35)': [(49, 27)],
    'achterwerk (inkeping rij 35 onder de staart, model 49,34)': [(49, 35)],
    'achterwerk (inkeping rij 40, model 49,18)': [(48, 40)],
    'achterwerk (inkeping rij 43-44, model 48,58/48,55)': [(48, 43), (48, 44)],
    'buik (inkeping x 29, model 47,58)': [(29, 47)],
}
for k, pts in PLUS.items():
    for x, y in pts:
        assert a[y, x] == 0, (k, x, y); a[y, x] = 1 if 'kleed' in k else 5
for k, pts in MIN.items():
    for x, y in pts:
        assert a[y, x] != 0, (k, x, y); a[y, x] = 0
np.save('stap2.npy', a); print('erbij', sum(map(len, PLUS.values())), 'weg', sum(map(len, MIN.values())))
