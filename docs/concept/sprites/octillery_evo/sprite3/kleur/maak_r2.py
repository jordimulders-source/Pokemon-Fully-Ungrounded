# maak_r2.py: maakt r2.png uit r1.png (Krassault, kleurfase r2). Gebruik (vanuit sprite3/kleur/): python3 maak_r2.py
# Elke wijziging staat als data in EDITS: "zone rij x0 tekens" ('_' = pixel laten staan), met de hand ingevuld naast het model.
# Zones: kl linkerkanon | kr rechterkanon | mo mond | tl kleine tentakels links | tr tentakels rechts | rl/rr rupsband links/rechts | lb losse lijncorrecties | kop kop-rand
# Het silhouet van r1 (= basis.png) is waarheid: een teken buiten het silhouet stopt het script. Palet ongewijzigd.
from PIL import Image; import numpy as np
CH={'K':1,'L':2,'D':3,'S':4,'B':5,'H':6,'W':7,'a':10,'b':11,'c':12}; INV={v:k for k,v in CH.items()}; INV[0]='.'
EDITS="""
# zone y x0 tekens ('_' = laten)
# --- linkerkanon (dichtbij)
kl 25 4 WHHHHH
kl 26 4 WLKKHL
kl 27 4 HKKKHL
kl 28 4 HKKKBL
kl 29 4 BKKBSL
kl 30 5 BBSL
kl 31 14 H
kl 32 15 H
kl 33 15 H
kl 34 15 H
kl 35 15 H
# --- rechterkanon (ver)
kr 25 45 BHHHHH
kr 26 45 HHSSSHH
kr 27 45 HSKKKSH
kr 28 45 HKKKKSB
kr 29 45 BKKKKBB
kr 30 45 BBKKBS
kr 31 47 BBS
kr 32 45 L
kr 33 45 L
kr 34 45 L
kr 35 45 K
kr 36 46 L
kr 37 46 L
# --- mond
mo 39 26 HHLBBL
mo 40 26 LHBLBBK
mo 41 26 HLHBLBK
mo 42 25 HHLHBLBK
mo 43 25 HHLHBLBK
mo 44 26 HHLBLSK
mo 45 28 LSLK
# --- kleine tentakels links
tl 38 8 L
tl 46 4 SSSSSSS
tl 48 8 BSSSS
tl 46 15 L
tl 47 14 LL
tl 48 16 LLL
tl 49 13 BHHHBS
tl 27 23 S
# --- tentakels rechts
tr 25 55 L
tr 26 55 L
tr 40 54 L
tr 43 54 L
tr 44 53 L
tr 40 49 B
tr 40 52 S
tr 37 50 S
tr 37 54 L
tr 43 61 L
tr 41 45 LL
# --- rupsband links
rl 50 12 L_c
rl 51 11 L_cLb__B
rl 52 10 L_BbLa_B__L___L
rl 53 11 a__a__S_L__L_____S
rl 54 16 B_LS_L____LLK
rl 55 11 b__c_B_LS_L_L____S
rl 56 11 a_cLb_B_L__L_____S
rl 57 13 bLa_S_L
rl 58 14 a_____LLLLL
rl 51 21 LLL
# --- rupsband rechts
rr 48 46 SS
rr 49 50 KK
rr 50 52 SSS
rr 51 45 LLLLLLLLLLLL
rr 52 32 BcB_____LLLLLL___________L
rr 53 32 cLb_S_LL__L________LLLL__L
rr 54 32 bLaSSL___L_L__LLLLLL_____L
rr 55 33 a_S_L__L___LLL________LL
rr 56 30 b__B_S_L__L_L________LLLL
rr 57 30 bBBcBS_L_________LLLLL
rr 58 32 cLbS__L____LLLLL
rr 59 32 bLa____LLLL
rr 60 33 a
# rolvulling: licht boven binnen de ovaal
rr 52 46 BBBBBBBBBBB
rr 53 40 BB_BBBBBBBB____BB
rr 54 38 BBB_B_BB
rl 52 21 BBB
rl 53 20 BB_BB
rl 54 19 BB_BBBB
# --- belijning (losse correcties)
lb 24 21 L
lb 45 40 LLL
lb 31 21 S
# --- kop-rand (lijnregel; zie LOG)
kop 29 23 L
kop 30 22 L
kop 34 43 L
kop 35 43 L
# ovaal: onderboog zwart (schaduwkant), bovenboog lijnrood (lichtkant)
rr 55 55 KK
rr 56 51 KKKK
rr 57 47 KKKKK
rr 58 43 KKKKK
rr 59 39 KKKK
rl 58 20 KKKKK
"""
im=Image.open('r1.png'); a=np.array(im); b=a.copy(); zone={}
for ln in EDITS.splitlines():
    ln=ln.split('#')[0].split()
    if len(ln)!=4: continue
    z,y,x0,s=ln[0],int(ln[1]),int(ln[2]),ln[3]
    for i,c in enumerate(s):
        if c=='_': continue
        assert a[y,x0+i]>0,('buiten het silhouet',z,x0+i,y)
        b[y,x0+i]=CH[c]; zone[(x0+i,y)]=z
assert ((a>0)==(b>0)).all()
out=Image.fromarray(b,'P'); out.putpalette(im.getpalette()); out.save('r2.png',transparency=0)
with open('raster_r2.txt','w') as f:
    print('    '+''.join(str(x//10) for x in range(64)),file=f); print('    '+''.join(str(x%10) for x in range(64)),file=f)
    for y in range(64): print('%2d  %s'%(y,''.join(INV[v] for v in b[y])),file=f)
# verslag
cnt={}
for (x,y),z in zone.items():
    if a[y,x]!=b[y,x]: cnt[z]=cnt.get(z,0)+1
print('gewijzigde pixels t.o.v. r1:',int((a!=b).sum()),'| per zone:',dict(sorted(cnt.items())))
# kop (bevroren): mantel/vin rij 5-20; kopkoepel + ogen: rij 21-24 x26-50, rij 25-30 x24-44, rij 31-33 x22-44, rij 34-38 x21-44
def kop(x,y): return y<=20 or (y<=24 and 26<=x<=50) or (25<=y<=30 and 24<=x<=44) or (31<=y<=33 and 22<=x<=44) or (34<=y<=38 and 21<=x<=44)
kd=[(x,y,INV[a[y,x]]+'>'+INV[b[y,x]]) for y in range(64) for x in range(64) if a[y,x]!=b[y,x] and kop(x,y)]
print('kop-diff:',len(kd),kd)
la=np.isin(a,[1,2]); lb=np.isin(b,[1,2]); ya=a>=10; yb=b>=10
print('lijn erbij:',int((lb&~la).sum()),'lijn weg:',int((la&~lb).sum()),'| K>L:',int(((a==1)&(b==2)).sum()),'L>K:',int(((a==2)&(b==1)).sum()),'| geel erbij:',int((yb&~ya).sum()),'geel weg:',int((ya&~yb).sum()))
