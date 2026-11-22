# r10 = r8 met een nieuw reliëf op het lijf IN DRIEKWART: voorvlak (klassen x11..19), ribbe x20, zijvlak x21..23; rijen 20..28.
# Centraal motief gecentreerd op het voorvlak (midden x15) en verkort in de breedte (7 i.p.v. 9 px);
# gordels/groeven lopen over de ribbe door op het zijvlak, verkort en in de schaduwtinten van het zijvlak (zoals de hoofdband op de kop).
# Alle tinten = verschuiving op de vlaktint (lijntint wisselt mee met het verloop); licht linksboven; silhouet/zwart ongewijzigd.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import lees, op, rgba
import numpy as np; from PIL import Image
g=lees('gereedschap/baltoy_r6_klassen.txt')
r8=np.array(Image.open('sprite_r8/baltoy_r8.png')); PAL=Image.open('sprite_r8/baltoy_r8.png').getpalette()
OY,OX=27,15; Y0,X0=20,11
def v(y,x): return 0.8+(x-11)/8*2.3+(y-20)/8*1.5+max(0,(x-15)/4+(y-24)/4-0.6)*1.2   # vlak() lijf uit bouw_r8
def base(y,x):
    if x>=20 or g[y][x] in 'lM' or x==11: return int(r8[y+OY,x+OX])-1      # ribbe/zijvlak/rand: r8-tint
    return int(round(v(y,x)))                                              # oude groef -> vlaktint
OFF={'n':0,'a':-2,'b':-1,'c':1,'d':2,'e':3}
# 13 tekens per rij: x11..19 voorvlak | x20 ribbe | x21..23 zijvlak ; '#' = r8 blijft
M={
'A':[  # Ponce/Bennett: hand met kero (links) en hand met staf (rechts) gecentreerd op het voorvlak; gordel loopt om de hoek
 "nabeddaen"+"#"+"###",
 "nbneddben"+"#"+"###",
 "nbneddben"+"#"+"###",
 "naaaaeben"+"#"+"###",
 "nbbbbaaac"+"#"+"###",
 "#eeeebbbe"+"#"+"###",
 "#ddddebcn"+"n"+"dd#",
 "#aaaaaaaa"+"b"+"bb#",
 "#nnnnnnnn"+"#"+"nn#"],
'B':[  # brede gordel met getrapt motief (trappiramide gecentreerd op het voorvlak), om de hoek doorlopend op het zijvlak; kledingbanen
 "nnebnnebn"+"#"+"###",
 "nnebnnebn"+"#"+"###",
 "eeeeeeeee"+"n"+"dd#",
 "eeebbbeee"+"b"+"nnd",
 "eebnnnbee"+"n"+"ndn",
 "#bnnnnnbe"+"n"+"dn#",
 "#eeeeeeee"+"n"+"dd#",
 "#bbbbbbbb"+"#"+"bb#",
 "#nebnnebn"+"#"+"##"+"#"],
'C':[  # getrapt kruis (chakana) met gat, gecentreerd op het voorvlak, 7 breed (verkort), hoeken weggehakt
 "neebbbeen"+"#"+"###",
 "neebnneen"+"#"+"###",
 "nebnnnben"+"#"+"###",
 "nbnnnnnbn"+"#"+"###",
 "nnnnennnn"+"#"+"###",
 "#nnnnnnnn"+"#"+"###",
 "#ennnnnen"+"#"+"###",
 "#eennneen"+"#"+"###",
 "#eennneen"+"#"+"###"],
}
def bouw(k):
    a=r8.copy()
    for j,row in enumerate(M[k]):
        assert len(row)==13,(k,j)
        for i,c in enumerate(row):
            if c=='#': continue
            y,x=Y0+j,X0+i
            if r8[y+OY,x+OX]==0 or g[y][x] in 'K.': continue           # silhouet en zwarte lijnen blijven
            a[y+OY,x+OX]=1+max(0,min(8,base(y,x)+OFF[c]))
    return a
if __name__=='__main__':
    for k in sys.argv[1:] or 'ABC':
        p=f'sprite_r10/baltoy_r10{k}.png'; im=Image.fromarray(bouw(k),'P'); im.putpalette(PAL); im.save(p,transparency=0)
        op(rgba(Image.open(p)),(255,255,255,255),8).save(f'sprite_r10/baltoy_r10{k}_8x.png')
        a=np.array(Image.open(p)); m=a!=r8; ys,xs=np.nonzero(m)
        print(k,'gewijzigd',m.sum(),'buiten zone',int(m.sum()-m[47:56,26:39].sum()),'kleuren',len(np.unique(a))-1)
