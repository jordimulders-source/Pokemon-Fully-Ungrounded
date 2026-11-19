# Kleurronde 1 op r4 (vorm bevroren: alpha en zwarte lijnposities blijven; alleen tinten/palet). Elke zone benoemt zijn pixels.
import numpy as np; from PIL import Image
PAL=[(152,208,160),(24,20,16),(238,156,88),(204,112,56),(150,72,38),(252,244,216),(232,210,160),(198,166,116),
     (234,82,74),(208,200,196),(148,138,134),(84,76,76),(250,214,64),(214,156,36),(255,246,168),(104,48,24)]
# index 14: was wit (alleen oogglans) -> lichtgeel L voor de bliksem; oogglans wordt C (5)
r4=np.load('_tmp/r4.npy'); o=r4.copy(); Z={}
def zet(z,lst):
    for x,y,v in lst:
        if o[y,x]!=v: Z.setdefault(z,[]).append((x,y,int(o[y,x]),v)); o[y,x]=v
zet('oogglans',[(20,12,5)])
# bliksem: licht L linksboven, y midden, Y schaduwkant rechts/onder en de punt; selout Y op de lichte linkerrand
L,y,Y=14,12,13
B={32:[(2,L)],33:[(2,L),(3,L)],34:[(3,L),(4,y)],35:[(3,L),(4,y),(5,y)],36:[(4,L),(5,y)],37:[(4,L),(5,y),(6,Y)],
   38:[(5,L),(6,y),(7,Y)],39:[(4,L),(5,L),(6,y),(7,Y)],40:[(2,L),(3,L),(4,y),(5,y)],41:[(3,L),(4,y),(5,Y)],
   42:[(4,L),(5,y),(6,Y)],43:[(5,L),(6,y)],44:[(6,y),(7,Y)],45:[(7,y),(8,Y)],46:[(8,y),(9,Y)],47:[(9,Y),(10,Y)]}
zet('bliksem vulling',[(x,yy,v) for yy,l in B.items() for x,v in l])
zet('bliksem selout',[(1,32,Y),(1,33,Y),(2,34,Y),(2,35,Y),(3,36,Y),(3,37,Y),(4,38,Y),(2,39,Y),(3,39,Y)])
# kop: hooglicht op voorhoofd/kruin linksboven, sikkel d langs het achterhoofd (1 px boven, 2 px onder)
zet('kop licht',[(21,7,2),(22,7,2),(23,7,3),(22,8,2),(20,9,2),(21,9,2)]+[(x,10,2) for x in range(15,19)]+[(14,11,2),(15,11,2)])
zet('kop sikkel',[(26,10,4),(27,11,4),(27,12,4),(27,13,4)]+[(x,yy,4) for yy in range(14,21) for x in (27,28)]+[(28,21,4),(29,21,4),(28,22,4)])
# buik: onderste c-strook (rij 41) opgelost: C-kern zakt links-midden door, sikkel blijft rechtsonder
zet('buik',[(26,40,5)]+[(x,41,5) for x in range(21,25)]+[(25,43,7)])
# poten: verre (linker) donkerder, nabije (rechter) lichter met 1 px glans
zet('verre poot',[(21,48,11),(20,47,11)])
zet('nabije poot',[(28,46,10),(28,47,10),(26,49,10),(26,50,10),(27,49,9)])
# vleugel/lijf: losse bruine tintpixel (alle bruine 4-buren dezelfde andere tint, >=3 buren) -> die tint
q=o.copy(); L1=[]
for yy in range(1,63):
    for x in range(1,63):
        if o[yy,x] in (2,3,4) and x>=29:
            nb=[o[yy+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if o[yy+dy,x+dx] in (2,3,4)]
            if len(nb)>=3 and len(set(nb))==1 and nb[0]!=o[yy,x]: L1.append((x,yy,int(nb[0])))
zet('vleugel ruis',L1)
np.save('r1.npy',o)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('picaraio.png',transparency=0)
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
Image.fromarray(np.array(PAL,'uint8')[o]).resize((512,512),0).save('picaraio_8x.png')
with open('pixels.txt','w') as f:
    f.write('Gewijzigde pixels r4 -> kleur r1 per zone: (x,y, oude index -> nieuwe index). Palet: alle 16 kleuren bijgesteld (zie normal.pal); index 14 wit -> lichtgeel.\n')
    for z,l in Z.items(): f.write('%s (%d): %s\n'%(z,len(l),' '.join('(%d,%d %d>%d)'%t for t in l)))
for z,l in Z.items(): print('%-16s %3d'%(z,len(l)))
print('alpha-diff',int(((o>0)!=(r4>0)).sum()),'| zwart verplaatst',int(((o==1)!=(r4==1)).sum()),'| totaal',int((o!=r4).sum()))
