# kijk.py uit.png txt [txt...] : naast elkaar 8x + model-avg, met optioneel rode modelomtrek op de eerste
import sys,numpy as np; from PIL import Image, ImageDraw; from pal import *
avg=np.load('avg.npy'); cov=np.load('cov.npy'); S=int(sys.argv[2]); files=sys.argv[3:]
ims=[rgb(lees(f)) for f in files]+[np.where((cov>=.5)[:,:,None],avg.clip(0,255),232).astype('uint8')]
V=Image.new('RGB',(len(ims)*(38*S+10),61*S),(255,255,255))
for k,r in enumerate(ims): V.paste(Image.fromarray(r).resize((38*S,61*S),Image.NEAREST),(k*(38*S+10),0))
V.save(sys.argv[1])
