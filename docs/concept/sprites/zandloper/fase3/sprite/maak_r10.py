# Ronde 10 op r9: linkerschouder als ronde koepel (fles 1-3 px verschoven), rechtervuist zonder "twee vingers",
# oogvarianten. Alleen verschuiven, weghalen, tint uit het palet (14 kleuren van r8/r9).
import numpy as np; from PIL import Image; import maak_r6 as m, maak_r9 as m9, schoon
T,ZW,S0,S1,S2,S3,S4,WIT=0,1,2,3,4,5,6,14
GLAS=(7,8,9,10)
R9=np.asarray(Image.open('r9/zandloper_fase3.png')).astype(int)
H=m.H
LOG={}
def zet(A,p,v,k):
    if A[p]!=v: LOG.setdefault(k,[]).append((p,int(A[p]),int(v))); A[p]=v
# ---------- 1 linkerschouder ----------
# fles = alles wat niet hoofd en niet leeg is in x13-20, rij 5-17 (glas, zwarte omlijning en het zand in de flesbuik)
R8=m9.R8
FLES=[(y,x) for y in range(5,18) for x in range(13,21) if R9[y,x]!=T and not H[y,x]]
# bron = de fles zoals in r8 (2 rijen hoger in r8-coordinaten); daar lag het glas nog tegen het hoofd (11,20),(12,20)
FLES8=[(y,x) for y in range(3,16) for x in range(13,22) if R8[y,x]!=T and not (H[y,x] and R8[y,x] not in GLAS)]
# koepel (r5-model: ronde deltaspier van de nek naar buiten en omlaag; overlay r10/overlay_schouder.png):
# omtrek als bolle boog, horizontale stukken bovenaan (2,2), dan diagonaal, dan verticale stukken (2,2,3,4) die al staan
KOEPEL_LIJN=[(15,19),(15,20),(16,17),(16,18),(17,16)]                 # (18,15)..(24,13) staan al (Jordi: "bijna goed")
# tinten per pixel, naar het model (overlay r10/overlay_schouder.png): grote lichte bolling midden-boven, d eromheen,
# c tegen de nek en als sikkel boven de binnenlijn; binnenlijn r24 (model: dunne lijn x15-23, links iets omhoog naar de rand)
KOEPEL={
 (16,19):S3,
 (17,17):S3,(17,18):S4,(17,19):S3,
 (18,16):S3,(18,17):S4,(18,18):S4,(18,19):S2,
 (19,16):S4,(19,17):S4,(19,18):S4,(19,19):S3,(19,20):S2,
 (20,15):S3,(20,16):S4,(20,17):S4,(20,18):S4,(20,19):S3,(20,20):S2,
 (21,15):S3,(21,16):S4,(21,17):S4,(21,18):S3,(21,19):S3,(21,20):S3,
 (22,14):S2,(22,15):S3,(22,16):S4,(22,17):S3,(22,18):S3,(22,19):S2,(22,20):S2,
 (23,15):S2,(23,16):S2,(23,17):S2,(23,18):S2,(23,19):S2,
 (23,14):S0,(24,14):S3,(24,15):S0,(24,16):S0,(24,17):S0,(24,18):S0,(24,19):S0,
 (25,15):S3,
}
def schouder(A0,dy,dx):
    A=A0.copy()
    for p in FLES: A[p]=T
    for y,x in FLES8:
        q=(y+2+dy,x+dx)
        if not H[q] and A[q]==T: A[q]=R8[y,x]
    for p in KOEPEL_LIJN: A[p]=S0                                     # koepel komt voor de fles
    for p,v in KOEPEL.items(): A[p]=v
    if A[16,16]==T and A[15,16]!=T: A[16,16]=S0                     # flesbuik sluit op de koepelomtrek
    for y in range(64):
        for x in range(64):
            if A[y,x]!=A0[y,x]: LOG.setdefault('schouder (fles %+d,%+d)'%(dy,dx),[]).append(((y,x),int(A0[y,x]),int(A[y,x])))
    return A
# ---------- 2 rechtervuist: één ronde vuist (model r5: x20-23, licht bovenop, knokkellijn schuin vanaf de boeirand
# (27-28,21) naar (29,22-23), schaduw onderaan). Linkerrand grote boei 1 px naar rechts (x23 -> x24) in rij 25-30.
VUIST={(25,20):S3,(25,21):S4,(25,22):S4,(25,23):S3,
       (26,20):S2,(26,21):S3,(26,22):S3,(26,23):S2,
       (27,22):S3,(27,23):S2,(28,22):S2,(28,23):S2,
       (29,21):S2,(29,22):S0,(29,23):S0,
       (30,21):S2,(30,22):S2,(30,23):S1}
def vuist(A):
    for y in range(25,31):
        if A[y,23] in GLAS: zet(A,(y,24),7,'grote boei: linkerrand 1 px naar rechts (verschoven)')
    for p,v in VUIST.items(): zet(A,p,v,'rechtervuist (tint/lijn uit het model)')
    return A
# ---------- 3 ogen (alleen bestaande oogpixels verschuiven of weghalen) ----------
def ogen(A,v):
    if v=='a':     # beide pupillen naar links
        for p,c in {(17,23):ZW,(17,24):ZW,(17,25):WIT,(18,24):ZW,(18,25):WIT}.items(): zet(A,p,c,'oog a: linkerpupil 1 px naar links')
        for p,c in {(17,29):ZW,(18,29):ZW,(17,30):WIT,(18,30):WIT}.items(): zet(A,p,c,'oog a: rechterpupil 1 px naar links')
    if v=='b':     # beide pupillen naar rechts (linkerpupil staat al rechts)
        for p,c in {(17,31):ZW,(18,31):ZW,(17,30):WIT,(18,30):WIT}.items(): zet(A,p,c,'oog b: rechterpupil 1 px naar rechts')
    if v=='c':     # linkeroog 1 px smaller, pupil 1x2 zoals rechts
        for p,c in {(17,25):S3,(18,25):S3,(18,24):ZW}.items(): zet(A,p,c,'oog c: linkeroog 1 px smaller')
    return A
def bouw(fles=(-2,0),oog='a'):
    LOG.clear(); A=schouder(R9,*fles); A=vuist(A); A=ogen(A,oog); return A
