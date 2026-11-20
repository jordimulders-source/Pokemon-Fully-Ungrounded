# telzones.py: per zone hoeveel pixels een andere kleur(index-betekenis) hebben dan s5 (s5-index omgezet naar dezelfde rol in s6; de paletverschuiving zelf telt niet)
import numpy as np
from PIL import Image
OUD = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 9, 8: 10, 9: 11, 10: 13, 11: 14, 12: 15, 13: 7, 14: 8, 15: 6}  # s5-index -> zelfde rol in s6
a = np.vectorize(OUD.get)(np.array(Image.open('../s5/hoatzin.png')).astype(int)); b = np.array(Image.open('hoatzin.png')).astype(int)
z = {'kuif': (0, 17, 18, 31), 'snavel/gezicht': (0, 13, 31, 37), 'nek': (12, 28, 29, 40), 'krop': (19, 35, 38, 49),
     'verre vleugel': (13, 30, 5, 30), 'nabije vleugel': (30, 62, 4, 30), 'lijf': (26, 46, 30, 50), 'staart': (46, 64, 38, 53), 'poten': (14, 46, 50, 62)}
d = a != b
for n, (x0, x1, y0, y1) in z.items(): print('%-15s %3d px anders' % (n, d[y0:y1, x0:x1].sum()))
print('totaal', d.sum())
