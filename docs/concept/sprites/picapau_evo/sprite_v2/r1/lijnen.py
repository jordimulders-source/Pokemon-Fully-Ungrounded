# Dunne zwarte modellijnen in de lucht (kuifslierten, staartkoord): donkerte-dekking per spritecel uit het 1024-model,
# daarna Zhang-Suen-verdunning tot 1 px (8-verbonden). Alleen cellen waarvan het 3x3-blok alleen zwart+achtergrond is
# (lijn in de lucht) of die al zwart/leeg zijn in de kale reductie. -> lijn.npy (1 = lijnpixel)
import numpy as np
K=np.load('klassen.npy'); kaal=np.load('kaal.npy'); OY,OX=1,4; h,w=kaal.shape
cov=np.zeros((h,w),int); air=np.zeros((h,w),bool)
for j in range(h):
    for i in range(w):
        b=K[OY+3*j:OY+3*j+3,OX+3*i:OX+3*i+3]
        cov[j,i]=(b==1).sum(); air[j,i]=((b==0)|(b==1)).all() and cov[j,i]>0
# donkerte-dekking per spritecel uit het 1024-model (ook de grijze anti-aliaslijnen tellen): neutraal en lum<150
from PIL import Image
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int)
lum=a.mean(2); sat=a.max(2)-a.min(2); ys,xs=np.where((lum<150)&(sat<40)); S=15.36
jj=((ys-OY*5.12)//S).astype(int); ii=((xs-OX*5.12)//S).astype(int); ok=(jj>=0)&(jj<h)&(ii>=0)&(ii<w)
dc=np.zeros((h,w)); np.add.at(dc,(jj[ok],ii[ok]),(150-lum[ys,xs][ok])/150)
body=(kaal>1)
lc=(~body)&(dc>=40)   # lijncel: geen lijf in de kale reductie, genoeg donker
# alleen lijncellen die tot een component behoren met een lucht-cel (lijnen in de lucht), lijfranden blijven uit de reductie
m=lc&(air|(kaal==0))
def zs(img):
    img=img.copy().astype(np.uint8); ch=True
    while ch:
        ch=False
        for step in (0,1):
            P=np.pad(img,1); rm=[]
            for y,x in zip(*np.where(img)):
                n=[P[y,x+1],P[y,x+2],P[y+1,x+2],P[y+2,x+2],P[y+2,x+1],P[y+2,x],P[y+1,x],P[y,x]]  # p2..p9
                B=sum(n); A=sum((n[k]==0 and n[(k+1)%8]==1) for k in range(8))
                if 2<=B<=6 and A==1:
                    if step==0 and n[0]*n[2]*n[4]==0 and n[2]*n[4]*n[6]==0: rm.append((y,x))
                    if step==1 and n[0]*n[2]*n[6]==0 and n[0]*n[4]*n[6]==0: rm.append((y,x))
            for y,x in rm: img[y,x]=0; ch=True
    return img
L=zs(m)
np.save('lucht.npy',air); np.save('lijn.npy',L)
print('luchtcellen',air.sum(),'na verdunning',L.sum())
