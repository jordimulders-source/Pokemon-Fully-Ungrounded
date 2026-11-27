# r8 = eindkeuring + zichtbare pupillen (Jordi: "bij geen enkel oog is een zichtbaar pupil").
# Links: pupil (10,17) kreeg oogwit erboven, zodat hij niet meer aan wenkbrauw/rand vastzit.
# Rechts: geel links van de pupil (38,5), zodat pupil (39,5) in het geel staat (1 px links van r5).
from PIL import Image
im=Image.open('sprite/eindkeuring/uku_pacha_e.png').copy()
for xy,c in {(10,16):15,(38,5):13}.items(): im.putpixel(xy,c)
im.save('sprite/r8/uku_pacha_r8.png')
