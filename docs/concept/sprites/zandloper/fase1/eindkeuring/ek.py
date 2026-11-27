# Eindkeuring zandloper fase 1: alleen tinten en schaduw (alpha blijft gelijk).
# 1) bovenkap: modelvlak (169,111,66) was door de palet-reductie verdeeld over zand-3 en hout-C -> alles hout-C
# 2) selout zoals fase 3 / Gen 3: glasrand en kaprand aan de schaduwkant (rechts/onder) zwart,
#    kaprand aan de lichte kant (boven/links) in de donkerste houttint (2)
# 3) glastinten 7 en 9 gelijk aan fase 3. Handen en ogen: geen pixel aangeraakt.
import numpy as np; from PIL import Image
from collections import Counter
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/zandloper/fase1/'
s=Image.open(D+'sprite/r14_natief/zandloper_fase1_natief.png'); a=np.asarray(s).copy(); o=a.copy()
n=np.asarray(Image.open(D+'sprite/natief.png').convert('RGB')).astype(int)[16:80,17:81]
pal=s.getpalette()[:48]
H=np.zeros_like(a,bool); H[22:36,0:14]=True; H[35:46,50:64]=True          # handen
EYE=np.zeros_like(a,bool); EYE[13:25,24:47]=True                           # gezicht/ogen
top=np.zeros_like(a,bool); top[0:19,22:64]=True; bot=np.zeros_like(a,bool); bot[44:64,0:42]=True
CAP=(top|bot)&~H&~EYE
wood=CAP&(np.isin(a,[1,2,11,12])|((a==3)&(n[:,:,1]<122)))
log=Counter()
# 1) bovenkap egaal hout
m=top&wood&(a==3); a[m]=12; log['kap: zand-3 -> hout-C']+=m.sum()
# 2) selout
T=lambda y,x: (y<0 or y>63 or x<0 or x>63) or o[y,x]==0
for y in range(64):
  for x in range(64):
    if o[y,x]==0 or H[y,x] or EYE[y,x]: continue
    r,b,l,t=T(y,x+1),T(y+1,x),T(y,x-1),T(y-1,x)
    if not (r or b or l or t): continue
    if wood[y,x]:
      new=1 if (r or b) else 2
      if a[y,x]!=new: log['kaprand -> %s'%('zwart' if new==1 else 'donkerste hout')]+=1; a[y,x]=new
    elif o[y,x] in (7,8,9,10) and (r or b):
      if a[y,x]!=1: log['glasrand schaduwkant -> zwart']+=1; a[y,x]=1
pal[7*3:7*3+3]=[64,94,122]; pal[9*3:9*3+3]=[160,204,224]
out=Image.fromarray(a,'P'); out.putpalette(pal+[0]*(768-48)); out.info['transparency']=0
out.save(D+'eindkeuring/zandloper_fase1_ek.png',transparency=0)
print(dict(log)); print('alpha-diff',int(((a>0)!=(o>0)).sum()),'handen-diff',int((a!=o)[H].sum()),'ogen-diff',int((a!=o)[EYE].sum()))
print('kleuren incl. transparant',len(set(a.flatten().tolist())))
ch=(a!=o); ys,xs=np.where(ch); print('totaal gewijzigd',ch.sum())
