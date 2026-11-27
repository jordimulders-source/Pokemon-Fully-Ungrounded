# Vergelijk lichaamstonen sprite (l/d/m) met modelhelderheid per spritepixel
from PIL import Image
import numpy as np, sys
s=np.array(Image.open('staryu/sprite_r1/staryu_r1.png'))
m=Image.open('gemini/r3_staryu.png').convert('RGB').crop((143,122,902,902)).resize((41,43),Image.BOX)
M=np.zeros((64,64,3)); M[12:55,11:52]=np.array(m)
L=M@[0.299,0.587,0.114]
body={5:'l',4:'d',3:'m'}
mask=np.isin(s,[3,4,5])
vals=L[mask]
# drempels: zelfde aandelen als de sprite
n5=(s==5).sum(); n3=(s==3).sum(); tot=mask.sum()
srt=np.sort(vals)
t_lo=srt[n3]; t_hi=srt[tot-n5]
print('drempels',t_lo,t_hi)
ch={0:'.',1:'K',2:'b'}
agree=0
out=[]
for y in range(12,55):
    r1='';r2=''
    for x in range(9,54):
        v=s[y,x]
        if v in body:
            r1+=body[v]
            c='m' if L[y,x]<t_lo else ('l' if L[y,x]>=t_hi else 'd')
            r2+=c; agree+= (c==body[v])
        else:
            r1+=ch.get(v,'#'); r2+=ch.get(v,'#')
    out.append('%2d %s   %s'%(y,r1,r2))
print('\n'.join(out)); print('overeenkomst',agree,'/',tot)
print('--- afwijkingen (sprite->model) ---')
from collections import defaultdict
d=defaultdict(list)
for y in range(64):
  for x in range(64):
    v=s[y,x]
    if v in body:
      c='m' if L[y,x]<t_lo else ('l' if L[y,x]>=t_hi else 'd')
      if c!=body[v]: d[body[v]+'->'+c].append((x,y))
for k,v in sorted(d.items()): print(k,len(v),v)
