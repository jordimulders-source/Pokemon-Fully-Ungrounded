# Eindkeuring DFC (c10_1) MOET 1-5 + MAG mondhoek, toegepast door Claude -> af/
from PIL import Image
E={(16,20):2,(22,49):1,(9,34):1,(14,46):3,(21,50):3,(20,37):2}
for t,n in [('','welp'),('_grijs','welp_grijs')]:
    im=Image.open(f'welp/c10/welp_c10_1{t}.png'); px=im.load()
    for k,c in E.items():
        if t=='': print(k,px[k],'->',c)
        px[k]=c
    im.save(f'af/{n}.png',transparency=0)
    Image.open(f'af/{n}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'af/{n}_8x.png')
im=Image.open('af/welp.png'); p=im.getpalette()[:48]
open('af/welp_normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join(f'{p[i*3]} {p[i*3+1]} {p[i*3+2]}\r\n' for i in range(16)))
