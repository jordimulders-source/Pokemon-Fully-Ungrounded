# r21 bouw_v.py (vanaf r20: bal = r20, alleen de V verandert). Punt blijft op (30,33) en bovenrand op rij 25,
# zoals r18/r20 (Jordi: "de positie verandert niet vanuit het midden", "alleen de vorm is anders in perspectief").
# Studie (studie_v.png): Throh/Sawk (kraag in driekwart naar links): verre flank kort en steil, volgt de romp; nabije
# flank lang en flauwer; punt onder het midden van het gezicht; banen 2 px (ver) en 2-3 px (nabij), één donkere tint.
# Daarom krijgen de flanken hier een rechte, gelijkmatige helling (andere hoek dan r18: links steil, rechts flauw).
# Tint = 3 (donkergrijs van de r18-V), alleen op romppixels (7/8): kop, ballen en borstvuist blijven ervoor.
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
PX,PY,TOP=30,33,25
def flank(x0):                       # x op elke rij 25..33 langs een rechte lijn van (x0,25) naar de punt
    return {y: round(x0+(PX-x0)*(y-TOP)/(PY-TOP)) for y in range(TOP,PY+1)}
def gevuld(lx,rx):
    L,R=flank(lx),flank(rx); return {(x,y) for y in L for x in range(L[y],R[y]+1)}
def banen(lx,rx,bl,br):              # bl/br = baanbreedte ver/nabij; binnenkant blijft wit
    L,R=flank(lx),flank(rx); s=set()
    for y in L:
        for x in range(L[y],R[y]+1):
            if x<L[y]+bl or x>R[y]-br: s.add((x,y))
    return s
VAR={'bokser':      gevuld(28,37),          # A: gevuld, verre flank steil (28->30), nabije flauw (37->30)
     'var/v_B_banen':banen(28,37,2,3),      # B: kraag als Throh/Sawk: verre baan 2 px, nabije 3 px, wit ertussen
     'var/v_C_steil':gevuld(29,37)}         # C: als A, verre flank nog korter/steiler (29->30)
if __name__=='__main__':
    for naam,V in VAR.items():
        a=np.load('ruw.npy'); a[22,25]=4 if a[22,25]==1 else a[22,25]   # randpixel bal van r20
        for x,y in V:
            if a[y,x] in(7,8): a[y,x]=3
        save(a,naam); print(naam)
        for j in range(24,35): print('%2d '%j+''.join(str(v) if v else '.' for v in a[j,20:42]))
