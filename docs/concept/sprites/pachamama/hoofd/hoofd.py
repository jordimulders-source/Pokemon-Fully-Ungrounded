# Vergroot alles boven Jordi's rode lijn (gemini/jordi_rode_lijn_hoofd.png) in het natieve model (199x199), anker = laagste punt van de lijn onder het gezicht.
import sys; from PIL import Image; import numpy as np
S=float(sys.argv[1])
J=np.array(Image.open('../gemini/jordi_rode_lijn_hoofd.png').convert('RGB')).astype(int)
r=(J[:,:,0]>180)&(J[:,:,1]<80)&(J[:,:,2]<80)
sc,ox,oy=9.8,9,7                         # Jordi-plaatje -> spritecoord (gemeten op de zwarte lijnen van r4)
ys,xs=np.where(r)
sx=xs/sc+ox; sy=ys/sc+oy
nx=3*sx+3; ny=3*sy-9                     # sprite -> natief (zelfde als zoom.py)
N=np.array(Image.open('../sprite/natief.png').convert('RGB'))
H,W=N.shape[:2]
lijn=np.full(W,-1.0)
for x in range(W):
    m=np.abs(nx-x)<1.0
    if m.any(): lijn[x]=ny[m].mean()
xs_l=np.where(lijn>=0)[0]
# anker: laagste lijnpunt binnen het gezichtsbereik (sprite x 24..34 -> natief 75..105)
mid=[x for x in xs_l if 75<=x<=105]; ax=int(np.mean(mid)); ay=lijn[mid].max()
bg=(N.min(2)>240)
mask=np.zeros((H,W),bool)
for x in xs_l: mask[:int(lijn[x]),x]=True
mask&=~bg
out=N.copy()
yy,xx=np.mgrid[0:H,0:W]
srcx=np.round(ax+(xx-ax)/S).astype(int); srcy=np.round(ay+(yy-ay)/S).astype(int)
ok=(srcx>=0)&(srcx<W)&(srcy>=0)&(srcy<H)
take=np.zeros((H,W),bool); take[ok]=mask[srcy[ok],srcx[ok]]
YC=int(sys.argv[2]) if len(sys.argv)>2 else 0
take&=(~bg)|(yy<YC)|(xx<ax)          # rechts onder YC: kap niet buiten het oude silhouet laten uitsteken
out[take]=N[srcy[take],srcx[take]]
Image.fromarray(out).save('natief_hoofd_%s.png'%sys.argv[1])
# snelle 3x3-preview zoals r1 (meerderheid -> hier gemiddelde) en vergroot model
Image.fromarray(out).resize((W*5,H*5),Image.NEAREST).save('model_hoofd_%s.png'%sys.argv[1])
print('anker',ax,ay,'verplaatst',int((take&~mask).sum()),'oud niet bedekt',int((mask&~take).sum()))
