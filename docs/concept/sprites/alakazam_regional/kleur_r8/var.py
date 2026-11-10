# var.py: varianten als volledige rijen in een box. L* = linkerhand (x3..20), R* = rechterhand (x46..59), P* = pupil
import pal
BL=3; BR=46
B=pal.load('basis_r7.txt')
def box(x0,x1,y0,y1): return {y:B[y][x0:x1+1] for y in range(y0,y1+1)}
V={}
# ---- pupil (x28..43)
V['P1']=(28,{16:"bbbbbooobcbbbo..",17:"bbbbwowwocbboo.."})
V['P2']=(28,{16:"bbbbowoobcbbbo..",17:"bbbbowwwocbboo.."})

def rows(x0,y0,txt):
    L=[l.split('|')[1] for l in txt.strip('\n').split('\n')]
    return (x0,{y0+i:l for i,l in enumerate(L)})
# linkerhand: x3..20, rij 37..45 (huidig r7 ter vergelijking)
L0="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowobcbcbocccc|
40|...owwwobdbcbcoooo|
41|....owwobdbdbcccco|
42|.....owwoobdbcccoo|
43|......oooobdbcco.o|
44|..........obboo..o|
45|...........oo...oo|
"""
LA="""
37|.dwwwwwwo.occccccc|
38|.dwwwowwoooooccccc|
39|..owoowoaabbcocccc|
40|...owwwobbbcccoooo|
41|....owwwoddbbcccco|
42|.....owoabbccccdoo|
43|......oobbcdccdo.o|
44|..........obcco..o|
45|...........oo...oo|
"""
LB="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoaboabocccc|
40|...owwwobcobcooooo|
41|....owwobcobcoabco|
42|.....owwooobcobcoo|
43|......ooooobcoco.o|
44|..........obcoo..o|
45|...........oo...oo|
"""
LC="""
37|.dwwwwwwo.occccccc|
38|.dwwwowwoooooccccc|
39|..owoowoaabbcocccc|
40|...owwwoobbcccoooo|
41|....owwwwwobbcccco|
42|.....owooobbcccdoo|
43|......oooobbccdo.o|
44|..........obcco..o|
45|...........oo...oo|
"""
R0="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....obdwwaoo..|
29|...obbdwaaoo..|
30|...obbooooo...|
31|.oobbcbbbo....|
32|obobbcccddo...|
33|abobbcbbbbo...|
34|bbobbccddo....|
35|ccoccbboo.....|
36|cccoooo.......|
37|cccoo.........|
"""
for k in ['LA','LB','LC']: V[k]=rows(BL,37,globals()[k])
V['L0']=rows(BL,37,L0); V['R0']=rows(BR,26,R0)
def build(keys,base=None):
    R=[list(r) for r in (base or B)]
    for k in keys:
        x0,rw=V[k]
        for y,s in rw.items():
            assert len(s)==len(rw[min(rw)]) or True
            for i,c in enumerate(s):
                if c=='=': continue
                if (R[y][x0+i]=='.')!=(c=='.'): print('SILHOUET',k,x0+i,y,R[y][x0+i],'->',c)
                R[y][x0+i]=c
    return [''.join(r) for r in R]
L1="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoabdabocccc|
40|...owwwoabdbcooooo|
41|....owoabobcoabbco|
42|.....oobcobcobccoo|
43|......oooobcobco.o|
44|..........oobco..o|
45|...........oo...oo|
"""
L2="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoabdabocccc|
40|...owwwoabobcooooo|
41|....owwwoobcoabbco|
42|.....owwwobcobccoo|
43|......oooobcobco.o|
44|..........oobco..o|
45|...........oo...oo|
"""
for k in ['L1','L2']: V[k]=rows(BL,37,globals()[k])
L3="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoaabbbocccc|
40|...owwwoccccccoooo|
41|....owwwobbbbbccco|
42|.....owwocccccccoo|
43|......oooobbbcco.o|
44|..........occoo..o|
45|...........oo...oo|
"""
V['L3']=rows(BL,37,L3)
L4="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoaabbbocccc|
40|...owwwoocccccoooo|
41|....owwwwooccbbcco|
42|.....owwobbobccdoo|
43|......ooooccocdo.o|
44|..........occoo..o|
45|...........oo...oo|
"""
L5="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoaabbbocccc|
40|...owwwobccccdoooo|
41|....owwooooobbccco|
42|.....owwwwwocccdoo|
43|......oooooobcco.o|
44|..........obcoo..o|
45|...........oo...oo|
"""
for k in ['L4','L5']: V[k]=rows(BL,37,globals()[k])
RA="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....oaowwaoo..|
29|...oabowwaoo..|
30|...oabooooo...|
31|.oobbcaabo....|
32|obobccbbcco...|
33|abocccoabco...|
34|bbocdcccdo....|
35|ccoddoooo.....|
36|cccoooo.......|
37|cccoo.........|
"""
RB="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....dwwooaoo..|
29|...dwwoabooo..|
30|...dwoabcoo...|
31|.oooobccoo....|
32|obobabcobco...|
33|abobbccobco...|
34|bbocccdodo....|
35|ccoddoooo.....|
36|cccoooo.......|
37|cccoo.........|
"""
RC="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....odwwwaoo..|
29|...oaowwoooo..|
30|...oaoowoabo..|
31|.oobboaboaco..|
32|obobcboooco...|
33|abobbcccbco...|
34|bbocccccdo....|
35|ccoddoooo.....|
36|cccoooo.......|
37|cccoo.........|
"""
for k in ['RA','RB','RC']: V[k]=rows(BR,26,globals()[k])
RA2="""
26|......dwoooao.|
27|.....owwwoaao.|
28|....oaowwaoo..|
29|...oabowwaoo..|
30|...oabcoooo...|
31|.oobbcobbo....|
32|obobccbbcco...|
33|abobccoocco...|
34|bboccbbbco....|
35|ccoddddoo.....|
36|cccoooo.......|
37|cccoo.........|
"""
V['RA2']=rows(BR,26,RA2)
RC2="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....dwooawoo..|
29|...dwoaboaoo..|
30|...dwoacoao...|
31|.ooooobcoo....|
32|obobabccbco...|
33|abobbcdobco...|
34|bbocccdcdo....|
35|ccoddoooo.....|
36|cccoooo.......|
37|cccoo.........|
"""
V['RC2']=rows(BR,26,RC2)
L5b="""
37|.dwwwwwwo.occccccc|
38|.dwwwowooooooccccc|
39|..owoowoaabbbocccc|
40|...owwwoccccccoooo|
41|....owwooooobbccco|
42|.....owwwwwobcccoo|
43|......ooooooobco.o|
44|..........occoo..o|
45|...........oo...oo|
"""
RB2="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....dwwowaoo..|
29|...dwwoaowoo..|
30|...dwoabooo...|
31|.oooobbcoo....|
32|obobbbccbco...|
33|abobbccobco...|
34|bboccccoco....|
35|ccoddoooo.....|
36|cccoooo.......|
37|cccoo.........|
"""
RC3="""
26|......dwoooao.|
27|.....dwwwoaao.|
28|....dwoowaoo..|
29|...dwoaaowoo..|
30|...dwoacowo...|
31|.ooooobcoo....|
32|obobbobbcco...|
33|abobcdocbco...|
34|bboccdccco....|
35|ccoddoooo.....|
36|cccoooo.......|
37|cccoo.........|
"""
for k in ['L5b','RB2','RC3']: V[k]=rows(BL if k[0]=='L' else BR,37 if k[0]=='L' else 26,globals()[k])
