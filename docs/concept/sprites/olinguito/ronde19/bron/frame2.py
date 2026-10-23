"""Frame 2: x<40 (kop, armen, klauwen, verre achterpoot): per pixel dezelfde beweging als ronde 18
(1 rij omhoog, behalve waar ronde 18 stil bleef); x>=40 uit ronde 18 frame 2 (na dezelfde knip van kolom 40-41).
Daarna handcorrecties (fix.py) in samen_f2.txt."""
A=[l.rstrip('\n') for l in open('samen_f1.txt')]
A18=[l.rstrip('\n') for l in open('r18_f1.txt')]
B18=[l.rstrip('\n') for l in open('r18_f2.txt')]
R=[r[:40]+r[42:]+'..' for r in B18]
out=[]
for y in range(64):
    row=''
    for x in range(64):
        if x>=40: row+=R[y][x]; continue
        up=A[y+1][x] if y<63 else '.'
        stil = B18[y][x]!='.' and B18[y][x]==A18[y][x] and (y==63 or B18[y][x]!=A18[y+1][x])
        if y>=46 and 33<=x<40: row+=A[y][x]; continue   # verre achterpoot staat stil
        row+= A[y][x] if (stil and y>=40) else up
    out.append(row)
open('samen_f2.txt','w').write('\n'.join(out)+'\n')
