# Zones op het natieve modelraster (alleen classificatie op modelkleur + vaste vakken voor onderdelen). Niets getekend.
# . achtergrond  K omlijning/lijn  W wol (crème)  D verre achterpoot (taupe)  G handschoen rood  T oorkwastje rood
# P oorbinnenkant roze  C kraag/manchet (roze/teal/geel)  E oog
import numpy as np; from PIL import Image
from scipy import ndimage
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
H,W,_=N.shape; r,g,b=N[...,0],N[...,1],N[...,2]; L=N.mean(2); mx=N.max(2); mn=N.min(2)
# achtergrond: bijna-wit en verbonden met de rand
wit=(mn>=226)&(mx-mn<=16)
lab,n=ndimage.label(wit); rand=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
bg=np.isin(lab,list(rand))
# ingesloten achtergrond (gat tussen de poten): puur wit en groot
lab2,n2=ndimage.label((mn>=240)&(mx-mn<=10))
for k in range(1,n2+1):
    if (lab2==k).sum()>=20: bg|=lab2==k
Z=np.full((H,W),'W',dtype='<U1'); Z[bg]='.'
yy,xx=np.mgrid[0:H,0:W]
red=(r-g>70)&(r>110)&(b<105)
darkred=(r-g>28)&(r>45)&(L<95)&(r>b)
pink=(r>170)&(r-g>45)&(b>=105)
teal=(g-r>35)&(b-r>25)
yel=(r>180)&(g>150)&(b<160)&(r-b>60)
med=ndimage.generic_filter(np.where(bg,np.nan,L),np.nanmedian,size=7,mode='nearest')
K=((L<92)|(L<med-30))&~darkred
Z[K]='K'
fg=~bg
# kraag (y 38-45) en manchetten (y 82-100 links)
kraag=(yy>=48)&(yy<=58)&(xx>=36)&(xx<=66)
manch=(yy>=82)&(yy<=101)&(xx<=68)
Z[fg&(pink|teal|yel)&(kraag|manch)]='C'
# oorbinnenkant
oor=(yy<=26)
Z[fg&pink&oor]='P'
Z[fg&(pink)&oor&~(red)]='P'
# rood: kwastjes boven, handschoenen onder
Z[fg&(red|darkred)&(yy<=30)]='T'
Z[fg&(red|darkred)&(yy>=78)]='G'
Z[fg&(yy>=78)&(Z=='K')&(r-g>18)&(r>b)]='G'
# oog: donker + glans in het ooggebied
oog=(yy>=29)&(yy<=38)&(xx>=45)&(xx<=52)
Z[fg&oog&((L<110)|((mn>200)&(Z=='W')&(L>235)))]='E'
# verre achterpoot: taupe rechtsonder
taupe=(L<175)&(L>=92)&(r-b>=22)&~red&~pink
far=(xx>=83)&(yy>=72)
Z[fg&far&taupe&(Z=='W')]='D'
np.save('zones_nat.npy',Z)
cm={'.':(255,255,255),'K':(20,20,20),'W':(240,232,210),'D':(150,120,90),'G':(220,40,50),'T':(255,120,0),'P':(255,170,200),'C':(40,170,170),'E':(0,0,255)}
img=np.array([[cm[z] for z in row] for row in Z],'uint8')
Image.fromarray(img).resize((W*6,H*6),0).save('zones_nat_6x.png')
for z in cm: print(z,(Z==z).sum())
