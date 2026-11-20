# r10 opnieuw bouwen: model per cel -> lagen/pennen -> kop -> kuif -> poten -> vel
set -e
python3 modelcel.py
python3 bouw.py
python3 kop.py
python3 kuif.py
python3 poten.py
python3 -c "
from PIL import Image; im=Image.open('hoatzin.png'); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
p=im.getpalette()[:48]
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%tuple(p[i:i+3]) for i in range(0,48,3)))"
python3 vel.py
