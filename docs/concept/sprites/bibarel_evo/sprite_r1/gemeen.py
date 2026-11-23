# Gedeelde palet- en hulpfuncties voor bibarel_evo sprite_r1
import numpy as np; from PIL import Image
PAL=[(152,208,160),(16,16,16),(96,56,32),(144,92,52),(188,128,74),(220,168,112),(208,176,136),(248,232,200),
     (56,44,36),(96,78,64),(140,120,100),(240,124,60),(192,72,36),(248,248,248),(176,176,168),(224,48,40)]
NAAM=['bg','zwart','bruin-lijn','bruin-donker','bruin-midden','bruin-licht','creme-schaduw','creme','donker-lijn','donker-midden','donker-licht','oranje','oranje-donker','wit','wit-schaduw','rood']
# k-means cluster -> paletindex (eerste toewijzing, plaatsafhankelijke correcties in de bouw)
KM2P={8:1,12:1,3:8,6:9,14:9,13:2,0:3,2:3,17:4,4:5,15:6,16:6,1:7,5:14,9:13,7:10,10:11,11:12}
def opslaan(idx,pad,schaal=None):
    im=Image.new('P',(idx.shape[1],idx.shape[0])); im.putpalette([v for p in PAL for v in p]+[0]*3*(256-len(PAL)))
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if schaal:
        rgb=np.array(PAL,'uint8')[idx]; Image.fromarray(rgb).resize((idx.shape[1]*schaal,idx.shape[0]*schaal),Image.NEAREST).save(pad.replace('.png',f'_{schaal}x.png'))
def laad(pad): return np.asarray(Image.open(pad)).astype(int)
def rgb(idx): return np.array(PAL,'uint8')[idx]
