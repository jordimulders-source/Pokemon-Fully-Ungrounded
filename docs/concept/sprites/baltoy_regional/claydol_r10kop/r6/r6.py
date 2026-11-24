# Ronde 6 (basis r5): lijf opnieuw als één ronde vorm (één lichtbron linksboven, gebogen tintgrenzen), onderlijf vanuit r3-logica
# (onderkant van een bol in schaduw), haken terug naar 9, neus: een paar pixels. Kop/krans/staven/ogen/rode lijn diff 0.
# Werkwijze: schets.py gaf een SCHETS (bolnormaal -> harde drempels, één palettint per pixel); daarna met de hand
# bijgewerkt (HAND hieronder) en als tekstraster vastgelegd in LIJF_A.
import os,sys,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
for p in ('..','../r2','../r3','../r5'): sys.path.insert(0,os.path.join(H,p))
from r2 import LIJF, KIN
from schets import schets, VAST6
yy,xx=np.mgrid[0:64,0:64]
R5=np.array(Image.open(os.path.join(H,'../r5/claydol_r10kop_r5.png'))).astype(int)
PAL=Image.open(os.path.join(H,'../r5/claydol_r10kop_r5.png')).getpalette()
LZ=LIJF&(yy>=40)
HAND={  # (x,y): tint  -- handwerk na de schets
 # hals: slagschaduw van de kop, cilinder 5 -> A met schuine grens; schouderrand rechts in schaduw
 **{(x,40):5 for x in range(24,32)}, **{(x,40):10 for x in range(32,39)}, (22,40):5, (40,40):10, (41,40):10,
 **{(x,41):5 for x in range(24,31)}, **{(x,41):10 for x in range(31,39)}, (21,41):5, (22,41):5, (40,41):10,
 **{(x,42):5 for x in range(23,30)}, **{(x,42):10 for x in range(30,40)}, (19,42):5, (20,42):5, (21,42):5, (41,42):5, (42,42):5, (43,42):5,
 # rechterarm: bovenrand onder de kop 5, lichtkap 3 alleen op de bovenkant (rij 44-45), verder 5 -> A
 **{(x,43):5 for x in range(41,46)}, (41,45):3, (45,45):5, **{(x,46):5 for x in range(40,44)}, (40,47):5, (41,47):5,
 # rechterhand: eigen kap (5) linksboven tegen de plooi, rest A
 (48,47):5, (49,47):10, (47,48):5, (48,48):5, (49,48):10, (47,49):5, (48,49):10, (46,50):10, (47,50):10, (48,50):10,
 # linkerarm: geen lichte kleur op de buitenrand (selout 5 aan de lichtkant)
 (18,43):5, (16,44):5, (17,44):5, (15,45):5,
 # romp onderkant: licht loopt links door (bol), rechts schaduw
 (27,54):5, (28,54):5, (29,54):5, (21,51):6, (40,44):5, (18,49):10, (25,51):5, (42,52):6, (21,52):6, (22,54):6,
 # voeten: gebogen sikkels i.p.v. bovenstrook
 (23,55):5, **{(x,55):5 for x in range(24,28)}, (28,55):10, (29,55):10, (30,55):10,
 **{(x,55):5 for x in range(31,37)}, **{(x,55):10 for x in range(37,43)}, (43,55):6,
 **{(x,56):5 for x in range(31,35)}, **{(x,56):10 for x in range(35,42)}, (42,56):6, (43,56):6,
 **{(x,57):10 for x in range(33,40)}, **{(x,57):6 for x in range(40,43)},
 **{(x,58):10 for x in range(33,37)}, **{(x,58):6 for x in range(37,41)},
 (34,59):10, (35,59):10, **{(x,59):6 for x in range(36,40)},
}
def bouw_lijf_schets(S):
    T,_=schets(False)
    S[LZ]=T[LZ]
    for (x,y),v in HAND.items():
        assert LZ[y,x] and R5[y,x] not in (7,8,9),(x,y)
        S[y,x]=v
    return S
# tekstraster lijf (x 13-51); bevroren na schets + handwerk (HAND) + spikkelreparaties FIX
LIJF_A={
40:'.........5755555555AAAAAAA6AA7.........',
41:'........5575555555AAAAAAAA6A777........',
42:'......55565555555AAAAAAAAAA65557.......',
43:'.....526622222222222233335565555577....',
44:'...552236666222222226663355563333357...',
45:'..52222362262222226263335556333355557..',
46:'..222335622666222266633355655553555AA7.',
47:'..2236356222222223633335556553355565A7.',
48:'..733365799922233333335559A733555655A7.',
49:'...7AAA672229333333399999AAA7655565A7..',
50:'....7A777933933333395555A9AAA67A6AAA7..',
51:'.....7..63933933355955966AAAA677AAA7...',
52:'........63393935555959AAAAAA667.777....',
53:'........73393955555959AAAA66667........',
54:'.........666665555A959AAAA66667........',
55:'7........755555AAA555555AAAAAA67......6',
56:'7.........755555665555AAAAAAA667......6',
57:'57.........775AAA677AAAAAAA6667......53',
58:'7............77777.7AAAA666677.......53',
59:'....................7AA66667........535',
60:'.....................777777........5355',
}
FIX={(20,46):5, (42, 44): 3, (32, 45): 2, (17, 49): 10, (19, 49): 10, (25, 51): 3, (25, 53): 3, (33, 53): 5, (33, 54): 5, (24, 56): 5}
def bouw_lijf(S):
    for y,r in LIJF_A.items():
        for i,c in enumerate(r):
            x=13+i
            if LZ[y,x]: S[y,x]=int(c,16)
    return S
def reflectie(S):
    """variant B: 1 px reflectierand boven de onderste omlijning (rechts/onder): 6 -> A, A -> 5"""
    for y,x in zip(*np.where(LZ&(xx>=31)&(yy>=50))):
        if (x,y) in VAST6: continue
        if R5[y+1,x]==7 and S[y,x] in (6,10): S[y,x]={6:10,10:5}[S[y,x]]
    return S
NEUS={(27,32):3}   # rechteronderkant: hoek (2 px 66 op rij 32) weg, rand stapt nu 1 px per rij zoals links
def bouw(var='A'):
    S=R5.copy(); bouw_lijf(S)
    if var=='B': reflectie(S)
    for (x,y),v in NEUS.items(): S[y,x]=v
    return S
def check(S):
    assert ((S>0)==(R5>0)).all(),'silhouet'
    nz=np.zeros((64,64),bool)
    for (x,y) in NEUS: nz[y,x]=True
    assert not ((S!=R5)&~LZ&~nz).any(),'buiten lijf/neus'
    assert ((S==7)==(R5==7))[LZ].all(),'omlijning'
    assert ((np.isin(S,(8,9)))==(np.isin(R5,(8,9))))[LZ].all() and not (S[LZ]==8).any(),'haken'
    assert all(S[y,x]==6 for x,y in VAST6),'trapjes/plooien/naden'
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    for v in 'AB':
        S=bouw(v); check(S); save(S,os.path.join(H,'proef_'+v))
        print(v,'lijf px t.o.v. r5',int(((S!=R5)&LZ).sum()))

def lever():
    for v,naam in (('A','claydol_r10kop_r6'),('B','claydol_r10kop_r6_B_reflectie')):
        S=bouw(v); check(S); save(S,os.path.join(H,naam))
        d=S!=R5
        print(naam,': t.o.v. r5 totaal',int(d.sum()),'| lijf',int((d&LZ).sum()),'| neus',int(sum(d[y,x] for x,y in NEUS)),'| elders',int((d&~LZ).sum())-int(sum(d[y,x] for x,y in NEUS)))
