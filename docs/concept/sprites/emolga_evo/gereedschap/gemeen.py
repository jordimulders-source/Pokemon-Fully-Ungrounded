# Gedeelde hulpjes Emolga-evolutie: klassen per natieve modelpixel, palet, opslaan, labels.
# Natief raster 99x99 (pitch 10,238, fase 9,35; natief.py), figuur x16-84, y7-84 (69x78).
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/'
NATIEF=D+'gereedschap/natief.png'
# Modelklassen: 0 bg | 1 K zwart | 2 D donker(33) | 3 E donker2(48) | 4 G grijs(66) | 5 y donkergeel | 6 Y geel midden | 7 L geel licht
#               | 8 B blauwgrijs (194,210,218) | 9 W wit (231,240,245 en ingesloten wit)
KL='.KDEGyYLBW'
MODELKLEUR=[(255,255,255),(1,2,1),(33,33,33),(48,48,47),(66,66,66),(166,140,50),(218,188,62),(241,216,89),(194,210,218),(236,243,248)]
def klassen(path=NATIEF):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    L=a.mean(2); sat=a.max(2)-a.min(2)
    licht=a.min(2)>=235
    lab,n=label(licht,acht=False)
    buiten=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1])
    bg=np.isin(lab,list(buiten))&licht
    c=np.zeros(L.shape,int)
    fg=~bg
    pal=np.array(MODELKLEUR[1:],float)
    d=((a[:,:,None,:]-pal[None,None])**2).sum(-1)
    c[fg]=d[fg].argmin(-1)+1
    return a,c,L
def label(mask,acht=True):
    lab=np.zeros(mask.shape,int); n=0
    nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if acht else [(-1,0),(1,0),(0,-1),(0,1)]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
    return lab,n
def toon(o,ch=KL,y0=0,y1=None,x0=0,x1=None):
    y1=y1 or o.shape[0]; x1=x1 or o.shape[1]
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(ch[v] for v in o[y,x0:x1]))
def rgbk(o,bg=(255,255,255),kleuren=None):
    kleuren=kleuren or MODELKLEUR
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg
    for k in range(1,len(kleuren)): img[o==k]=kleuren[k]
    return Image.fromarray(img)
SCR='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad/'
