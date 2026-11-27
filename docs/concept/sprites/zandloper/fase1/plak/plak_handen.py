# Handen uit r3 knippen, draaien/spiegelen en op r7 plakken (bollen weg).
from PIL import Image, ImageOps
import numpy as np, sys
G='../gemini/'
r3=Image.open(G+'r3.png').convert('RGB'); r7=Image.open(G+(sys.argv[1] if len(sys.argv)>1 else 'r7.png')).convert('RGB')

def knip(im,box):
    c=im.crop(box); a=np.array(c).astype(int)
    m=(a.min(axis=2)<235)
    rgba=np.dstack([a,np.where(m,255,0)]).astype('uint8')
    return Image.fromarray(rgba,'RGBA')

L=knip(r3,(280,525,425,640)); R=knip(r3,(615,380,735,505))
base=np.array(r7)
for x0,y0,x1,y1 in [(180,395,310,525),(700,515,845,650)]:
    base[y0:y1,x0:x1]=255
base=Image.fromarray(base)
links,rechts=(245,460),(772,582)   # middens van de bollen in r7

def plak(im,hand,c):
    im.paste(hand,(c[0]-hand.width//2,c[1]-hand.height//2),hand)

def variant(naam,hl,hr):
    im=base.copy(); plak(im,hl,links); plak(im,hr,rechts); im.save(naam)

# A: gespiegeld (r3 helt naar links, r7 naar rechts): r3-rechterhand -> links, r3-linkerhand -> rechts
variant('A_gespiegeld.png',ImageOps.mirror(R),ImageOps.mirror(L))
# B: gedraaid met de zandloper mee (r3 -> r7 = 44 graden met de klok mee)
rot=lambda h:h.rotate(-44,resample=Image.NEAREST,expand=True)
variant('B_gedraaid.png',rot(R),rot(L))   # links boven = r3 rechterhand? zie noot
variant('C_gedraaid_omgewisseld.png',rot(L),rot(R))
