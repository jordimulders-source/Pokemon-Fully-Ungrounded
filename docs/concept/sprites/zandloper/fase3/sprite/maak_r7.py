# Ronde 7 op r6-W1-basis (r5 + maak_r6): ogen uit het r8-model, brein met middengroef, linkerarm + boeien naar het model.
# Alleen per pixel: verschuiven, weghalen, tint uit het r5-palet. Elke wijziging komt in LOG (via maak_r6.zet).
import numpy as np; from PIL import Image; import maak_r6 as m, schoon
T,ZW,S0,S1,S2,S3,S4,WIT=0,1,2,3,4,5,6,14
CH={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5,'e':6,'f':7,'g':8,'h':9,'i':10,'m':14}
zet=m.zet
# ---------- brein: middengroef (r8 comp B, doorgetrokken van achter bij de kuif tot voor op het voorhoofd),
# links r8 comp A, rechts r8 comp C (spiraal) en D ----------
m.WIND['B']=[(7,29),(8,28),(9,28),(10,27),(11,27),(12,26),(13,26)]
def brein(A): return m.brein(A,'ABCD')
# ---------- ogen: r8-model, oogzone verkleind met factor 8 (modelpixels per spritepixel), materiaalregel als hoofd.oog_r8:
# W = oogwit, # = pupil, a = ooglid (S0). Rooster x412+8i, y272+8j van gemini/r8.png (fase 0,0).
OOG_L=[(1,1,'a'),(2,1,'a'),(2,2,'W'),(2,3,'a'),(3,2,'W'),(3,3,'#'),(3,4,'#'),(4,3,'W'),(4,4,'#')]
OOG_R=[(0,13,'a'),(0,14,'a'),(1,11,'a'),(1,12,'a'),(1,14,'a'),(2,9,'a'),(2,10,'a'),(2,11,'W'),(2,12,'W'),(2,13,'W'),(2,14,'a'),
       (3,9,'a'),(3,10,'W'),(3,11,'#'),(3,12,'W'),(3,13,'W'),(4,10,'W'),(4,11,'#'),(4,12,'W'),(4,13,'W')]
def oog_r8(A):
    for p in [(y,x) for y in range(14,21) for x in range(20,35)]:
        if A[p] in (WIT,ZW) and m.binnen(p): zet(A,p,S3,'r5-oog weg')
    for p in m.BROW_R5:
        if A[p]==S0: zet(A,p,S3,'r5-wenkbrauw weg (ooglid uit r8 komt ervoor)')
    gez=[]
    for pix,(ty,tx) in ((OOG_L,(17.5,24.0)),(OOG_R,(17.5,30.5))):
        w=[(r,c) for r,c,k in pix if k in 'W#']; cy=np.mean([r for r,c in w]); cx=np.mean([c for r,c in w])
        dy=int(round(ty-cy)); dx=int(round(tx-cx))
        for r,c,k in pix:
            p=(r+dy,c+dx); zet(A,p,{'W':WIT,'#':ZW,'a':S0}[k],'oog r8 (f8)'); gez.append(p)
    g=set(gez)
    for p in gez:
        if A[p] not in (WIT,ZW): continue
        for dy,dx in schoon.N4:
            q=(p[0]+dy,p[1]+dx)
            if q not in g and A[q] in (S1,S2) and m.binnen(q): zet(A,q,S3,'oog vrij (tint)')
    return A
# ---------- linkerarm, kleine boeien, hand: per rij overgenomen van het r5-model op 1:1 (kijk.model64, zelfde raster
# als het lijf), buitenrand op Jordi's krabbel (boog x15 -> x12). Kolommen x9..22; '_' = laat staan. ----------
ARM={ # rij: (eerste x, tekens)
 16:(14,'.adddcc'),
 17:(15,'adedd'),
 18:(14,'adeedd'),
 19:(14,'adeddd'+'d'),
 20:(14,'adddddd'),
 21:(13,'adcccddd'),
 22:(13,'adddddddda'),
 23:(13,'adeddddda'),
 24:(12,'addcccaad'),
 25:(12,'adccafffff'),
 26:(12,'aaaacfiihf'),
 27:(12,'addcccfffc'),
 28:(12,'adedcddedd'),
 29:(11,'adeedfffff'),
 30:(11,'adedfiihhgf'),
 31:(12,'#dcfihhggf'),
 32:(13,'##fhgggf#'),
}
def arm(A):
    for y,(x0,s) in ARM.items():
        for i,c in enumerate(s): zet(A,(y,x0+i),CH[c],'arm/boei/hand naar model')
    return A
def bouw():
    m.LOG.clear(); A=m.R5.copy()
    A=brein(A); A=m.gezicht(A); A=oog_r8(A); A=m.selout_links(A); A=arm(A)
    return A,dict(m.LOG)
