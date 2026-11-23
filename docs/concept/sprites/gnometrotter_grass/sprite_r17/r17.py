# Grass r17 = r16 + de 11 lijnpixels uit eindkeuring_r16/KEURING.md
from PIL import Image
im=Image.open('../sprite_r16/gnometrotter_grass.png'); p=im.load()
fix=[((15,26),1,5),((16,27),1,5),((5,37),1,2),((17,37),1,2),((18,38),1,2),((18,39),1,2),
     ((18,47),1,9),((19,48),1,9),((39,49),1,9),((40,50),1,9),((41,51),1,9)]
for (x,y),a,b in fix:
    assert p[x,y]==a,(x,y,p[x,y]); p[x,y]=b; print(x,y,a,'->',b)
im.save('gnometrotter_grass.png'); im.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
