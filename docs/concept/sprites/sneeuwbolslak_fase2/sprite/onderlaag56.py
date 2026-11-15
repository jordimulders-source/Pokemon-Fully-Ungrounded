# Onderlaag volgens fase 1 (sneeuwbolslak/sprite/onderlaag.py + maattest.py) en Krassault: natief raster (pitch 10,24 -> 81x58)
# -> kwantiseren naar het gemeten palet (sprite/maker/pal.py) -> verkleinen naar 56 breed met vlakgemiddelde -> dichtstbijzijnde paletkleur.
# Silhouet = sprite/sil56_rond.npy (ronde bol, bevroren). Uit: sprite/onderlaag56.txt + .png (8x).
import sys,numpy as np; from PIL import Image
sys.path.insert(0,'sprite/maker'); from pal import PAL
keys=[k for k in PAL if k!='.']; P=np.array([PAL[k] for k in keys],float)
n=np.asarray(Image.open('sprite/natief.png').convert('RGB')).astype(float)
fg=n.sum(2)<735; ys,xs=np.where(fg); n=n[ys.min():ys.max()+1,xs.min():xs.max()+1]; fg=fg[ys.min():ys.max()+1,xs.min():xs.max()+1]
q=P[((n[:,:,None,:]-P[None,None])**2).sum(-1).argmin(-1)]   # natief gekwantiseerd
h0,w0=fg.shape; W=56; H=round(h0*W/w0)
A=fg.astype(np.float32)
R=np.stack([np.array(Image.fromarray((q[...,c]*A).astype(np.float32)).resize((W,H),Image.BOX)) for c in range(3)],-1)
Aw=np.array(Image.fromarray(A).resize((W,H),Image.BOX)); C=R/np.maximum(Aw,1e-6)[...,None]
S=np.load('sprite/sil56_rond.npy'); oy,ox=np.where(S)[0].min(),np.where(S)[1].min()
print('verkleind',W,H,'silhouet box',ox,oy,np.where(S)[1].max()-ox+1,np.where(S)[0].max()-oy+1)
out=[]
for y in range(64):
    r=''
    for x in range(64):
        if not S[y,x]: r+='.'; continue
        yy,xx=y-oy,x-ox
        if 0<=yy<H and 0<=xx<W and Aw[yy,xx]>0.05: r+=keys[int(((P-C[yy,xx])**2).sum(1).argmin())]
        else: r+='c'   # cirkelpixel buiten het model: middentint, maker vult
    out.append(r)
for y in range(64):   # buitenrand = omlijning
    r=list(out[y])
    for x in range(64):
        if S[y,x] and any(not(0<=a<64 and 0<=b<64) or not S[a,b] for a,b in ((y,x+1),(y+1,x),(y,x-1),(y-1,x))): r[x]='#'
    out[y]=''.join(r)
open('sprite/onderlaag56.txt','w').write('\n'.join(out)+'\n')
img=np.full((64,64,3),255,np.uint8)
for y in range(64):
    for x in range(64):
        if out[y][x]!='.': img[y,x]=PAL[out[y][x]]
Image.fromarray(img).resize((512,512),Image.NEAREST).save('sprite/onderlaag56_8x.png')
