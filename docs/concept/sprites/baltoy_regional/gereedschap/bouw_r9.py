# r9 = r8 met alleen een nieuw reliëf op het VOORVLAK VAN HET LIJF (klassen-x 12..19, y 20..28; png x 27..34, y 47..55).
# Basis van het vlak = r8-verloop zonder het oude reliëf (oude groeven 'd' -> vlaktint volgens vlak() uit bouw_r8).
# Reliëf: alle tinten zijn een verschuiving op de vlaktint, dus lijnen wisselen mee met het verloop (licht links, donker rechtsonder).
# Licht linksboven, consequent: verhoogd = lichter met lichtste bovenrand, slagschaduw rechts/onder; groef = donker met lichtrand rechts/onder.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import lees, op, rgba
import numpy as np; from PIL import Image
g=lees('gereedschap/baltoy_r6_klassen.txt')
r8=np.array(Image.open('sprite_r8/baltoy_r8.png')); PAL=Image.open('sprite_r8/baltoy_r8.png').getpalette()
OY,OX=27,15; Y0,Y1,X0,X1=20,28,12,19
def v(y,x): return 0.8+(x-11)/8*2.3+(y-20)/8*1.5+max(0,(x-15)/4+(y-24)/4-0.6)*1.2   # = vlak() lijf uit bouw_r8
def base(y,x):
    if g[y][x] in 'lM': return int(r8[y+OY,x+OX])-1
    return int(round(v(y,x)))
# maskers 8 breed (x12..19) x 9 hoog (y20..28)
# verschuiving op de vlaktint: a -2, b -1 (verhoogd/licht, bovenranden lichtst) | n 0 | c +1, d +2 (weggehakt veld) | e +3 (groef/slagschaduw) | f +4
# (X/g/'.' = automatische variant, in r9 alleen gebruikt in B: g groef, '.' krijgt lichtrand rechts/onder van een groef)
M={
'A':[  # Ponce/Bennett: linkerhand met kero (rechte beker), rechterhand met staf, in reliëf voor de borst; gordel eronder
 "dabdddad",
 "dbnedcbe",
 "dbnedcbe",
 "aaaaedbe",
 "bbbbeaaa",
 "eeeedbbb",
 "ddddeebe",
 "bbbbbbbb",
 "nnnnnnnn"],
'B':[  # brede gordel met getrapt motief (lichte trappiramide tussen ingehouwen treden), erboven en eronder verticale kledingbanen
 "..g..g..",
 "..g..g..",
 "gggggggg",
 "eee..eee",
 "ee....ee",
 "e......e",
 "gggggggg",
 "........",
 "..g..g.."],
'C':[  # groot getrapt kruis (chakana) met gat in het midden, als ingehouwen paneel: kruis blijft staan, hoeken getrapt weggehakt
 "eeebbeee",
 "eeebneee",
 "eebnnnee",
 "bbnnnnnn",
 "bnneennn",
 "nnnnnnnn",
 "eebnnnee",
 "eeebneee",
 "eeebneee"],
}
OFF={'n':0,'a':-2,'b':-1,'.':0,'c':1,'d':2,'e':3,'f':4,'g':3}
def off(m,j,i):
    at=lambda jj,ii: m[jj][ii] if 0<=jj<len(m) and 0<=ii<len(m[0]) else '.'
    c=m[j][i]
    if c=='X': return -2 if at(j-1,i)!='X' else -1
    if c!='.': return OFF[c]
    if at(j-1,i)=='X' or at(j,i-1)=='X': return 3
    if at(j-1,i-1)=='X': return 2
    if at(j-1,i)=='g' or at(j,i-1)=='g': return -1
    return 0
def bouw(k):
    a=r8.copy(); m=M[k]
    for j,row in enumerate(m):
        for i,c in enumerate(row):
            y,x=Y0+j,X0+i
            a[y+OY,x+OX]=1+max(0,min(8,base(y,x)+off(m,j,i)))
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
