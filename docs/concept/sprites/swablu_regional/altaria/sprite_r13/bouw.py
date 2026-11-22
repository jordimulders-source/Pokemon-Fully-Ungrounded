# r13 (Jordi 21 nov): "vanzelfsprekend dat de kuif meeschuift, je bent wel 2 pixels vergeten mee te schuiven."
# K2 + de twee navy randpixels van de kuifpunt (40,20),(41,20) ook 2 px naar rechts.
from PIL import Image
im=Image.open('sprite_r12/altaria_r12_K2.png').copy()
im.putpixel((42,20),2); im.putpixel((43,20),2); im.putpixel((40,20),0); im.putpixel((41,20),0)
im.save('sprite_r13/altaria_r13.png',transparency=0)
a=Image.open('sprite_r13/altaria_r13.png').convert('RGBA');bg=Image.new('RGBA',(64,64),'white');bg.alpha_composite(a);bg.resize((512,512),Image.NEAREST).save('sprite_r13/altaria_r13_8x.png')
