# model.py: maakt het model met de steunarm korter (alleen rijen uit het rechte armstuk tussen lijf en polsband;
# alles erboven zakt mee, hand blijft staan) + alpha-masker (witte achtergrond vanaf de rand weggevuld).
# derde: rijen 774-835 (62 px = 1/3 van 185 px armlengte lijf->polsband, y 653-838); kwart: rijen 782-827 (46 px).
import numpy as np; from PIL import Image; from collections import deque
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/'
c=np.asarray(Image.open(H+'referenties/gemini_gekozen_capoeira.png').convert('RGB')).astype(int)
h,w,_=c.shape
wit=(c.min(2)>232)
bg=np.zeros((h,w),bool); q=deque()
for y in range(h):
  for x in (0,w-1):
    if wit[y,x]: bg[y,x]=1; q.append((y,x))
for x in range(w):
  for y in (0,h-1):
    if wit[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
while q:
  y,x=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    yy,xx=y+dy,x+dx
    if 0<=yy<h and 0<=xx<w and wit[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
rgba=np.zeros((h,w,4),'uint8'); rgba[...,:3]=c; rgba[...,3]=np.where(bg,0,255)
Image.fromarray(rgba).save(H+'sprite_gemini/ronde1/gereedschap/model_origineel.png')
for naam,(a,b) in {'derde':(774,836),'kwart':(782,828)}.items():
  n=b-a
  o=np.zeros_like(rgba)
  o[n:b]=rgba[:a]           # alles boven het knipstuk zakt n rijen
  o[b:]=rgba[b:]            # polsband + hand blijven staan
  Image.fromarray(o).save(H+f'sprite_gemini/ronde1/gereedschap/model_{naam}.png')
  ys,xs=np.where(o[...,3]>0); print(naam,'bbox',xs.min(),xs.max(),ys.min(),ys.max())
