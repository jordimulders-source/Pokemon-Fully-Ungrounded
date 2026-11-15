"""Hauntflare v8b: mond van v7 blijft (omtrek, maat, plek, opening, tong); alleen tanden VAST aan de lip:
hoofdroze V's die van de bovenlip naar beneden en van de onderlip omhoog steken, zwarte lijn om de tand.
Elke kandidaat = lijst wijzigingen (x, y, index) op v7."""
from PIL import Image
import numpy as np, os
H = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.join(H, '..', 'sprite_v7', 'hauntflare_v7.png')
def rij(y, x0, s): return [(x0 + i, y, int(c, 16)) for i, c in enumerate(s) if c != '.']
# P: 2 boventanden (voet in de lip y33, punt y34, zwarte flanken), 2 ondertanden (voet in de lip y37, punt y36)
P = (rij(33, 24, '1777177711')      # x24-33: lip breekt open voor de tandvoeten; hoek x32-33 zwart
   + rij(34, 24, 'a171a171a')       # x24-32: punten x26, x30 met zwarte flanken
   + rij(36, 24, '71517152')        # x24-31: onderpunten x24, x28 met flanken
   + rij(37, 24, '7717771')         # x24-30: voeten onder, inkeping x26 en x30 zwart
   + rij(38, 27, '77'))             # kinschaduw onder de voet weg: tand vast aan het hoofd
# Q: als P, maar de zwarte lijn alleen aan de schaduwkant (rechts) van elke tandpunt; lichtkant grenst aan het donkerrood/de tong
Q = (rij(33, 24, '1777177711')
   + rij(34, 24, 'aa71aa71a')
   + rij(36, 24, '71557152')
   + rij(37, 24, '7717771')
   + rij(38, 27, '77'))
# R: als P, maar de lijn om de ondertanden in lipdonker 2 (zoals de onderlip van v7 rechts), bovenlijn zwart
R = (rij(33, 24, '1777177711')
   + rij(34, 24, 'a171a171a')
   + rij(36, 24, '72527252')
   + rij(37, 24, '7727772')
   + rij(38, 27, '77'))
# S: als R, maar kleinere ondertanden (zoals de artwork: grote V's boven, kleine golf onder): onderlip blijft zwart, alleen 1 px voet onder elke punt
S = (rij(33, 24, '1777177711')
   + rij(34, 24, 'a171a171a')
   + rij(36, 24, '72527252')
   + rij(37, 24, '7111712')
   + rij(38, 28, '7'))
KAND = {'R': R, 'S': S}  # P en Q afgevallen (zie NOTITIES)
def bouw(n, w):
    im = Image.open(V7); a = np.array(im).copy()
    for x, y, c in w: a[y, x] = c
    out = Image.fromarray(a, 'P'); out.putpalette(im.getpalette())
    p = os.path.join(H, f'kandidaat_{n}.png'); out.save(p, transparency=0); return p
if __name__ == '__main__':
    for n, w in KAND.items(): print(bouw(n, w))
