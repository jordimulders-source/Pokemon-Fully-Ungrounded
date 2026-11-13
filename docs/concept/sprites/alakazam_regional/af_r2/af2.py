# af2.py: af_r1/raster.txt -> raster.txt. Reparaties van de eindkeuring; elke pixel met verwachte oude letter.
B=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open('basis_af_r1.txt')][:64]
R=[r[:] for r in B]; zone={}
E=[]  # (zone, x, y, verwacht, nieuw)
def z(n,pts,old,new): E.extend((n,x,y,old,new) for x,y in pts)
z('1 selout grijs',[(29,7),(22,16),(21,17),(14,29),(13,30),(12,31),(12,32),(20,43),(20,44),(19,45),
   (51,27),(50,28),(49,29),(49,30),(48,31),(47,31)],'o','d')
# verre scheen: opdracht zei c; c op de buitenrand = lichte kleur op de rand (controle: open rand) -> d
z('1 selout verre scheen',[(32,49),(32,50),(32,51),(32,52),(31,53),(31,54),(30,55),(29,56)],'o','d')
z('2 selout zwart',[(15,19),(16,19),(17,18),(18,18),(19,18),(20,18),(14,20),(13,21),(13,22),(12,23),(12,24),
   (14,27),(14,28),(11,34),(18,46),(18,47),(18,48),(18,49),(18,50),(41,33),(42,33),(43,33)],'o','k')
z('3 hooglicht',[(22,40),(22,41),(22,42),(13,31),(13,32),(14,30)],'b','a')   # (14,30) erbij: anders is a op de bovenarm maar 2 px
z('4 banding bovenarm',[(16,29),(15,30)],'c','b'); z('4 banding bovenarm',[(17,29),(16,30)],'d','c')
z('5 schaduwkant hand',[(11,43),(12,43),(13,44)],'d','o')
z('6 deuk kop',[(23,13)],'.','d'); z('6 deuk kop',[(24,13)],'d','b')
z('7 onderarm',[(42,38),(49,38)],'o','.'); z('7 onderarm',[(42,37)],'k','o')
# gevolgen: (29,7) d liet (30,7) als losse o achter in de oorinkeping; (11,43)/(12,43) o liet (11,42) d als 1 px
z('1 selout grijs',[(30,7)],'o','d'); z('5 schaduwkant hand',[(11,42)],'d','c')
for n,x,y,old,new in E:
    if B[y][x]!=old: print('AFWIJKING',n,x,y,'staat',B[y][x],'verwacht',old)
    R[y][x]=new; zone[(x,y)]=n
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
diff=[(x,y) for y in range(64) for x in range(64) if R[y][x]!=B[y][x]]
print('gewijzigd tegen af_r1:',len(diff),' buiten zones:',[p for p in diff if p not in zone])
from collections import Counter
for n,c in Counter(zone[p] for p in diff).items(): print(f'  {n}: {c} px')
print('silhouet: erbij',[(x,y) for x,y in diff if B[y][x]=='.'],'eraf',[(x,y) for x,y in diff if R[y][x]=='.'])
