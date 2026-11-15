# p8: keuring p7 (rugband breder bovenaan, krul dicht) + MAG voorhoofd, toegepast door Claude
from PIL import Image
im=Image.open('p7/welp_p7.png'); px=im.load()
E={(30,33):7,(31,34):7,(32,35):7,(38,40):7,(39,41):3,(16,21):4,(17,21):4,(18,21):4}
for k,v in E.items(): print(k,px[k],'->',v); px[k]=v
im.save('p8/welp_p8.png',transparency=0)
a=Image.open('p8/welp_p8.png').convert('RGBA'); a.resize((512,512),Image.NEAREST).save('p8/welp_p8_8x.png')
