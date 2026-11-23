# Gedeelde palet- en hulpfuncties voor bibarel_evo sprite_r1
import numpy as np; from PIL import Image
PAL=[(152,208,160),(16,16,16),(96,56,32),(144,92,52),(188,128,74),(220,168,112),(208,176,136),(248,232,200),
     (56,44,36),(96,78,64),(140,120,100),(240,124,60),(192,72,36),(248,248,248),(176,176,168),(224,48,40)]
NAAM=['bg','zwart','bruin-lijn','bruin-donker','bruin-midden','bruin-licht','creme-schaduw','creme','donker-lijn','donker-midden','donker-licht','oranje','oranje-donker','wit','wit-schaduw','rood']
# k-means cluster -> paletindex (eerste toewijzing, plaatsafhankelijke correcties in de bouw)
REF=[((7,4,2),1),((38,29,24),1),((65,52,43),8),((91,77,66),9),((116,86,65),9),((106,68,41),2),((123,80,48),2),((146,94,52),3),((171,115,68),3),
     ((189,129,75),4),((196,138,85),5),((176,142,105),6),((210,177,141),6),((243,225,193),7),((192,189,186),14),((252,252,251),13),
     ((132,129,127),10),((232,114,56),11),((197,81,38),12)]
def _km2p():
    c=np.load('sprite_r1/km.npy'); R=np.array([r for r,_ in REF],float)
    return {k:REF[int(np.argmin(((R-c[k])**2).sum(1)))][1] for k in range(len(c))}
KM2P=_km2p()
def opslaan(idx,pad,schaal=None):
    im=Image.new('P',(idx.shape[1],idx.shape[0])); im.putpalette([v for p in PAL for v in p]+[0]*3*(256-len(PAL)))
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if schaal:
        rgb=np.array(PAL,'uint8')[idx]; Image.fromarray(rgb).resize((idx.shape[1]*schaal,idx.shape[0]*schaal),Image.NEAREST).save(pad.replace('.png',f'_{schaal}x.png'))
def laad(pad): return np.asarray(Image.open(pad)).astype(int)
def rgb(idx): return np.array(PAL,'uint8')[idx]
