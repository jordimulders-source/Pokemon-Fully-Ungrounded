# Ronde 11 op r9: alleen fles + schouderkoepel uit r10 (zonder binnenlijn r24), de verticale scheidingslijn in de
# rechtervuist weg, linkeroog = gespiegeld r9-rechteroog met 1 kolom oogwit minder aan de buitenkant.
import numpy as np; import maak_r10 as m10
T,ZW,S0,S1,S2,S3,S4,WIT=0,1,2,3,4,5,6,14
R9=m10.R9
LOG={}
def zet(A,p,v,k):
    if A[p]!=v: LOG.setdefault(k,[]).append((p,int(A[p]),int(v))); A[p]=v
BINNENLIJN=[(23,14),(24,14),(24,15),(24,16),(24,17),(24,18),(24,19),(25,15)]
def schouder(A):
    S=m10.schouder(R9,-2,0)
    for y,x in zip(*np.where(S!=R9)):
        if (y,x) not in BINNENLIJN: zet(A,(y,x),S[y,x],'schouder + fles uit r10')
    return A
# rechtervuist r9: kolom x22 vormt met de glasranden x21/x23 een rechtopstaande "vinger"; de donkere pixels in die kolom
# (26,22) en (29,22) zijn de scheidingslijn -> buurtint van de vuist (boven/onder dezelfde kolom)
def vuist(A):
    zet(A,(26,22),S2,'vuist: scheidingslijn weg (buurtint (27,22))')
    zet(A,(29,22),S1,'vuist: scheidingslijn weg (buurtint (28,22)/(30,22))')
    return A
# ogen
OUD_L={(15,22):5,(16,22):4,(16,24):5,(16,23):4,(17,23):5,(17,24):5,(17,25):4,(18,24):5,(18,25):4}   # tinten van voor oog_r8 (r8/log.txt)
RECHTS=[(y,x) for y in range(14,19) for x in range(28,34) if R9[y,x] in (S0,ZW,WIT) and not (y<=15 and x<30 and R9[y,x]!=S0)]
def linkeroog(A):
    for p,v in OUD_L.items(): zet(A,p,v,'r9-linkeroog weg (oude tint)')
    pix={}
    for y,x in RECHTS:
        if (y,x) in [(14,32),(14,33),(15,30),(15,31),(15,33),(16,28),(16,29),(16,33),(17,28)] or R9[y,x] in (ZW,WIT):
            pix[(y,61-x)]=R9[y,x]                                              # spiegelen binnen x28-33
    # 1 kolom oogwit aan de buitenkant (m=29) weg, het ooglid op m=28 in rij 16 schuift 1 naar binnen
    for y in (16,17,18): pix.pop((y,29),None)
    if (16,28) in pix: pix[(16,29)]=pix.pop((16,28))
    w=[(y,m) for (y,m),v in pix.items() if v in (ZW,WIT)]
    cx=np.mean([m for y,m in w]); dx=int(round(24.0-cx))
    for (y,m),v in pix.items(): zet(A,(y,m+dx),v,'linkeroog: gespiegeld r9-rechteroog, 1 kolom smaller (dx %d)'%dx)
    return A
def bouw():
    LOG.clear(); A=R9.copy(); A=schouder(A); A=vuist(A); A=linkeroog(A); return A
# ---------- variant biceps (Jordi: "ja een schouder en een biceps oid") ----------
# Model r5 (overlay op 20x, lijf -2): schouderkoepel boven, daaronder de bovenarm die verder naar buiten steekt, schuine plooi
# van de oksel naar linksboven tot de buitenrand, elleboog linksonder. De sprite is hier 1-3 px breder dan het model
# (groter hoofd), dus de plooi ligt 1-2 px links van de modelplooi (23,16)-(24,17)-(24,18) en eindigt vóór (25,19)/de hand.
BICEPS={
 # omtrek: koepel buigt onderaan terug (22,14), bovenarm 1-2 px naar buiten (omtrekpixels verschoven), elleboog (33,12) blijft
 (22,13):T,(22,14):S0,(24,12):S0,(25,11):S0,(26,11):S0,(27,10):S0,(28,10):S0,(29,10):S0,
 # plooi, schuin
 (23,14):S0,(24,15):S0,(24,16):S0,(23,15):S2,
 # sikkel onder de koepel
 (22,15):S2,
 # bovenarm: licht op de top, d, sikkel naar de elleboog
 (24,13):S4,(24,14):S4,(25,12):S4,(25,13):S4,(25,14):S3,(25,15):S3,(26,12):S4,(26,13):S3,
 (27,11):S3,(27,12):S3,(28,11):S3,(29,11):S2,(30,12):S2,(31,12):S1,(32,12):S1,
}
def biceps(A):
    A=A.copy()
    for p,v in BICEPS.items(): zet(A,p,v,'biceps-variant')
    return A
