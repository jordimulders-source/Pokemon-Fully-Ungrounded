# Meetgereedschap (naar poedelmot px.py/box1x.py): model in spriteruimte, vergelijkingen, px-helderheid.
import sys,numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kay_pacha/'
SRC=Image.open(D+'referenties/gemini_gekozen_r10a.png').convert('RGB')
xy=np.load(D+'sprite/r1/natief_xy.npy'); P=xy[2]
# natieve px n -> 1024: xs0 + n*P (celmidden); celrand = midden - P/2
X0=xy[0]-P/2+26*P; Y0=xy[1]-P/2+21*P; K=162/62*P   # 1024-px per spritepixel
top,left=1,3
GRID=False
def model_box(z=1):
    """model op spriteschaal (BOX), 64x64"""
    bx=(X0-left*K, Y0-top*K, X0+(64-left)*K, Y0+(64-top)*K)
    return SRC.resize((64,64),Image.BOX,box=bx)
def model_crop(x0,y0,x1,y1,z):
    """modeluitsnede overeenkomend met spritevak, op zoom z (LANCZOS)"""
    bx=(X0+(x0-left)*K, Y0+(y0-top)*K, X0+(x1-left)*K, Y0+(y1-top)*K)
    return SRC.resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS,box=bx)
def px(x,y):
    a=np.asarray(SRC.crop((int(X0+(x-left)*K),int(Y0+(y-top)*K),int(X0+(x-left+1)*K),int(Y0+(y-top+1)*K)))).astype(float)
    l=a.mean(2); return l.mean(),np.percentile(l,15),l.max(),a.reshape(-1,3).mean(0)
def rgba(path_or_im,bgc=(255,255,255)):
    im=Image.open(path_or_im) if isinstance(path_or_im,str) else path_or_im
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,bgc+(255,)); b.alpha_composite(im); return b.convert('RGB')
def side(sprite,x0,y0,x1,y1,z,out):
    """sprite | model (zelfde vak) op zoom z, met spritegrid over model"""
    s=rgba(sprite).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    m=model_crop(x0,y0,x1,y1,z); ma=np.asarray(m).copy()
    if GRID: ma[::z,:]=(ma[::z,:]*0.6+np.array([255,0,0])*0.4).astype('uint8');
    if GRID: ma[:,::z]=(ma[:,::z]*0.6+np.array([255,0,0])*0.4).astype('uint8')
    o=Image.new('RGB',(2*(x1-x0)*z+10,(y1-y0)*z),'white'); o.paste(s,(0,0)); o.paste(Image.fromarray(ma),((x1-x0)*z+10,0))
    if out: o.save(out)
    return o
if __name__=='__main__':
    if sys.argv[1]=='px':
        for t in sys.argv[2:]:
            x,y=map(int,t.split(',')); g,p15,mx,c=px(x,y); print(f'({x},{y}) gem {g:.0f} p15 {p15:.0f} max {mx:.0f} rgb {c.round()}')
    elif sys.argv[1]=='side':
        a=list(map(int,sys.argv[3:8])); side(sys.argv[2],*a,sys.argv[8])
