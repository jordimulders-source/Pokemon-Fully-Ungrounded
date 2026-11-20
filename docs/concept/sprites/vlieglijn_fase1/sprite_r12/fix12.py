# r12 = r11 zonder de horizontale kabel onder het achterlijf (Jordi, 20 nov: optie A).
# Het lijf loopt door tot de onderlijn op rij 41; de achterpoot komt daar onder het achterlijf vandaan.
from PIL import Image
im=Image.open('sprite_r11/vlieg_r11.png'); a=im.load()
donker={5:3,3:2,4:3,2:2,6:4}
for x in range(35,40): a[x,39]=a[x,38]
a[33,39]=2; a[33,40]=2; a[34,40]=1
for x in range(35,39): a[x,40]=donker.get(a[x,39],2)
for x in range(39,42): a[x,40]=1
im.save('sprite_r12/vlieg_r12.png',transparency=0)
im2=Image.open('sprite_r12/vlieg_r12.png').convert('RGBA')
bg=Image.new('RGBA',im2.size,(255,255,255,255)); bg.alpha_composite(im2)
bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_r12/vlieg_r12_8x.png')
bg.convert('RGB').crop((22,30,50,58)).resize((28*16,28*16),Image.NEAREST).save('sprite_r12/poten_16x.png')
r=Image.open('sprite_r11/vlieg_r11.png'); print('diff',[(x,y) for x in range(64) for y in range(64) if r.getpixel((x,y))!=a[x,y]])
# daarna: lichte vlakje onder het lijf (37,43),(38,43) van 5 naar 3 (los tintvlakje).
