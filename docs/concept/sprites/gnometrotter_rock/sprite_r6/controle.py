# controle.py: lever r6 af (png, _8x, naast_model) en tel/controleer.
import numpy as np, pickle; from PIL import Image; from scipy import ndimage as nd
from vgl import sprite_rgb, model_crop
r5=Image.open('r5.png'); R5=np.asarray(r5).astype(int); O=np.load('O.npy'); Z=np.load('../sprite/zone.npy')
K=np.asarray(Image.open('red_r8_kaal.png')).astype(int)
p=Image.fromarray(O.astype('uint8'),'P'); p.putpalette(r5.getpalette()); p.save('gnometrotter_rock.png',transparency=0)
sprite_rgb('gnometrotter_rock.png').resize((512,512),Image.NEAREST).save('gnometrotter_rock_8x.png')
a=sprite_rgb('gnometrotter_rock.png').resize((512,512),Image.NEAREST); m=model_crop(0,0,64,64,8)
W=Image.new('RGB',(1040,512),'white'); W.paste(a,(0,0)); W.paste(m,(528,0)); W.save('naast_model.png')
BRON,DEEL=pickle.load(open('bron.pkl','rb'))
print('silhouet alpha-diff met r5:',((O>0)!=(R5>0)).sum(),' met r4:',((O>0)!=(np.asarray(Image.open('../sprite_r4/gnometrotter_rock.png'))>0)).sum())
print('palet gelijk aan r5:',Image.open('gnometrotter_rock.png').getpalette()[:48]==r5.getpalette()[:48])
ZN={1:'muts+rugkam',2:'haar L',3:'haar R',4:'baard',5:'neus',6:'lijf',7:'arm L+hand',8:'arm R',9:'hand R',10:'riem',11:'stok',12:'broek/benen',13:'zool L',14:'zool R'}
print('%-14s %6s %6s %8s %6s %6s'%('zone','!=r5','!=kaal','vd r5:!=kaal','gesp','ruis'))
tot=0
for k,n in ZN.items():
    z=(Z==k)&(O>0); d5=(O!=R5)&z; dk=(O!=K)&z; tot+=d5.sum()
    g=sum(1 for (y,x),b in BRON.items() if b=='G' and z[y,x] and O[y,x]!=R5[y,x])
    r=sum(1 for (y,x),b in BRON.items() if b=='R' and z[y,x])
    print('%-14s %6d %6d %8d %6d %6d'%(n,d5.sum(),dk.sum(),((R5!=K)&z).sum(),g,r))
print('totaal anders dan r5:',tot)
ring=sum(1 for b in BRON.values() if b=='O'); print('ringpixels (modellijn rond teruggezette delen, in r5-onderdelen):',ring)
# losse pixels (8-buren, zelfde index)
los=[(x,y,O[y,x]) for y in range(1,63) for x in range(1,63) if O[y,x] and not any(O[y+dy,x+dx]==O[y,x] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse pixels:',los)
# tinten per onderdeel
for k in (2,3,4,10,12):
    print(ZN[k],'indexen:',sorted(set(O[(Z==k)&(O>0)].tolist())))
sch=np.zeros((64,64),bool); sch[19:29,38:49]=True; sch&=(Z==6)
print('schouder R indexen:',sorted(set(O[sch].tolist())),' arm R:',sorted(set(O[Z==8].tolist())))
