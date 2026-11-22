# telt per aanzicht en zone hoeveel pixels afwijken van de kale 2x-verkleining (h3_*_10)
def load(f): return [l.rstrip('\n') for l in open(f) if l.strip()]
K={'.':'.','o':'o','b':'o'}
for c in 'FhmseC c': pass
def cls(c):
    if c=='.': return '.'
    if c in 'ob': return 'o'
    if c in 'Cc': return 'C'
    if c in 'Yyk': return 'Y'
    return 'F'
Z={'voor':  [('pluim+steel',0,7),('kop/oren',4,9),('gezicht/wangen',10,15),('lijf/poten',16,21)],
   'achter':[('oren',0,4),('kop/pluim/wangen',5,9),('lijf/staart',10,18)],
   'opzij': [('pluim+staart',0,21,17,25),('oren',4,9,0,10),('kop/oog/wang',10,17,0,9),('lijf',9,19,9,20),('poten',19,21,0,19)]}
for n,o in (('voor','h3_front_10.txt'),('achter','h3_back_10.txt'),('opzij','h3_side_10.txt')):
    A=load(o); B=load(n+'.txt')
    tot=sum(1 for y in range(len(A)) for x in range(len(A[0])) if A[y][x]!=B[y][x])
    tcls=sum(1 for y in range(len(A)) for x in range(len(A[0])) if cls(A[y][x])!=cls(B[y][x]))
    sil=sum(1 for y in range(len(A)) for x in range(len(A[0])) if (A[y][x]=='.')!=(B[y][x]=='.'))
    print(f'{n}: {tot} px anders (kleurtint meegeteld), {tcls} px andere klasse, silhouet {sil} px')
    for z in Z[n]:
        nm,y0,y1=z[:3]; x0,x1=(z[3],z[4]) if len(z)>3 else (0,len(A[0])-1)
        d=sum(1 for y in range(y0,y1+1) for x in range(x0,x1+1) if cls(A[y][x])!=cls(B[y][x]))
        print(f'   {nm:16s} {d} px andere klasse')
