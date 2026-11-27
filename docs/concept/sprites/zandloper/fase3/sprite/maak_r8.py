# Ronde 8 op r7: strakke boog linkerarm, handen op modelhelderheid, hoofd-omhoog-varianten, losse pixels.
import numpy as np; import maak_r7 as m7, maak_r6 as m, kijk, schoon
T,ZW,S0,S1,S2,S3,S4=0,1,2,3,4,5,6
zet=m.zet
# 1 linkerarm: buitenrand x15(2) x14(2) x13(3) x12(4) x11(4), binnentinten verschoven met de rand mee
m7.ARM.update({
 16:(14,'.adddcc'),
 17:(14,'.adedd'),
 18:(14,'adeedd'),
 19:(14,'adeeddd'),
 20:(13,'addeddd'),
 21:(13,'adcccddd'),
 22:(13,'adcddddd'),
 23:(12,'addeddddda'),
 24:(12,'addcccaad'),
 25:(12,'adccafffff'),
 26:(11,'.aaaacfiihf'),
 27:(11,'adddcccfffc'),
 28:(11,'addedcddedd'),
})
# 2 handen: zandpixels in de handzone krijgen de band van de modelhelderheid (kijk.model64, zelfde raster als het lijf);
#   heel donker = binnenlijn (S0). Glas, zwart en transparant blijven.
BAND=[(95,S0),(135,S1),(170,S2),(200,S3),(999,S4)]
HAND=[(y,x) for y in range(27,33) for x in range(13,26)]+[(y,x) for y in range(22,27) for x in range(20,23)]
def handen(A):
    M=np.asarray(kijk.model64()).astype(float)@[.299,.587,.114]
    for p in HAND:
        if not (3<=A[p]<=6): continue                                       # lijnen (S0) blijven
        if any(A[p[0]+dy,p[1]+dx]==T for dy,dx in schoon.N4): continue      # buitenrand blijft
        v=next(t for g,t in BAND if M[p]<g); zet(A,p,v,'hand: modelhelderheid (tint)')
    return m.vlekjes(A,(27,16,33,25))
def basis():
    m.LOG.clear(); A=m.R5.copy()
    A=m7.brein(A); A=m.gezicht(A); A=m7.oog_r8(A); A=m.selout_links(A); A=m7.arm(A)
    zet(A,(16,13),T,'rand') if A[16,13] else None
    A=handen(A); return A
# 3 hoofd omhoog (alleen verschuiven): hoofd (masker H uit r5) n px omhoog; bovenste kuifrijen vallen weg; onder het hoofd
#   schuift de onderliggende rij (nek/schouder/boei) mee omhoog.
def omhoog(A,n):
    """Hoofd (masker H uit r5) n px omhoog; bovenste kuifrijen vallen weg. Vrijgekomen pixels (oud hoofd, niet meer
    bedekt) krijgen de zandtint van de gemeten modelhelderheid (nek/schouder, kijk.model64); glas eronder schuift niet mee."""
    H=m.H; B=A.copy(); Mo=np.asarray(kijk.model64()).astype(float)@[.299,.587,.114]
    Hn=np.zeros_like(H); Hn[:64-n]=H[n:]
    for y in range(64):
        for x in range(64):
            if Hn[y,x] and not 7<=A[y+n,x]<=10: B[y,x]=A[y+n,x]
            elif H[y,x] or Hn[y,x]:
                B[y,x]=T if y<12 else next(t for g,t in BAND[1:] if Mo[y,x]<g)   # boven: leeg; onder het hoofd: nek/schouder
    # kuif: de nieuwe bovenkant (open na het weghalen van de bovenste rijen) krijgt de selout-lijntint
    for y in range(0,22):
        for x in range(1,63):
            if Hn[y,x] and 3<=B[y,x]<=6 and (y==0 or T in (B[y-1,x],B[y,x-1],B[y,x+1])): B[y,x]=S0   # open rand -> selout
    return B
