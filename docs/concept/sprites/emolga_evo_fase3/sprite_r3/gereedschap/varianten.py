# varianten.py: Jordi's twee goedgekeurde afwijkingen als bovenlaag op A0 (alleen kleur/kap, silhouet gelijk):
#  C: oogvlek (masker) in het donkere leigrijs van het vizier van fase 2 (emolga_evo/af/model.png: E 64/64/82, G 98/96/114,
#     D 38/38/52): masker licht O en N -> G, omlijning M -> E (de variant N -> E, M -> D maakte het oog onleesbaar: zwart op 64/64/82). Vorm uit het model; mond en wangplukken blijven.
#  A: zwarte kap op de kruin (onderaan tussen de oren) met een V-punt omhoog naar de ogen (vorm-voorbeeld gemini/r7.png, Emolga):
#     v=2 (gekozen): punt op 25,49, rij 50 x24-30 (kruin); het witte voorhoofd (rij 48 x24-26, rij 49 x23-24 en 26-28) blijft als witte band.
#     v=1 (punt 25,48 tegen de maskerbrug) liet twee losse witte stipjes onder het masker over die als slagtanden lazen.
#  A.png: V over het gele voorhoofdvlekje (vlekje weg) | A_geel.png: gele vlekje blijft op de kap.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet
K,Dk,E,Gl,y,Y,L,B,W,w,M,N,O=range(1,14)
a0=np.asarray(Image.open(D+'sprite_r1/A0.png')).astype(int)
def maak(geel,v=2):
    o=a0.copy(); log=[]
    def zet(x,yy,v,r):
        if o[yy,x]!=v: log.append((x,yy,palet.CH[o[yy,x]],palet.CH[v],r)); o[yy,x]=v
    # C
    for yy in range(42,50):
        for x in range(20,34):
            if o[yy,x] in (M,N,O): zet(x,yy,{O:Gl,N:Gl,M:E}[o[yy,x]],'C: vizier fase 2')
    # A
    if v==1: kap=[(25,48)]+[(x,49) for x in (24,25,26)]+[(x,50) for x in range(23,31)]
    else:    kap=[(25,49)]+[(x,50) for x in range(24,31)]
    for x,yy in kap: zet(x,yy,Dk,'A: kap met V')
    zet(26,51,Dk,'A: kap (onderkant voorhoofdstreep)')
    if geel:
        for (x,yy),v in (((25,49),L),((25,50),Y),((26,50),Y),((26,51),y)): zet(x,yy,v,'A_geel: gele voorhoofdvlekje van het model blijft')
    # lichtkant van de kap (linksboven, tegen het wit) iets lichter voor volume
    for x,yy in ((24,49),(23,50),(24,50)):
        if o[yy,x]==Dk and (x,yy) in kap: zet(x,yy,E,'A: kap licht linksboven')
    return o,log
for naam,geel,v in (('A',False,2),('A_geel',True,2),('tussen/A_v1',False,1)):
    o,log=maak(geel,v); palet.opslaan(o,D+'sprite_r1/%s.png'%naam)
    from collections import Counter
    print(naam,len(log),Counter(r[4] for r in log))
