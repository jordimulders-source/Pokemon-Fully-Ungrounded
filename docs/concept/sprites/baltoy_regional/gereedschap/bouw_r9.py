# r9 = r8 met alleen een nieuw reliëf op het VOORVLAK VAN HET LIJF (klassen-x 12..19, y 20..28; png x 27..34, y 47..55).
# Basis van het vlak = r8-verloop zonder het oude reliëf (oude groeven 'd' -> vlaktint volgens vlak() uit bouw_r8).
# Reliëf: groef = vlaktint+3 (wisselt dus mee met het verloop), lichtrand = vlaktint-1/-2 onder/rechts van de groef.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import lees, op, rgba
import numpy as np; from PIL import Image, ImageDraw
g=lees('gereedschap/baltoy_r6_klassen.txt')
r8=np.array(Image.open('sprite_r8/baltoy_r8.png')); PAL=Image.open('sprite_r8/baltoy_r8.png').getpalette()
OY,OX=27,15; Y0,Y1,X0,X1=20,28,12,19
def v(y,x): return 0.8+(x-11)/8*2.3+(y-20)/8*1.5+max(0,(x-15)/4+(y-24)/4-0.6)*1.2
def base(y,x):
    if g[y][x] in 'lM': return int(r8[y+OY,x+OX])-1
    return int(round(v(y,x)))
# maskers 8 breed (x12..19) x 9 hoog (y20..28)
# . vlak | g groef (+3) | G diepe groef (+4) | s schaduw (+2) | m (+1) | h licht (-1) | H hooglicht (-2)
M={
'A':[  # Ponce/Bennett: hand met kero (links) en hand met staf (rechts) voor de borst, gordel eronder
 "Hh...h..",
 "hgm..hg.",
 "hgm..hg.",
 "gggg.hg.",
 "hhhg.ggg",
 "....hhhg",
 "......g.",
 "gggggggg",
 "hhhhhhhh"],
'B':[  # gordel met getrapt motief, erboven en eronder verticale kledingbanen
 "..g..g..",
 "..g..g..",
 "..g..g..",
 "gggggggg",
 "hg.hhg.h",
 "hgg.hgg.",
 "gggggggg",
 "hhhhhhhh",
 "..g..g.."],
'C':[  # groot getrapt kruis (chakana) als ingehouwen paneel
 "..gggg..",
 "..ghhg..",
 "gggssggg",
 "ghs..shg",
 "ghs..shg",
 "gggssggg",
 "..ghhg..",
 "..gggg..",
 "........"],
}
D={'.':0,'g':3,'G':4,'s':2,'m':1,'h':-1,'H':-2}
def bouw(k):
    a=r8.copy()
    for j,row in enumerate(M[k]):
        for i,c in enumerate(row):
            y,x=Y0+j,X0+i; b=base(y,x)
            a[y+OY,x+OX]=1+max(0,min(8,b+D[c]))
    return a
def sla(a,naam):
    im=Image.fromarray(a,'P'); im.putpalette(PAL); im.save(naam,transparency=0); return Image.open(naam)
if __name__=='__main__':
    for k in sys.argv[1:] or 'ABC':
        p=f'sprite_r9/baltoy_r9{k}.png'; sla(bouw(k),p)
        op(rgba(Image.open(p)),(255,255,255,255),8).save(f'sprite_r9/baltoy_r9{k}_8x.png')
        d=(np.array(Image.open(p))!=r8); ys,xs=np.nonzero(d)
        buiten=[(y,x) for y,x in zip(ys,xs) if not(Y0+OY<=y<=Y1+OY and X0+OX<=x<=X1+OX)]
        print(k,'gewijzigd',len(ys),'buiten zone',len(buiten),'kleuren',len(np.unique(np.array(Image.open(p))))-1)
