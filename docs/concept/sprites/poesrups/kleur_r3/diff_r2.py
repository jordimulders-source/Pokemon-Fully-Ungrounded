"""diff_r2.py: pixeldiff r3 t.o.v. r2 (raster), per zone; alles buiten de zones moet 0 zijn; alpha van het lijf (buiten kam/pootjes) diff 0."""
import os
H=os.path.dirname(os.path.abspath(__file__))
A=[l.rstrip('\n') for l in open(os.path.join(H,'raster.txt'))][:64]
B=[l.rstrip('\n') for l in open(os.path.join(H,'..','kleur_r2','raster.txt'))][:64]
Z={'kam':[(15,24,23,32),(24,27,30,33),(30,31,36,36),(36,34,42,39),(41,39,45,43),(43,44,47,46)],
   'pootjes':[(34,59,37,61)],'loklijnen':[(22,52,52,58)],'verre oog':[(8,55,9,56)]}
n={k:0 for k in Z}; na={k:0 for k in Z}; buiten=[]
for y in range(64):
    for x in range(64):
        if A[y][x]==B[y][x]: continue
        for k,rs in Z.items():
            if any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in rs):
                n[k]+=1; na[k]+=(A[y][x]=='.')!=(B[y][x]=='.'); break
        else: buiten.append((x,y,B[y][x],A[y][x]))
for k in Z: print(f'{k}: {n[k]} px gewijzigd, waarvan alpha {na[k]}')
print('buiten de zones:',len(buiten),buiten)
