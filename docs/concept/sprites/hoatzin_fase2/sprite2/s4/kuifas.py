# kuifas.py: de plukken van de kuif uit het model als 1-px-lijnen: skelet (middellijn) van het kuifvlak in MODEL.png
# (bruine tinten 9/10, inclusief de zwarte lijnen erbinnen), geprojecteerd op het spriteraster. Uit: kuifas.npy
import numpy as np
from scipy import ndimage as nd
from skimage.morphology import skeletonize
kl = np.load('modelklas.npy')
DX, DY = map(float, open('fase_keuze.txt').read().split())
X0, Y0, s = 97, 125, 833 / 62
bruin = np.isin(kl, (9, 10))
bruin[:, 330:] = False; bruin[440:, :] = False         # alleen de kop
bruin = nd.binary_closing(bruin, iterations=3)          # zwarte haarlijnen binnen de pluk dichten
lab, n = nd.label(bruin); sz = nd.sum(bruin, lab, range(1, n + 1))
bruin = lab == (np.argmax(sz) + 1)
sk = skeletonize(bruin)
A = np.zeros((64, 64), int)
for y, x in zip(*np.where(sk)):
    i = int(np.floor((x - X0) / s + 1 - DX)); j = int(np.floor((y - Y0) / s + 5 - DY))
    A[j, i] += 1
np.save('kuifas.npy', A)
for j in range(15, 31): print('%2d ' % j + ''.join('#' if A[j, i] else '.' for i in range(0, 20)))
