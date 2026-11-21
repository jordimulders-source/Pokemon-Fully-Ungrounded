# bewijs: alle verschillen r13 -> r14 vallen binnen de opdrachtzones
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
from maak import RINGEN
r=Image.open('sprite_r13/vlieg_r13.png').load()
Z={'1 voorpoten':lambda x,y: 8<=x<=27 and 39<=y<=58,
   '3 onderrand':lambda x,y: 22<=x<=38 and 39<=y<=41,
   '4 zwart vak':lambda x,y: 18<=x<=21 and y==27,
   '5 led':lambda x,y: 9<=x<=21 and 28<=y<=34,
   '2 ringen':lambda x,y: any(r_-1<=y<=r_+1 and min(cu,cl)-2<=x<=max(cu,cl)+3 for r_,cu,cl in RINGEN)}
for n in ('A_L1','A_L2','B_L1','B_L2'):
    im=Image.open('sprite_r14/vlieg_r14_%s.png'%n); a=im.load()
    assert im.mode=='P' and im.getpalette()[:48]==Image.open('sprite_r13/vlieg_r13.png').getpalette()[:48]
    d=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=r[x,y]]
    cnt={k:0 for k in Z}; buiten=[]
    for p in d:
        k=next((k for k,f in Z.items() if f(*p)),None)
        if k: cnt[k]+=1
        else: buiten.append(p)
    print(n,'totaal',len(d),cnt,'BUITEN zones:',buiten, 'indexen',sorted(set(im.getdata())))
