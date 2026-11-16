# r23 = r22 + Jordi's schets 2 (jordi/koeienvanger_lijnen2.png, teruggerekend met ijk.py: schaal 9,85, offset -8/2,5; fitfout 3,1).
# Jordi: "heb een beetje met lijnen getekend hoe ik het zie, veel klopt al wel hoor". Schets = richting; vorm volgt de schets.
# Bevroren (assert): groen, alles buiten de koeienvanger-zone x0-26 / y45-56.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r22/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette(); a=r.copy()
GRS=[2,3,4,5,6,13]
def zet(lst,v):
    for y,x in lst: a[y,x]=v
# 1. linkerrand recht verticaal op x2 (schets x2,3-2,8, y43-52): selout 9 op x2 rij 45-50 (zoals r20 links), x3 wordt wig
zet([(y,2) for y in range(45,51)],9)
for y in range(45,51): a[y,3]=7 if a[y,4]==7 else 8           # x3 = lichte wig (licht 7), anders roest 8
# 2. schuine bovenlijn links (schets (3,9;42,9)->(6,9;46)): ligt al op (45,6),(46,7); het zwarte blokje eronder dunner
zet([(46,6),(47,6)],7); zet([(47,7)],1)
# 3. "^" bij (9,49)-(8,53)/(10,51): top van het tweede blad als punt; poten 1 px zwart, binnenin lichte plaattint 10
zet([(49,9),(50,8),(51,8),(52,8),(53,8),(50,10),(51,10)],1)
zet([(50,9),(51,9),(52,9),(53,9)],10)
# 4. ruit bij x16-19, y49,5-54,6: zwarte ruitomlijning (3 breed, 5 hoog), roest 8 binnenin; rechts ervan rechterplaat
zet([(50,17),(51,16),(51,18),(52,16),(52,18),(53,16),(53,18),(54,17)],1)
zet([(51,17),(52,17),(53,17)],8)
zet([(51,19),(52,19),(53,19),(54,19)],11); zet([(54,18)],12); zet([(54,16)],9)
# 5. "<" bij x20-23, y49-53: naad van de rechterplaat, 1 px zwart; omgeving plaattinten
zet([(49,23),(50,22),(51,21),(52,22),(53,23)],1)
zet([(50,23),(51,22),(51,23),(52,23)],11); zet([(49,21),(49,22)],10); zet([(52,21),(53,21),(53,22),(52,20),(53,20)],12)
# 6. rechterrand recht verticaal op x24 tot y55, haakse hoek, vlakke onderrand y55 naar links (x18-24)
zet([(y,24) for y in range(47,55)],1)
zet([(55,x) for x in range(18,25)],1)
zet([(54,x) for x in range(20,24)],12)
a[54,25]=0
# opschonen: ruittop 1 px, geen losse 1-px-tinten
zet([(50,18),(54,18)],11); zet([(49,3)],9)
# bewijs bevroren
groen=np.isin(r,GRS)
assert (a[groen]==r[groen]).all() and not np.isin(a[~groen],GRS).any(),'groen gewijzigd'
KV=np.zeros((64,64),bool); KV[45:57,0:27]=True
assert (a[~KV]==r[~KV]).all(),'buiten zone gewijzigd'
if __name__=='__main__':
    d=a!=r; print('gewijzigd',int(d.sum()),'buiten zone',int(d[~KV].sum()),'groen-diff',int(d[groen].sum()),'silhouet +',int(((r==0)&(a!=0)).sum()),'-',int(((r!=0)&(a==0)).sum()))
    print('   '+''.join(str(x%10) for x in range(30)))
    for y in range(43,59): print('%2d'%y,''.join('.' if q==0 else '%X'%q for q in a[y,:30]))
    o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal); o.save(D+'sprite_r23/sprite.png',transparency=0)
    o.resize((512,512),Image.NEAREST).save(D+'sprite_r23/sprite_8x.png',transparency=0)
