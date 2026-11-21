# Verre (linker)vleugel één tint donkerder (Jordi: "luister naar de gidsen voor de linkervleugel").
from PIL import Image
im=Image.open('sprite_r10/rufflet_r10.png'); src=im.copy()
map_={6:7,7:8,8:9}; n=0
for y in range(38,58):
    for x in range(14,24):
        # stop bij het lijf (wit/schaduw/selout van het lijf)
        if any(src.getpixel((xx,y)) in (2,3,4,5) for xx in range(14,x+1)): break
        v=src.getpixel((x,y))
        if v in map_: im.putpixel((x,y),map_[v]); n+=1
print('gewijzigd',n)
im.save('sprite_r11/rufflet_r11.png',transparency=0)
bg=Image.new('RGBA',(64,64),(255,255,255,255))
a=Image.alpha_composite(bg,src.convert('RGBA') if False else Image.open('sprite_r10/rufflet_r10.png').convert('RGBA'))
b=Image.alpha_composite(bg,Image.open('sprite_r11/rufflet_r11.png').convert('RGBA'))
out=Image.new('RGB',(512*2+16+80,512),'white')
out.paste(a.resize((512,512),0),(0,0));out.paste(b.resize((512,512),0),(528,0));out.paste(b,(1056,10))
out.save('sprite_r11/vel.png'); b.resize((512,512),0).save('sprite_r11/rufflet_r11_8x.png')
