# diff.py kaal.txt raster.txt: afwijkingen van de kale reductie per zone
import sys
A=[l.rstrip('\n') for l in open(sys.argv[1])][:64]; B=[l.rstrip('\n') for l in open(sys.argv[2])][:64]
Z=[('ogen (toegestaan)',12,37,26,43),('deur+latei',11,44,27,60),('gevels+boventerrassen',18,3,56,28),('terrassen/blokken rechts',30,26,63,63),('linkervleugel+rest',0,0,64,64)]
cnt={z[0]:0 for z in Z}; sel=0; tot=0
for y in range(64):
  for x in range(64):
    a,b=A[y][x],B[y][x]
    if a==b: continue
    tot+=1
    if a=='X' and b=='+': sel+=1; continue
    for n,x0,y0,x1,y1 in Z:
      if x0<=x<=x1 and y0<=y<=y1: cnt[n]+=1; break
print('totaal',tot,'waarvan selout (zwart->lijntint op de buitenlijn linksboven)',sel)
for k,v in cnt.items(): print(k,v)
