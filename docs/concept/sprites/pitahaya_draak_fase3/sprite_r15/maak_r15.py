# r15 = r14 met de buikpitjes van r10A terug (Jordi: "de stippen op de buik waren eerst beter, kopieer de buik van eerder").
# Alleen pixels in de buikzone (x17-30, y30-43) die r11 t.o.v. r10A veranderde, krijgen de r10A-kleur terug.
from PIL import Image
r10=Image.open('sprite_r10/pitahaya3_r10_A.png'); r11=Image.open('sprite_r11/pitahaya3_r11_D.png'); r14=Image.open('sprite_r14/pitahaya3_r14.png')
def rgb(im,x,y):
    i=im.getpixel((x,y)); p=im.getpalette(); return None if i==0 else tuple(p[3*i:3*i+3])
pal=r14.getpalette(); lut={tuple(pal[3*i:3*i+3]):i for i in range(1,16)}
out=r14.copy(); n=[]
for y in range(30,44):
    for x in range(17,31):
        if rgb(r10,x,y)!=rgb(r11,x,y):
            assert rgb(r14,x,y)==rgb(r11,x,y), (x,y)
            c=rgb(r10,x,y); out.putpixel((x,y),lut[c]); n.append((x,y))
# buiten de zone ongewijzigd
for y in range(64):
    for x in range(64):
        if not(17<=x<=30 and 30<=y<=43): assert out.getpixel((x,y))==r14.getpixel((x,y))
out.save('sprite_r15/pitahaya3_r15.png',transparency=0); print(len(n),'px',n)
