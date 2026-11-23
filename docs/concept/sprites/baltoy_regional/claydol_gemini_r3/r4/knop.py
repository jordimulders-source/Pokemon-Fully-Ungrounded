# Punten 2+3: stafknoppen per pixel uit het model (natieve modelpixel, geen middeling) naar de stafgroep:
# >=195 glans 2 | 160-195 vlak 5 | 100-160 schaduw/zachte barst 7 | <100 barst 8. K en rood blijven.
import sys, numpy as np; sys.path.insert(0,'r4')
from natcoord import S3, NY, NX, lum, RST, LST
def tint(l): return 2 if l>=195 else 5 if l>=160 else 7 if l>=100 else 8
ZR=np.zeros((64,64),bool); ZR[37:48,:]=True; ZR&=RST
ZL=np.zeros((64,64),bool); ZL[32:43,:]=True; ZL&=LST
def knoppen(S):
    log=[]
    for Z,naam in ((ZR,'knop rechterstaf'),(ZL,'knop linkerstaf')):
        for y,x in zip(*np.where(Z&np.isin(S,(2,4,5,6,7,8)))):
            v=tint(lum(y,x))
            if v!=S[y,x]: log.append((naam,int(y),int(x),int(S[y,x]),v)); S[y,x]=v
    return log

def scherp(S):
    # (a) zachte barst (model 100-160, binnen de knop, niet aan de buitenrand) die een gat tussen twee barstpixels (8) overbrugt -> 8:
    #     één barstlijn in één tint i.p.v. 7/8 om en om. (c) donkere pixel (8) op de buitenrand rechts/onder -> K (randregel g3).
    log=[]; T=np.pad(S==0,1,constant_values=True)
    for Z,naam in ((ZR,'knop rechterstaf'),(ZL,'knop linkerstaf')):
        rand=lambda y,x: T[y:y+3,x:x+3].any()
        for y,x in zip(*np.where(Z&(S==7))):
            brug=any(S[y+dy,x+dx]==8 and S[y-dy,x-dx]==8 for dy,dx in ((1,0),(0,1),(1,1),(1,-1)))
            if not rand(y,x) and 100<=lum(y,x)<160 and brug:
                log.append((naam,int(y),int(x),7,8)); S[y,x]=8
        for y,x in zip(*np.where(Z&(S==8))):
            if T[y+1,x+2] or T[y+2,x+1]: log.append((naam,int(y),int(x),8,10)); S[y,x]=10
    return log
