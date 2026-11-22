# Vleugel (grote, verre vleugel) opnieuw inkleuren binnen de bestaande omtrek uit de reductie:
# dekveren b met c-sikkel aan de voorrand, slagpennen a met 2 pennenlijnen (K) op de plekken van de modelstippellijnen, b-rand rechts van elke lijn.
R=[list(r.rstrip('\n')) for r in open('r.txt')]
E={22:22,23:24,24:26,25:26,26:27,27:28,28:29,29:30,30:31,31:31,32:32,33:33,34:33,35:33,36:33,37:34,38:34,39:34,40:34,41:34,42:34,43:34,44:34,45:34,46:34,47:34,48:35,49:35,50:36,51:36,52:36,53:37,54:37}
L={23:20,24:20,25:19,26:19,27:18,28:18,29:18,30:18,31:18,32:18,33:19,34:19,35:19,36:20,37:21,38:21,39:22,40:23,41:24,42:24,43:25,44:25,45:29,46:31,47:30,48:29,49:28,50:27,51:28,52:29,53:31,54:33}
C={23:(20,21),24:(20,22),25:(19,21),26:(19,20),27:(18,19),28:(18,18)}
A={33:27,34:28,35:28,36:29,37:29,38:30,39:30,40:31,41:31,42:32}
B={36:23,37:24,38:24,39:25,40:25,41:26,42:27,43:27,44:28,45:29,46:29,47:30,48:30,49:31,50:32,51:32,52:33,53:34}
for y in range(23,55):
    l,e=L[y],E[y]
    for x in range(l,e):
        if y<=31: v='b'; v='a' if x>=e-(2 if y>=28 else 1) else v
        elif y<=34: v='b' if x<l+5-(y-32) else 'a'
        else: v='a'
        if y in C and C[y][0]<=x<=C[y][1]: v='c'
        if 35<=y<=41 and x==l: v='b'
        R[y][x]=v
    R[y][e]='K'
    for D in (A,B):
        if y in D and l<D[y]<e:
            R[y][D[y]]='K'
            if D[y]+1<e: R[y][D[y]+1]='b'
# randen links-onder van de vleugelpunt en onderrand
for y,x in ((50,26),(51,27),(52,28),(53,29),(53,30),(54,31),(54,32)): R[y][x]='K'
for x in range(33,37): R[55][x]='K'
R[55][37]='.'; R[54][37]='K'; R[55][32]='.'
for y in range(48,56):
    for x in range(36,38):
        if x>E.get(y,99): R[y][x]='.'
# lila flank
fl={45:'Kghg K',}
R[44][24]='K'
R[45][24:29]=list('KhggK')
R[46][24:31]=list('KKhhgK.')[:7]
R[46][24:31]=list('.KhhggK'); R[46][24]='h' if False else R[46][24]
R[47][24:30]=list('Khggg'+'K')
R[48][24:29]=list('KhggK')
R[49][24:28]=list('KggK')
R[50][25]='.'
open('r.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
for i in range(21,61): print('%2d'%i,''.join(R[i]))
