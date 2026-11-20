# r18 = r17 + (1) linkerpoot per pixel uit het model (meettabel: meetpoot.txt) + (2) nek los van de vleugel (nek.py, alleen kleur).
import numpy as np; from PIL import Image
from nek import nek
im17=Image.open('../r17/hoatzin.png'); r17=np.array(im17)
out=r17.copy()
# (1) linkerpoot (verre poot). Per spritepixel gemeten in het natieve model (3x3 natief): achtergrond/9, donker/9, gem. grijs.
#   scheen y51-53 schuin van x26-27 naar x25: lijn | grijs | lijn (model 2 px incl. lijn per kant);
#   bovenste teen y55 x19-23 grijs (licht bovenkant: x21-22 L>=100 -> 15), lijn erboven y54 (model 6/9 rand), lijn y56 tussen de tenen (model 4-6/9 donker);
#   onderste teen y57 x17-21 grijs, onderkant y58 lijn; teenpunten x17-18; klauwen zwart (17,58) en (18,59) (model 7/9 donker).
#   verre poot een stap donkerder: onderkant/donker deel = 2 i.p.v. 14.
POOT={ # y: (x0, 'rij'), . = transparant, 1 lijn, 2 donker, e 14 grijs, f 15 licht grijs
 51:(15,'..........12e'),
 52:(15,'..........1e1'),
 53:(15,'.........1ee1'),
 54:(15,'....11111ff1.'),
 55:(15,'...1eeffeeee1'),
 56:(15,'..1e111111eee'),
 57:(15,'.1e2fef11'),
 58:(15,'..1e1111'),
 59:(15,'...1.....'),
}
ZONE=np.zeros((64,64),bool); C={'.':0,'1':1,'2':2,'e':14,'f':15}
for y,(x0,s) in POOT.items():
    for i,ch in enumerate(s):
        x=x0+i
        assert r17[y,x] not in (11,12,13), ('buik', x, y)
        out[y,x]=C[ch]; ZONE[y,x]=True
# r17-poot buiten de nieuwe vorm in hetzelfde gebied (rafels links/onder) weg: x13-16, y54-60 en x15-23 y59-61
for y in range(54,62):
    for x in range(12,24):
        if not ZONE[y,x] and (y>=59 or x<=16) and r17[y,x] in (1,2,14,15): out[y,x]=0; ZONE[y,x]=True
# (2) nek
out,log,lijn=nek(out)
NEK=np.zeros((64,64),bool)
for w,x,y,o,n in log: NEK[y,x]=True
im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette(im17.getpalette()); im.save('hoatzin.png',transparency=0)
im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png'); np.save('r18.npy',out); np.save('zones.npy',{'poot':ZONE,'nek':NEK},allow_pickle=True)
open('normal.pal','w').write(open('../r17/normal.pal').read())
d=out!=r17; al=(out>0)!=(r17>0)
print('anders dan r17',d.sum(),'| poot',(d&ZONE).sum(),'nek',(d&NEK).sum(),'| buiten de zones',(d&~ZONE&~NEK).sum())
print('alpha anders',al.sum(),'waarvan buiten poot',(al&~ZONE).sum())
for y in range(48,62): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in out[y,12:34]),'  ',''.join('.' if v==0 else '%x'%v for v in r17[y,12:34]))
