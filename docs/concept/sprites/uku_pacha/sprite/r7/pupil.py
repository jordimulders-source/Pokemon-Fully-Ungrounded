# r7: rechterpupil los van de oogrand. A = pupil (39,5), randpixel (38,5) zwart -> koptint 5. B = pupil (39,6), (39,5) geel.
from PIL import Image
for naam,zet in {'A':{(38,5):5},'B':{(39,5):13,(39,6):1}}.items():
    im=Image.open('sprite/r6/uku_pacha_r6.png').copy()
    for xy,c in zet.items(): im.putpixel(xy,c)
    im.save(f'sprite/r7/uku_pacha_r7{naam}.png')
