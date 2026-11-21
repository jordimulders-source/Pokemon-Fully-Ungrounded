# r10 = r9 + reparaties van de eindkeuring (keuring_r9): alleen index-wijzigingen, vorm gelijk.
from PIL import Image
im=Image.open('sprite_r9/vlieg_r9.png'); a=im.load()
def zet(pts,new,old=None):
    for x,y in pts:
        if old is None or a[x,y] in old: a[x,y]=new
        else: print('overgeslagen',x,y,a[x,y])
zet([(39,53)],14)                                   # voetje: licht linksboven zoals andere voeten
zet([(36,17),(37,17),(33,18),(34,18),(35,18),(31,19),(32,19),(31,20),(29,21),(30,21),(27,22),(28,22),(27,23),(26,24),(46,17),(45,18)],9,{10,11})
zet([(41,27),(42,27)],12,{11})
zet([(54,19),(55,19)],9,{6})
zet([(30,25)],12,{1})
zet([(13,26)],6,{1})
zet([(11,26),(12,37),(18,37)],1,{4,5})
zet([(32,44)],1,{8}); zet([(39,40)],9,{8})
im.save('sprite_r10/vlieg_r10.png',transparency=0)
im2=Image.open('sprite_r10/vlieg_r10.png').convert('RGBA')
bg=Image.new('RGBA',im2.size,(255,255,255,255)); bg.alpha_composite(im2)
bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_r10/vlieg_r10_8x.png')
r9=Image.open('sprite_r9/vlieg_r9.png'); print('diff',sum(1 for x in range(64) for y in range(64) if r9.getpixel((x,y))!=a[x,y]))
