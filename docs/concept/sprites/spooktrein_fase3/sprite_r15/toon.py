# hulpje: uitsneden op wit, model op hetzelfde raster
from PIL import Image, ImageDraw; import numpy as np
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
PAL=Image.open(D+'sprite_r14/sprite.png').getpalette()
M=Image.open(D+'model/model.webp').convert('RGB'); K=13.77
def rgb(a,bg=(255,255,255)):
    o=Image.fromarray(np.asarray(a,np.uint8),'P'); o.putpalette(PAL); o=o.convert('RGB'); A=np.array(o); A[np.asarray(a)==0]=bg; return Image.fromarray(A)
def crop(a,box,Z,bg=(255,255,255)): return rgb(a,bg).crop(box).resize(((box[2]-box[0])*Z,(box[3]-box[1])*Z),Image.NEAREST)
def mod(box,Z,dy=0):  # model op het r14-raster; dy=-1 => model 1 rij hoger (koeienvanger)
    x0,y0,x1,y1=box; X=102+(x0-2)*K; Y=71+(y0-2-dy)*K
    return M.crop((int(X),int(Y),int(X+(x1-x0)*K),int(Y+(y1-y0)*K))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def rij(ims,gap=12):
    W=sum(i.size[0] for i in ims)+gap*(len(ims)-1); H=max(i.size[1] for i in ims)
    V=Image.new('RGB',(W,H),(220,220,220)); x=0
    for i in ims: V.paste(i,(x,0)); x+=i.size[0]+gap
    return V
