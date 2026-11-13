# gemiddelde helderheid van het model (natief lijf, en 2x verkleind) als maat voor de sprite
import numpy as np
from PIL import Image
a = np.asarray(Image.open('../natief_zonder_wangoog.png').convert('RGB')).astype(float)
lum = a @ [0.299, 0.587, 0.114]
body = a.min(2) < 215
print('model natief lijf %.1f' % lum[body].mean())
im = Image.open('../natief_zonder_wangoog.png').convert('RGB').resize((66, 66), Image.BOX)
b = np.asarray(im).astype(float); l2 = b @ [0.299, 0.587, 0.114]; m2 = b.min(2) < 225
print('model 2x verkleind (box) %.1f' % l2[m2].mean())
