# r12 bouwen vanaf ../r11/hoatzin.png: kuif + verre vleugel -> kop -> nek -> poten -> staart -> opschonen -> check -> vel
set -e
python3 kuif12.py
python3 kop12.py
python3 nek12.py
python3 poten12.py
python3 staart12.py
python3 fix12.py
python3 check.py
python3 -c "
from PIL import Image; im=Image.open('hoatzin.png'); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
p=im.getpalette()[:48]
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%tuple(p[i:i+3]) for i in range(0,48,3)))"
python3 vel.py
