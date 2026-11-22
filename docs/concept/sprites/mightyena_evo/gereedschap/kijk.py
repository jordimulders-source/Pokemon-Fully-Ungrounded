# kijk.py SPRITE.png UIT.png: sprite 8x naast Gen 3-Mightyena 8x, plus 1x op wit/donker
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image; import numpy as np; from gemeen import *
def rgbp(im,bg):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); my=Image.open('../../../../graphics/pokemon/mightyena/anim_front_gba.png')
v=Image.new('RGB',(1034,512+80),'white')
v.paste(rgbp(sp,(255,255,255)).resize((512,512),Image.NEAREST),(0,0)); v.paste(rgbp(my,(255,255,255)).resize((512,512),Image.NEAREST),(522,0))
for i,bg in enumerate([(255,255,255),(232,232,216),(40,48,56)]):
    v.paste(rgbp(sp,bg),(i*140,520)); v.paste(rgbp(my,bg),(i*140+68,520))
v.save(sys.argv[2])
