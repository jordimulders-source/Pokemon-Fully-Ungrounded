# Dump van het verkleinde model in grove modelkleurklassen (alleen om te lezen, niet om te kleuren).
# Y geel  y donkergeel  G lichtgroen  g groen  v donkergroen/olijf  K donker  O oranje(licht) o oranje  R rood  r donkerrood  P roze  W wit  B bruin
import numpy as np, colorsys
from PIL import Image
a=np.asarray(Image.open('model_verkleind63.png').convert('RGBA')).astype(int)
def k(p):
    if p[3]==0: return '.'
    r,g,b=p[:3]/255; h,l,s=colorsys.rgb_to_hls(r,g,b); h*=360
    if l<0.13: return 'K'
    if l>0.78 and s<0.3: return 'W'
    if 60<=h<=160:
        if l<0.3: return 'v'
        return 'G' if l>0.55 else 'g'
    if 38<=h<60: return 'Y' if l>0.58 else ('y' if l>0.38 else 'B')
    if (h>=330 or h<15) and l>0.6: return 'P'
    if h<38 or h>=330:
        if l<0.33: return 'r'
        if h<14 or h>=330: return 'R'
        return 'O' if l>0.6 else 'o'
    return '?'
print('    '+''.join(str(i%10) for i in range(63)))
for y in range(63): print('%2d  '%y+''.join(k(a[y,x]) for x in range(63)))
