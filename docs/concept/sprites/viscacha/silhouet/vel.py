"""Silhouetvel: bron, silhouet 1x en 8x, bronomtrek (rood) over het verkleinde silhouet."""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
x0,y0,S,ox,oy=np.load(D+'silhouet/meta.npy')
src=Image.open(D+'referenties/gemini_gekozen_ronde6.png').convert('RGB')
im=np.array(src).astype(int); m=np.abs(im-255).sum(2)>60
m=nd.binary_fill_holes(m); mo=nd.binary_opening(m,structure=np.ones((7,7)))
d=m&~mo; lab,n=nd.label(d,structure=np.ones((3,3)))
sat=im.max(2)-im.min(2)
for i in range(1,n+1):   # dunne delen terug als ze gekleurd zijn (pluimpunten, oorranden); grijze snorharen blijven weg
    z=lab==i
    if (sat[z]>90).sum()>=4 and z.sum()<3000: mo|=z
m=mo
lab,n=nd.label(m); m=lab==(1+np.argmax(nd.sum(m,lab,range(1,n+1))))
edge=m&~nd.binary_erosion(m)
sil=np.array([[c=='#' for c in l.strip()] for l in open(D+'silhouet/silhouet.txt')][:64])
Z=8
big=np.full((512,512,3),235,np.uint8); big[np.kron(sil,np.ones((Z,Z),bool))]=(90,90,100)
ys,xs=np.nonzero(edge)
px=((xs-x0)/S+ox)*Z; py=((ys-y0)/S+oy)*Z
ok=(px>=0)&(px<512)&(py>=0)&(py<512); big[py[ok].astype(int),px[ok].astype(int)]=(230,20,20)
W=Image.new("RGB",(512+20+512+20+128+20,560),'white')
s=src.crop((x0-20,y0-20,x0+int(S*62)+20,y0+int(S*53)+20)); s.thumbnail((512,512))
W.paste(s,(0,0)); W.paste(Image.fromarray(big),(532,0))
one=Image.fromarray(np.where(sil[...,None],np.array([60,60,70],np.uint8),np.array([255,255,255],np.uint8)).astype(np.uint8))
W.paste(one,(1064,0)); W.paste(one.resize((128,128),Image.NEAREST),(1064,80))
ImageDraw.Draw(W).text((4,520),'bron (Gemini r6) | silhouet 8x + bronomtrek rood | 1x en 2x',fill='black')
W.save(D+'silhouet/vel.png')
Image.fromarray((sil*255).astype(np.uint8)).save(D+'silhouet/silhouet.png')
