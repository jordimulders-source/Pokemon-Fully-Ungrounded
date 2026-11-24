# skel.py: modellijnen als 1 px-lijnen. Zwarte modellijnen (fam 1) -> skelet (skimage) op volle resolutie; elk skeletpunt telt
# in de spritepixel waar het (met de gedeelde geometrie) in valt. Buitenomtrek van het model (<= 7 modelpx van de achtergrond) telt
# niet mee: die is de buitenlijn van de sprite. -> skel.npy (aantal skeletpunten per spritepixel) en skel.png (controle)
import numpy as np; from PIL import Image; from scipy import ndimage as nd; from skimage.morphology import skeletonize
from reductie_gedeeld import P, X0M,X0S,Y0M,Y0S
from fam import MODEL
f=np.load('model_fam.npz')['f'].astype(int)
a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); L=a.mean(2)
lm=(f==1)|((f>0)&(L<nd.gaussian_filter(L,5)-35))     # zwarte lijnen + duidelijk donkere modellijnen (naden tussen houtplaten, bladranden)
sk=skeletonize(nd.binary_closing(lm))
d=nd.distance_transform_edt(f>0); sk&=d>7
lab,n=nd.label(sk,structure=np.ones((3,3))); gr=nd.sum(sk,lab,range(1,n+1))
sk&=np.isin(lab,1+np.where(gr>=20)[0])   # korte stukjes (houtnerf-streepjes, ruis) tellen niet: minder maar duidelijke lijnen
cnt=np.zeros((64,64))
for v,u in zip(*np.where(sk)):
    X=int(np.floor((u-X0M)/P+X0S)); Y=int(np.floor(Y0S-(Y0M-v)/P))
    if 0<=X<64 and 0<=Y<64: cnt[Y,X]+=1
np.save('skel.npy',cnt)
img=np.full(f.shape+(3,),255,'uint8'); img[f>0]=200; img[sk]=(255,0,0)
Image.fromarray(img).crop((260,30,760,530)).save('skel.png'); print('skeletpunten',sk.sum())
