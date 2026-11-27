# r2 stap 1: staart van r5 (vorm, aantal, breedte) op dezelfde schaal (kopmaat r7/r5 gemeten: breedte 140/145, hoogte 211/215 -> 0,98)
# achter de klauwen van r7, kleuren van de r7-staart (goud in de r5-goudtint, donkere punten i.p.v. de witte r5-punten).
# Samenstelling in r7-origineelcoordinaten, daarna dezelfde verkleining als de rest (gereedschap/reduceer.py).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from reduceer import *
r7=np.asarray(Image.open('../gemini/r7.png').convert('RGB')); r5=np.asarray(Image.open('../gemini/r5.png').convert('RGB'))
F=0.98; A5=np.array([725,525]); A7=np.array([522,728])
VOET5=[(550,512,676,600),(686,510,806,606)]          # x0,y0,x1,y1 voeten r5 (vallen weg; r7-klauwen komen ervoor)
# --- r5-staartlaag: alle r5-figuurpixels met y >= 525 tussen x 540-980, zonder de voeten; voetgaten = pixel recht eronder
sys.path.insert(0,'gereedschap'); from klassen import klassen
_,c5,L5=klassen('../gemini/r5.png')        # achtergrond via floodfill vanaf de rand (witte punten blijven figuur)
st=np.zeros(r5.shape[:2],bool); st[525:,540:980]=c5[525:,540:980]>0
st[470:525,790:980]=c5[470:525,790:980]>0     # rechter staartveren komen al hoger onder het lijf vandaan
gat=np.zeros_like(st)
for x0,y0,x1,y1 in VOET5: st[y0:y1,x0:x1]=False; gat[y0:y1,x0:x1]=True
r5v=r5.copy()
for x0,y0,x1,y1 in VOET5:
    for x in range(x0,x1):
        if c5[y1+2,x]>0:
            for y in range(y0,y1): r5v[y,x]=r5[y1+2+((y-y0)%6),x] if c5[y1+2+((y-y0)%6),x]>0 else r5[y1+2,x]
            st[y0:y1,x]=True
# witte punten van r5 -> donkere punt (kleur r7-punt (54,49,59)); lijnen blijven
wit=st&(c5==5); r5v[wit]=(54,49,59)
# naar r7-coordinaten
H=1024; laag=np.zeros((H,H,4),'uint8')
yy,xx=np.mgrid[0:H,0:H]; sx=np.round(A5[0]+(xx-A7[0])/F).astype(int); sy=np.round(A5[1]+(yy-A7[1])/F).astype(int)
ok=(sx>=0)&(sy>=0)&(sx<r5.shape[1])&(sy<r5.shape[0]); m=np.zeros((H,H),bool); m[ok]=st[sy[ok],sx[ok]]
laag[m,:3]=r5v[sy[m],sx[m]]; laag[m,3]=255
# r7 ervoor: alles boven de staartwortel (natief v<108) en de voeten van r7
_,c7,L7=klassen('../gemini/r7.png'); v=(yy-0.1)/6.4; u=(xx-0.1)/6.4
voor=(c7>0)&((v<108)|((u>=53)&(u<=74)&(v<=122))|((u>=76)&(u<=93)&(v<=121)))
# alleen de onderkant telt; r7-staart buiten de voetvakken valt weg
laag[voor,:3]=r7[voor]; laag[voor,3]=255
Image.fromarray(laag).save('samenstelling_onder.png')
c,L=klas(laag[...,:3],laag[...,3])
BG=float(sys.argv[1]) if len(sys.argv)>1 else 0.35; DG=float(sys.argv[2]) if len(sys.argv)>2 else 0.25; TP=float(sys.argv[3]) if len(sys.argv)>3 else 0.45
o,fr=reduceer(c,L,BG=BG,TP=TP,DG=DG,LMIN=0.25,box=(0,40,64,64))
np.save('onder_kaal.npy',o); print('onder: figuurpx',(o>0).sum())
# klauwen: in de voetvakken van r7 wint de roomwitte klauw vanaf 22 % (anders vallen ze weg tussen de goudlijnen)
VOETEN=[(19,45,28,49),(28,44,38,48)]
nk=0
for x0,y0,x1,y1 in VOETEN:
    for Y in range(y0,y1):
        for X in range(x0,x1):
            f=fr[Y,X]
            if f[5]>=0.28 and o[Y,X] not in (0,7):
                o[Y,X]=7 if f[5]>=0.4 else 14; nk+=1
np.save('onder_kaal.npy',o); print('klauwpixels',nk)
