# Model op 1x (vlakgemiddelde per spritepixel, 64x64) en 8x: sprite/meet/model_1x.png, model_8x.png
import numpy as np; from PIL import Image
G=np.load('sprite/gids56.npy'); M=np.load('sprite/sil56.npy')
o=np.full((64,64,3),255,np.uint8); o[M]=G[M].astype(np.uint8)
Image.fromarray(o).save('sprite/meet/model_1x.png'); Image.fromarray(o).resize((512,512),Image.NEAREST).save('sprite/meet/model_8x.png')
# modeluitsnede op exact het 64-raster (8 px per spritepixel), om lijnen over te leggen
c=Image.open('sprite/r8_bol_r7.png').convert('RGB'); S=(973-144)/56
box=(int(144-4*S),int(215-19*S),int(144+60*S),int(215+45*S))
c.crop(box).resize((512,512),Image.LANCZOS).save('sprite/meet/model_raster_8x.png')
