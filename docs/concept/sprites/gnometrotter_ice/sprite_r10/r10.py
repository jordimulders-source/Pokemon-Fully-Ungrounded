# Ice r10 = r9 + de 13 lijnpixels uit eindkeuring_r9/KEURING.md
from PIL import Image
im=Image.open('../sprite_r9/gnometrotter_ice.png'); p=im.load()
fix=[((22,6),3,2),((19,11),3,2),((51,16),3,2),((15,26),1,2),((16,27),1,2),((17,37),1,2),((18,38),1,2),((18,39),1,2),
     ((18,47),1,9),((19,48),1,9),((39,49),1,9),((40,50),1,9),((41,51),1,9)]
for (x,y),a,b in fix:
    assert p[x,y]==a,(x,y,p[x,y]); p[x,y]=b; print(x,y,a,'->',b)
im.save('gnometrotter_ice.png'); im.resize((512,512),Image.NEAREST).save('gnometrotter_ice_8x.png')
