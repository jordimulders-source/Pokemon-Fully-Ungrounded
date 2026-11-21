# r13 = r12, nabije middenpoot (x27-30) begint niet meer hoog in het zwarte borststuk (Jordi, 20 nov:
# "de eerste voorpoot rechts begint ook wat te hoog in het lichaam?"): kabel op rij 37-39 wordt borststuk,
# rij 39 wordt de onderlijn waar de poot onder het lijf vandaan komt.
from PIL import Image
im=Image.open('sprite_r12/vlieg_r12.png'); a=im.load()
for y in (37,38):
    for x in range(26,31): a[x,y]=2
a[26,39]=2
for x in range(27,31): a[x,39]=1
im.save('sprite_r13/vlieg_r13.png',transparency=0)
im2=Image.open('sprite_r13/vlieg_r13.png').convert('RGBA')
bg=Image.new('RGBA',im2.size,(255,255,255,255)); bg.alpha_composite(im2)
bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_r13/vlieg_r13_8x.png')
bg.convert('RGB').crop((8,28,50,62)).resize((42*12,34*12),Image.NEAREST).save('sprite_r13/poten_12x.png')
