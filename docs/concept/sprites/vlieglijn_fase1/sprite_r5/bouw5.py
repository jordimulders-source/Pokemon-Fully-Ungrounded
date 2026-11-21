# r5 basis: r4 zonder de verre poten, met de benoemde reparaties (canvas-coördinaten x,y; hex-index)
import numpy as np
f=np.loadtxt('basis_r4_zonder_verre.txt',dtype=int)
ZONES={}
def P(zone,y,x,s):
    for k,ch in enumerate(s):
        if ch==' ': continue
        f[y,x+k]=0 if ch=='.' else int(ch,16); ZONES.setdefault(zone,set()).add((x+k,y))
# 2. poot 3 onderbeen recht omlaag (glans op x31), voet knikt pas vanaf y57: een klauw omlaag, een naar rechts
for y in range(47,62): 
    for x in range(26,38):
        if f[y,x] in (1,7,8,9,14,15,10,12) and not (y<=48 and x<=27): f[y,x]=0; ZONES.setdefault('poot3',set()).add((x,y))
P('poot3',47,29,'1AAA1'); P('poot3',48,29,'1CCC1')   # ring (zoals r4)
for y in range(49,57): P('poot3',y,30,'1971')
P('poot3',57,31,'1971')
P('poot3',58,32,'1E1EE1'); P('poot3',59,32,'1E111F1'); P('poot3',60,33,'1F1.11'); P('poot3',61,34,'1')
# 3. poot 4 voet: klauwen uitwaaierend naar rechts tot x51
for y in range(56,61):
    for x in range(44,54):
        if f[y,x]!=0: f[y,x]=0; ZONES.setdefault('poot4voet',set()).add((x,y))
P('poot4voet',56,46,'11EE11'); P('poot4voet',57,46,'1E11EF1'); P('poot4voet',58,47,'1EE11'); P('poot4voet',59,48,'11EF1'); P('poot4voet',60,50,'11')
# 4. poot 4 aanzet: horizontaal stuk tot x39 op y40, daarna pas omlaag
P('poot4aanzet',39,37,'111'); P('poot4aanzet',40,33,'99999989')
P('poot4aanzet',40,41,'1'); P('poot4aanzet',41,35,'1111998'); P('poot4aanzet',41,42,'1')
P('poot4aanzet',42,38,'31987'); P('poot4aanzet',42,43,'1')
# 5. ^-ogen: punt 2 px hoog, schuine benen
P('ogen',30,17,'2D2'); P('ogen',30,9,'2D2')
# 7. vleugelrand
P('vleugel',25,31,'C')
np.savetxt('r5_basis.txt',f,fmt='%2d')
import pickle; pickle.dump(ZONES,open('zones.pkl','wb'))
