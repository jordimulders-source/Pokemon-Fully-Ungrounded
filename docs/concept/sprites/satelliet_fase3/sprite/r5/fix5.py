# r5 = r4 + MOET-reparaties keuring_r4 (alleen index-wissels + 1 pixel)
from PIL import Image
im=Image.open('../r4/sprite.png'); px=im.load()
fix={2:[(46,21),(38,26),(39,26),(40,26),(33,28),(27,35),(24,37),(50,35),(17,41),(27,34),(17,29),(34,17),(26,20),(30,21),(52,29),(56,30)],
     1:[(22,50),(36,42),(37,43),(37,47),(49,39),(50,40),(37,23)]}
for i,l in fix.items():
    for p in l: px[p]=i
im.save('sprite.png',transparency=0)
im2=Image.open('sprite.png').convert('RGBA'); im2.resize((512,512),Image.NEAREST).save('sprite_8x.png')
print('ok', sum(len(v) for v in fix.values()))
