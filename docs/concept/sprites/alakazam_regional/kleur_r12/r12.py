# r12.py: rechterbovenarm helemaal grijs (Jordi: "rechts dan ook he grappenmaker, bovenarm"). Alleen kleur, zone x36-41, y28-34.
# Armstuk x37-40, rij 29-33 (model D op x37-38, B op x39-40): licht linksboven -> b links, c rechts; omlijning o bestaat al rondom.
import pal,numpy as np
B0=[list(r) for r in pal.load('basis_r11.txt')]
W={(37,29):'b',(38,29):'b',(38,30):'b',(38,31):'b',(39,30):'c',(39,31):'c',(39,32):'c',(40,33):'c'}
R=[r[:] for r in B0]
for (x,y),c in W.items(): R[y][x]=c
R=[''.join(r) for r in R]; open('var_r12.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,'var_r12.png')
a=np.array([list(r) for r in R]); b=np.array(B0); ys,xs=np.where(a!=b)
print(len(xs),'px gewijzigd; buiten x36-41,y28-34:',[(x,y) for x,y in zip(xs,ys) if not (36<=x<=41 and 28<=y<=34)])
