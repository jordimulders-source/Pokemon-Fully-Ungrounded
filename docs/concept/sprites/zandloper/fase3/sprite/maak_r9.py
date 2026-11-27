# Ronde 9 op r8: hoofd hoger op de schouders via de staart (2 rijen staart weg, lijf+armen+glas 2 px omlaag, hoofd en
# zandloper blijven staan), handen: lijnen uit het r5-model. Alleen verschuiven, weghalen, tint uit het r8-palet.
import numpy as np; from PIL import Image; import maak_r6 as m, kijk, schoon
T,ZW,S0,S1,S2,S3,S4=0,1,2,3,4,5,6
R8=np.asarray(Image.open('r8/zandloper_fase3.png')).astype(int)
LOG={}
def zet(A,p,v,k):
    if A[p]!=v: LOG.setdefault(k,[]).append((p,int(A[p]),int(v))); A[p]=v
GLAS=(7,8,9,10)
# hoofd: r5-masker, maar het glas in de borst (onder de kin) hoort bij het lijf
HOOFD=m.H.copy()
for y,x in zip(*np.where(HOOFD)):
    if R8[y,x] in GLAS: HOOFD[y,x]=False          # glas (fles bij de kin, flessenhals links) hoort bij het lijf
# zandloper: alles vanaf rij 53, plus de glazen helften naast de staart in rij 50-52
ZL=np.zeros((64,64),bool); ZL[53:]=True; ZL[50:53,:29]=True; ZL[52,33:]=True
LIJF=(R8!=T)&~HOOFD&~ZL
WEG_RIJEN=(51,52)          # staart: rechte nek "ac#" op x30-32, identiek in beide rijen
def schuif(A0):
    A=np.zeros_like(A0); A[ZL]=A0[ZL]
    for y in range(64):
        if y in WEG_RIJEN: continue
        ny=y+2 if y<WEG_RIJEN[0] else y
        for x in range(64):
            if LIJF[y,x] and ny<64 and not HOOFD[ny,x]: A[ny,x]=A0[y,x]
    A[HOOFD]=A0[HOOFD]
    return A

# vrijgekomen pixels (binnen het oude of nieuwe silhouet, nu leeg): zandtint van de modelhelderheid in lijfcoordinaten
# (kijk.model64 op (y-2,x): het lijf is 2 px omlaag geschoven, het model hoort bij het lijf), banden als r8.
BAND=[(95,S0),(135,S1),(170,S2),(200,S3),(999,S4)]
MO=np.asarray(kijk.model64()).astype(float)@[.299,.587,.114]
def gaten(A):
    """transparante pixels die niet met de rand van het beeld verbonden zijn (4-buren)"""
    buiten=np.zeros((64,64),bool); st=[(y,x) for y in range(64) for x in (0,63)]+[(y,x) for x in range(64) for y in (0,63)]
    st=[p for p in st if A[p]==T]
    for p in st: buiten[p]=True
    while st:
        y,x=st.pop()
        for dy,dx in schoon.N4:
            q=(y+dy,x+dx)
            if 0<=q[0]<64 and 0<=q[1]<64 and A[q]==T and not buiten[q]: buiten[q]=True; st.append(q)
    return [(y,x) for y,x in zip(*np.where((A==T)&~buiten))]
def vul(A):
    """Nek 2 rijen langer. Model r5: direct onder de kaak een schaduwband, daaronder borst/schouder. Dus: gatpixel direct
    onder de kin-omlijning van het hoofd = schaduwtint S1; de rest = tint van de eerste lijfpixel eronder in dezelfde kolom
    (schouder/borst loopt recht omhoog door). Alleen tintkeuze uit het palet."""
    g=[p for p in gaten(A) if p[0]<40]; G=set(g)
    for p in sorted(g):
        y,x=p
        if HOOFD[y-1,x] and A[y-1,x] in (S0,ZW): zet(A,p,S1,'nek: schaduw onder de kaak (tint)'); continue
        yy=y+1
        while (yy,x) in G: yy+=1
        v=A[yy,x] if A[yy,x] in (S1,S2,S3,S4) else S2
        zet(A,p,v,'nek/schouder: tint van het lijf eronder')
    return A
# ---------- handen: lijnen en tinten uit het r5-model, per spritepixel (modelblok 15,36 px, lijfcoordinaten y-2) ----------
_RGB=np.asarray(Image.open('../gemini/r5.webp').convert('RGB')).astype(float); _L=_RGB@[.299,.587,.114]
_SAT=_RGB.max(2)-_RGB.min(2); _X0=(0*3+2)*5.12-0.12; _Y0=(2*3+2)*5.12-0.12; _P=15.36
def modelklasse(Y,X):
    """'.' leeg, 'g' glas, '#' lijn, '+' halve lijn, anders zandband 'b'..'e' (b donker)"""
    y=Y-2; sl=(slice(int(_Y0+y*_P),int(_Y0+(y+1)*_P)),slice(int(_X0+X*_P),int(_X0+(X+1)*_P)))
    b=_L[sl]; s=_SAT[sl]
    if (b>235).mean()>.5: return '.'
    if ((s<60)&(b>=75)&(b<=235)).mean()>.4: return 'g'
    d=(b<75).mean()
    if d>.3: return '#'
    if d>.12: return '+'
    return 'bbcde'[min(4,max(0,int((b.mean()-90)/30)))]
# Per pixel uit het r5-model (modelklasse, overlay op 20x): '#'/'+' = lijn (S0, donkerste zandtint), b..e = tint.
# Linkervuist: knokkellijn diagonaal (26,17)-(27,15/16)-(28,13/14) zoals het model, licht op de bolling (28,15),(29,14-15),
# schaduw onder de bovenste boei en langs de onderkant (rij 32-33). Rechtervuist: bovenlijn rij 24 x20-23, licht (25,21-22),
# knokkellijn (29,22) blijft, de verticale tussenlijn x21 r24-25 (niet in het model) weg.
HAND={
 # linkervuist
 (26,17):S0,(27,15):S0,(28,15):S4,(27,13):S2,(29,13):S2,(29,17):S1,
 (30,12):S2,(30,18):S2,(30,19):S2,(30,21):S2,(31,14):S2,(31,15):S2,
 (32,12):S2,(32,13):S3,(32,14):S3,(33,14):S1,
 # rechtervuist
 (24,20):S0,(24,22):S0,(24,23):S0,(25,19):S0,(25,20):S3,(25,21):S4,(26,21):S2,(29,21):S2,
}
def handen(A):
    for p,v in HAND.items(): zet(A,p,v,'hand: lijn/tint uit het model')
    return A
def rand(A):
    # hoofdomlijning links: de flessenhals (glas) die hier tegen het hoofd lag is meegeschoven; het gat in de omlijning
    # tussen (10,22) en (12,21) krijgt de lijntint
    zet(A,(11,21),S0,'hoofdomlijning (tint)')
    # staart: de ingekorte nek sluit nu op rij 52 tegen de zandloper; het ingesloten gaatje (53,33) wordt omlijning
    zet(A,(53,33),ZW,'staart/zandloper: ingesloten gaatje -> omlijning')
    return A
def bouw():
    LOG.clear(); A=schuif(R8); A=handen(A); A=vul(A); A=rand(A); return A
