# Jordi (met krabbel): "1 rij weg klopt, alleen deze twee pixels moeten nog weg, en dan de 2 pixels 1 pixel links daarvan worden zwart"
from PIL import Image
import numpy as np
im = Image.open('r3/claydol_eind_r3_1rij.png'); pal = im.getpalette(); A = np.array(im)
assert A[55,44] == 7 and A[56,44] == 7 and A[55,43] == 6 and A[56,43] == 6
A[55,44] = A[56,44] = 0
A[55,43] = A[56,43] = 7
out = Image.fromarray(A, 'P'); out.putpalette(pal)
out.save('r3/claydol_eind_r3.png', transparency=0)
Image.open('r3/claydol_eind_r3.png').convert('RGBA').resize((512,512), Image.NEAREST).save('r3/claydol_eind_r3_8x.png')
