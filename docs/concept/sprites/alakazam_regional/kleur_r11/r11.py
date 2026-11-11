# r11.py: onderarmen zwart, bovenarmen grijs, zoals het model (Jordi: "het model had de onderarm zwart gemaakt en de bovenarmen grijs, laten we dat doen").
# Alleen kleur: alpha-diff 0. Tinten per pixel uit de modelklasse (kaart.py: B->b, C->c, D->d; K -> k/m/n met licht linksboven). Omlijning o blijft.
import pal,numpy as np
B0=[list(r) for r in pal.load('basis_L1.txt')]
W={}
def p(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': W[(x0+i,y)]=c
# links bovenarm (model rij 28-32 x13-17: C D D D / B B D / B B D / B B C / B B D)
p(28,15,"dddd"); p(29,15,"bcd"); p(30,14,"bcd"); p(31,13,"bbc"); p(32,13,"bbc")   # schoongemaakt: schaduwband onder de plaat, b links, c/d rechts
# links onderarm zwart (model K rij 34-39 x12-20), licht linksboven, k onder/rechts
p(34,12,"nnnmm"); p(35,12,"nnmmmm"); p(36,13,"nmmmmmkk"); p(37,14,"mmmmmkk"); p(38,16,"mmkkk"); p(39,16,"kkkk")
# rechts bovenarm grijs (model B op (39,30-32), (40,33)); de plaat (37-38,29), (38,30-31) blijft zwart
p(30,39,"b"); p(31,39,"b"); p(32,39,"b"); p(33,40,"b")
# rechts onderarm zwart (model K rij 33-37 x40-48)
p(32,47,"n"); p(33,44,"nnnn"); p(34,39,"o"); p(34,41,"nnmmmmm"); p(35,40,"nmmmmmmm"); p(36,40,"mmmmmmmkk"); p(37,41,"okkkkkkk")   # (41,37) is silhouetrand: o
ZONES=[(11,26,21,40),(36,28,49,38)]
R=[r[:] for r in B0]
for (x,y),c in W.items():
    if (R[y][x]=='.')!=(c=='.'): print('SILHOUET',x,y)
    if R[y][x]=='o': print('LET OP: omlijning overschreven',x,y)
    R[y][x]=c
R=[''.join(r) for r in R]; open('var_r11.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,'var_r11.png')
a=np.array([list(r) for r in R]); b=np.array(B0); ys,xs=np.where(a!=b)
buiten=[(x,y) for x,y in zip(xs,ys) if not any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in ZONES)]
print(len(xs),'px gewijzigd; buiten de armzones:',buiten)
