# Telt per zone de pixels die afwijken van de kale reductie (geschrapt samengesteld model, paletindex).
import numpy as np; from PIL import Image
K=np.load('claydol_sprite_r1/kaal.npy'); S=np.load('claydol_sprite_r1/sprite.npy')
Z=np.full((64,64),'kop',dtype='<U8')
Z[40:64,14:50]='lijf'
Z[33:64,0:15]='staf L'; Z[36:64,48:64]='staf R'
for x0,y0,x1,y1 in [(18,1,27,10),(10,6,17,12),(5,13,12,20),(3,21,9,29),(7,31,14,37),(38,1,46,10),(46,6,52,12),(50,13,58,21),(52,21,59,29),(48,31,55,38)]:
    Z[y0:y1+1,x0:x1+1]='krans'
Z[18:32,8:42]='gezicht'
d=K!=S
for z in ['gezicht','krans','kop','lijf','staf L','staf R']: print(z,int((d&(Z==z)).sum()))
print('totaal',int(d.sum()))
im=Image.open('claydol_sprite_r1/claydol_r1.png'); print(im.mode,im.size,im.info.get('transparency'),len(set(np.asarray(im).ravel())))
