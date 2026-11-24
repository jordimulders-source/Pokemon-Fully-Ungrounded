# bewijs.py oud.txt nieuw.txt : pixeldiff in bevroren zones + aantal gewijzigde pixels per werkzone
import sys
A=[l.rstrip('\n') for l in open(sys.argv[1])][:64]; B=[l.rstrip('\n') for l in open(sys.argv[2])][:64]
P=lambda R,x,y: R[y][x] if 0<=x<64 and 0<=y<64 else '.'
edge=lambda R,x,y: R[y][x]!='.' and any(P(R,x+dx,y+dy)=='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
Z={}
Z['silhouet (alpha)']=[(x,y) for y in range(64) for x in range(64)]
Z['buitenlijn + selout (randpixels)']=[(x,y) for y in range(64) for x in range(64) if edge(A,x,y)]
Z['ogen (x13-16, x22-25, y38-42)']=[(x,y) for y in range(38,43) for x in list(range(13,17))+list(range(22,26))]
Z['latei (x12-25, y44-47)']=[(x,y) for y in range(44,48) for x in range(12,26)]
door=[]
for y in range(48,61):
    r=A[y]; l=next((x for x in range(11,20) if r[x]=='+'),12); rr=next((x for x in range(23,28) if r[x]=='+'),26)
    door+= [(x,y) for x in range(l,rr+1)]
Z['deur (linker t/m rechter deurstijl, y48-60)']=door
Z['gezichtsblok-indeling: kap y33-37 x11-30 en zijkant x30-33 y37-60']=[(x,y) for y in range(33,38) for x in range(11,31)]+[(x,y) for y in range(37,61) for x in range(30,34) if A[y][x] in 'de']
for k,pts in Z.items():
    if k.startswith('silhouet'): d=sum((A[y][x]=='.')!=(B[y][x]=='.') for x,y in pts)
    else: d=sum(A[y][x]!=B[y][x] for x,y in pts)
    print(f'{k}: diff {d}')
W={'gevels: topgevels (x33-52,y3-10)':(33,3,52,10),'gevels: middelste + onderste + voeten (x16-42,y8-28)':(16,8,42,28),'gezichtsblok (x7-31,y36-60)':(7,36,31,60),'vleugel (x2-6,y38-58)':(2,38,6,58),
   'rechter onderblok voorkant (x33-41,y44-60)':(33,44,41,60),'bergwand + terraszijkanten (x41-60,y9-40)':(41,9,60,40)}
tot=sum(A[y][x]!=B[y][x] for y in range(64) for x in range(64)); seen=set()
for k,(x0,y0,x1,y1) in W.items():
    pts=[(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1) if (x,y) not in seen]; seen|=set(pts)
    print(f'{k}: {sum(A[y][x]!=B[y][x] for x,y in pts)} px')
print('buiten de werkzones:',sum(A[y][x]!=B[y][x] for y in range(64) for x in range(64) if (x,y) not in seen),'px; totaal',tot)

ch=[(x,y,A[y][x],B[y][x]) for y in range(64) for x in range(64) if edge(A,x,y) and A[y][x]!=B[y][x]]
print('gewijzigde randpixels (alleen kleur, alpha gelijk):',len(ch),[(x,y) for x,y,_,_ in ch])
