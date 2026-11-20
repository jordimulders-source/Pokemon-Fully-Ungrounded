# r8: reparaties keurder op r7. Gebruik: python3 bouw.py [A|B]  (B = verre vleugel volledig grijzer)
import sys, numpy as np; from PIL import Image
CH='.KWwvucbanyedrs'
var=sys.argv[1] if len(sys.argv)>1 else 'B'
b=np.array([list(l.rstrip('\n')) for l in open('rufflet_r7.txt')]); g=b.copy()
Z={}
def zet(zone,pts):
    for x,y,c in pts:
        g[y,x]=c; Z.setdefault(zone,[]).append((x,y))
# 1 rechterpoot
zet('1 rechterpoot',[(34,55,'d'),(35,55,'d'),(36,55,'d'),(33,54,'K')])
# 2 voet veer/snavel ((24,29) s = veervoet sinds r5, bevroren -> niet aangeraakt)
zet('2 rand/snavel',[(22,27,'.'),(22,28,'K'),(24,30,'e')])
# 3 verre vleugel
p3=[(21,41,'a'),(22,41,'c'),(23,41,'a'),(22,42,'c'),(23,42,'a'),(22,43,'c'),(23,43,'a'),
    (21,44,'c'),(22,44,'c'),(23,44,'a'),(18,45,'a'),(23,45,'a'),(17,46,'a'),(23,46,'u')]
zet('3 verre vleugel',p3)
if var=='B':  # vleugelvlak grijzer: c->b binnen de vleugel, W-hooglicht op de vleugel -> c
    vl=[]
    for y in range(41,57):
        for x in range(15,25):
            if (y>=47 and x>=24) or (x==23 and y>=47) : continue
            if g[y,x]=='c': vl.append((x,y,'b'))
            elif g[y,x]=='W' and x<=20: vl.append((x,y,'c'))
    zet('3 verre vleugel',vl)
# 4 nabije vleugel: a-sikkel langs onderrand, lichtere veerlijnen onderaan
zet('4 nabije vleugel',[(39,41,'b'),(40,42,'b'),(39,47,'a'),(38,48,'a'),(39,48,'a'),
    (37,49,'a'),(38,49,'a'),(41,49,'b'),(36,50,'a'),(38,50,'b')])
# 5 kop w-sikkel rechts
zet('5 kop sikkel',[(34,22,'w'),(34,23,'w'),(35,23,'w'),(35,24,'w'),(36,24,'w'),(35,25,'w'),(35,26,'w'),
    (34,27,'w'),(34,28,'w'),(34,29,'w'),(35,29,'w'),(33,30,'w'),(33,31,'w')])
# 6 rechtervoet
zet('6 rechtervoet',[(32,59,'y'),(33,59,'y'),(34,59,'y'),(35,59,'y'),(36,59,'y'),(37,59,'e'),(38,59,'e'),
    (32,60,'e'),(33,60,'e'),(34,60,'e'),(35,60,'e'),(36,60,'e'),(37,60,'e'),(38,60,'d'),(39,60,'d')])
# 7 dubbele rand hals/schouder
zet('7 hals',[(35,35,'v'),(36,36,'v'),(36,37,'v')])
# 8 klein
zet('8 klein',[(45,47,'n'),(45,49,'a'),(45,50,'a'),(31,63,'K'),(41,61,'K'),(31,18,'a'),(32,18,'a'),(32,19,'a')])
# eigen: klauw linkervoet (24,60-61) had ook een open onderkant
zet('eigen klauw',[(24,62,'K')])
# ---- controles
d=(g!=b)
for k,v in Z.items():
    print('%-18s %2d px gewijzigd'%(k,sum(int(g[y,x]!=b[y,x]) for x,y in set(v))))
alle=set(p for v in Z.values() for p in v)
buiten=[(x,y) for y,x in zip(*np.where(d)) if (x,y) not in alle]
print('totaal',int(d.sum()),'| buiten opdrachtzones:',buiten)
# bevroren: veer (alle r/s + W (26,22),(28,23),(25,23)) en oog/masker (kopvak x22-32,y18-34 behalve toegestane px)
veer=[(x,y) for y,x in zip(*np.where((b=='r')|(b=='s')))]+[(26,22),(28,23),(25,23)]
print('veer diff:',sum(int(g[y,x]!=b[y,x]) for x,y in veer),'(van',len(veer),'px)')
toe={(22,27),(22,28),(24,30),(31,18),(32,18),(32,19)}
kop=sum(int(d[y,x]) for y in range(18,35) for x in range(22,33) if (x,y) not in toe)
print('oog/masker-vak x22-32 y18-34 diff (excl. toegestane):',kop)
sil=((g!='.')!=(b!='.')); print('silhouet:',[(x,y,'+' if g[y,x]!='.' else '-') for y,x in zip(*np.where(sil))])
open('rufflet_r8.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
src=Image.open('../sprite_r7/rufflet_r7.png'); pl=src.getpalette()
idx=np.vectorize(CH.index)(g).astype('uint8'); p=Image.fromarray(idx,'P'); p.putpalette(pl); p.save('rufflet_r8.png',transparency=0); p.info['transparency']=0
r=p.convert('RGBA'); t=Image.new('RGB',(64,64),(255,255,255)); t.paste(r,(0,0),r); t.resize((512,512),Image.NEAREST).save('rufflet_r8_8x.png')
