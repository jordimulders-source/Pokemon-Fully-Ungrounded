# Jordi: "de ogen moeten nog wit". Irispixels (rode tinten rond de pupil) -> wit (index 15), zoals het Lotad-oog.
from PIL import Image
L=[(20,26),(22,26),(21,27)]
R=[(27,26),(29,26),(28,27),(29,27),(28,28),(29,28)]
for n in 'AB':
    im=Image.open('oog_%s.png'%n)
    extra={'A':[(27,27)],'B':[(30,26),(30,27)]}[n]
    for p in L+R+extra:
        if im.getpixel(p) in (4,5,6,7): im.putpixel(p,15)
    im.save('oog_%s_wit.png'%n)
vel=Image.new('RGBA',(2*(240+160)+20,240),(200,200,200,255))
for i,n in enumerate('AB'):
    im=Image.open('oog_%s_wit.png'%n).convert('RGBA')
    vel.paste(im.crop((14,20,44,35)).resize((240,120),Image.NEAREST),(i*410,0))
    vel.paste(im.resize((128,128),Image.NEAREST),(i*410+250,0),im.resize((128,128),Image.NEAREST))
    vel.paste(im,(i*410,140),im)
vel.save('oog_wit_vel.png')
