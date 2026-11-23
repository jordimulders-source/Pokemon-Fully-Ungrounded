# controle.py: lever r7 af en tel/controleer.
import numpy as np, pickle; from PIL import Image
from vgl import sprite_rgb, model_crop
r6=Image.open('r6.png'); R6=np.asarray(r6).astype(int); O=np.load('na_tint.npy'); Z=np.load('zone.npy'); V=np.load('na_vorm.npy')
p=Image.fromarray(O.astype('uint8'),'P'); p.putpalette(r6.getpalette()); p.save('gnometrotter_rock.png',transparency=0)
a=sprite_rgb('gnometrotter_rock.png').resize((512,512),Image.NEAREST); a.save('gnometrotter_rock_8x.png')
b=sprite_rgb('r6.png').resize((512,512),Image.NEAREST); m=model_crop(0,0,64,64,8)
W=Image.new('RGB',(1568,512),'white'); W.paste(a,(0,0)); W.paste(b,(528,0)); W.paste(m,(1056,0)); W.save('naast_model.png')
sd=np.argwhere((O>0)!=(R6>0)); print('silhouet anders dan r6:',[(x,y) for y,x in sd])
ZN={1:'muts+rugkam',2:'haar L',3:'haar R',4:'baard',5:'neus',6:'lijf',7:'arm L+hand',8:'arm R',9:'hand R',10:'riem',11:'stok',12:'broek/benen',13:'zool L',14:'zool R'}
B=pickle.load(open('bron_vorm.pkl','rb'))
print('%-13s %5s %6s %6s'%('zone','!=r6','vorm','tint'))
t=0
for k,n in ZN.items():
    z=(Z==k)|((Z==0)&(k==7)&((O>0)!=(R6>0)))
    d=(O!=R6)&z; vorm=((V!=R6)&z&np.isin(V,[1,2,4,6,9])&np.isin(O,[1,2,4,6,9])).sum(); t+=d.sum()
    print('%-13s %5d %6d %6d'%(n,d.sum(),vorm,d.sum()-vorm))
print('totaal',t)
los=[(x,y,O[y,x]) for y in range(1,63) for x in range(1,63) if O[y,x] and not any(O[y+dy,x+dx]==O[y,x] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse pixels:',los)
T={'steen':(3,4,5),'licht':(12,13,14),'roze':(7,8,15),'blauw':(9,10,11)}
for k,n in ZN.items(): print(n,sorted(set(O[(Z==k)&(O>0)].tolist())))
