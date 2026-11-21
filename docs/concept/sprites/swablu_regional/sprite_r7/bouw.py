# r7 (Jordi 21 nov): "oog wil ik 2 pixels linksboven en linksonder de witte pixel. de pixel rechts van het zwart van het oog mag weg"
# Witte glans (28,28); halotint = index 7 (vogel donker), weg = index 8 (vogel midden). Alleen oog; elders diff 0.
from PIL import Image
for naam,weg in [('A',(30,29)),('B',(29,27))]:
    im=Image.open('sprite_r6/swablu_r6.png').copy()
    im.putpixel((27,27),7); im.putpixel((27,29),7); im.putpixel(weg,8)
    im.save('sprite_r7/swablu_r7%s.png'%naam,transparency=0)
