# Eindkeuring zandloper fase 1 op fase 1-maat (r12, reductie 0,70): zelfde correcties als ../eindkeuring/ek.py.
# 1) bovenkap: gemeten op het model (0,70-raster) al vlak hout-C (bovenvlak) + hout-B (zijband), geen zand -> niets te doen
# 2) selout zoals fase 3 / Gen 3: kaprand schaduwkant (rechts/onder) zwart, lichte kant (boven/links) donkerste hout (2);
#    glasrand schaduwkant zwart, lichte kant blijft eigen tint
# 3) glastinten 7 en 9 gelijk aan fase 3. Handen en ogen: geen pixel aangeraakt.
import numpy as np; from PIL import Image
from collections import Counter
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/zandloper/fase1/'
s=Image.open(D+'sprite/r12/zandloper_fase1_r12.png'); a=np.asarray(s).copy(); o=a.copy()
pal=s.getpalette()[:48]
H=np.zeros_like(a,bool); H[30:38,9:20]=True; H[38:47,45:56]=True             # handen
EYE=np.zeros_like(a,bool); EYE[24:31,27:34]=True; EYE[28:33,35:45]=True      # ogen (Jordi)
top=np.zeros_like(a,bool); top[12:28,26:56]=True; bot=np.zeros_like(a,bool); bot[44:60,12:42]=True
CAP=(top|bot)&~H&~EYE
wood=CAP&np.isin(a,[1,2,11,12,13])
log=Counter()
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
out=Image.fromarray(a,'P'); out.putpalette(pal+[0]*(768-48))
out.save(D+'eindkeuring_070/zandloper_fase1_ek070.png',transparency=0)
print(dict(log)); print('alpha-diff',int(((a>0)!=(o>0)).sum()),'handen-diff',int((a!=o)[H].sum()),'ogen-diff',int((a!=o)[EYE].sum()))
print('kleuren incl. transparant',len(set(a.flatten().tolist())),'idx15',int((a==15).sum()))
print('totaal gewijzigd',int((a!=o).sum()))
# 8x en vel
def rgb(idx,p,bg):
  P=np.array(p[:48]).reshape(16,3).astype('uint8'); im=P[idx].copy(); im[idx==0]=bg; return Image.fromarray(im)
Image.open(D+'eindkeuring_070/zandloper_fase1_ek070.png').convert('RGBA').resize((512,512),0).save(D+'eindkeuring_070/zandloper_fase1_ek070_8x.png')
op=s.getpalette()[:48]
v=Image.new('RGB',(512*2+16,512+80),(255,255,255))
v.paste(rgb(o,op,(255,255,255)).resize((512,512),0),(0,0)); v.paste(rgb(a,pal,(255,255,255)).resize((512,512),0),(528,0))
for k,bg in enumerate([(255,255,255),(232,232,224),(40,40,48),(0,0,0)]):
  v.paste(rgb(o,op,bg),(k*72,520)); v.paste(rgb(a,pal,bg),(528+k*72,520))
v.save(D+'eindkeuring_070/vel.png')
