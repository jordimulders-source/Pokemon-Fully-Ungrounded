# drie.py a.png b.png uit.png : a | b | model, 8x, zelfde uitsnede
import sys; from PIL import Image
from vgl import sprite_rgb, model_crop
ims=[sprite_rgb(p).resize((512,512),Image.NEAREST) for p in sys.argv[1:-1]]+[model_crop(0,0,64,64,8)]
W=Image.new('RGB',(len(ims)*528-16,512),'white')
for i,im in enumerate(ims): W.paste(im,(i*528,0))
W.save(sys.argv[-1])
