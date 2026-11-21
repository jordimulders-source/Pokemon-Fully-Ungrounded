# diff.py eind.txt : afwijkingen per zone t.o.v. de kale reductie (stap1.txt = kaal.npy in eindletters)
import sys
A=[r.rstrip('\n') for r in open('stap1.txt')]; B=[r.rstrip('\n') for r in open(sys.argv[1])]
def zone(y,x):
    if 14<=y<=16 and 8<=x<=12: return 'oog'
    if 13<=y<=21 and x<=8: return 'snavel'
    if y<=7: return 'kuif'
    if y<=14 and (x<=5 or x>=21): return 'kuif'
    if y<=14 and A[y][x] in 'abcK' and B[y][x] in 'abcK' and y<=9: return 'kuif'
    if y<=23 and x<=21: return 'kop'
    if 48<=y and x<=27: return 'poten/klauwen'
    if 42<=y<=47 and 10<=x<=24: return 'dijen (banden)'
    if 44<=y<=49 and 24<=x<=29: return 'flank'
    if x<=9 and 24<=y<=42: return 'nabije vleugel'
    if 22<=y<=32 and 6<=x<=17: return 'halsband'
    if 30<=y<=41 and 6<=x<=22: return 'buik'
    return 'grote vleugel/staart'
from collections import Counter
n=Counter(); t=Counter(); d=Counter()
for y in range(len(A)):
    for x in range(38):
        z=zone(y,x)
        if A[y][x]!='.' or B[y][x]!='.': t[z]+=1
        if A[y][x]!=B[y][x]:
            n[z]+=1
            G=lambda c: 'K' if c in 'Kn' else 'L' if c in 'abc' else 'G' if c in 'ghiW' else 'S' if c in 'stu' else c
            k='silhouet' if (A[y][x]=='.')!=(B[y][x]=='.') else ('groep' if G(A[y][x])!=G(B[y][x]) else 'tint')
            d[(z,k)]+=1
for z in t: print('%-22s %4d van %4d px  (silhouet %3d, lijn/vlak-wissel %3d, alleen tint %3d)'%(z,n[z],t[z],d[(z,'silhouet')],d[(z,'groep')],d[(z,'tint')]))
print('totaal',sum(n.values()),'van',sum(t.values()))
