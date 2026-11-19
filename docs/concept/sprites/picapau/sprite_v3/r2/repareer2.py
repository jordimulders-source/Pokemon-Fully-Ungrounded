# r2: benoemde reparaties van de coordinator op r1.npy. Codes als r1; nieuw: 18 = middengrijs.
# Grijs: 10 = licht (nieuw 180 180 172), 18 = midden (124 124 128), 11 = donker (64 64 72). Glans 16 -> creme 14.
import numpy as np
o=np.load('r1.npy').copy(); R={}
def zet(zone,lst):
    for x,y,v in lst: R.setdefault(zone,[]).append((x,y,o[y,x],v)); o[y,x]=v
# 1 VLEUGEL: hoofdkleur donker (13), licht (12) alleen als smalle strook aan voorrand/schouder; 4 cremestippen op modelplek
vl=[]
for y in range(24,45):
    for x in range(33,50):
        if o[y,x]==12: vl.append((x,y,13))
zet('vleugel donker',vl)
zet('vleugel voorrand licht',[(38,26,12),(39,26,12),(40,26,12),(37,28,12),(37,29,12),(37,30,12),(37,31,12),(38,32,12)])
zet('stippen',[(41,27,13),(42,27,14),(43,27,1),(40,27,13),(44,32,14),(39,27,14)])   # stip 2 op modelplek x42 (rand 1 px naar buiten, model dekt 1/3), stip 4 2x2-ish
# 2 WANG: ronde schijf uit de modeldekking (>=4.5/9): 3/5/5/5/3, sikkel rechtsonder
w=[(30,23,5),(31,23,5),(32,23,5),(29,24,5),(30,24,5),(31,24,5),(32,24,5),(33,24,5),
   (29,25,5),(30,25,5),(31,25,5),(32,25,5),(33,25,6),(29,26,5),(30,26,5),(31,26,5),(32,26,5),(33,26,6),
   (30,27,5),(31,27,5),(32,27,6),(34,25,4)]
zet('wang',[t for t in w if o[t[1],t[0]]!=t[2]])
# 3 SNAVEL: kegel uit de modeltonen (3 grijzen), licht binnen, midden aan de bovenrand, zwart onder
s=[(19,18,11),(20,18,18),(20,19,18),(21,19,10),(22,19,10),(23,19,18),
   (20,20,1),(21,20,10),(22,20,10),(23,20,10),(24,20,18),
   (21,21,1),(22,21,18),(23,21,18),(24,21,18),(25,21,18),
   (21,22,1),(22,22,11),(23,22,11),(24,22,18),(25,22,18),(26,22,11),
   (22,23,1),(23,23,11),(24,23,11),(25,23,18),(26,23,1),
   (23,24,1),(24,24,1),(25,24,1)]
zet('snavel',[t for t in s if o[t[1],t[0]]!=t[2]])
# 4 VERRE WANG: 1 px rood binnen de koprand, omlijnd met selout
zet('verre wang',[(20,23,17),(21,23,3),(21,24,17),(21,25,17),(22,25,5)])
# 5 VOETEN: verre (linker) poot donkergrijs, tenen omlijnd, geen zwart tussen de tenen; nabije poot midden/licht
zet('verre poot',[(29,45,11),(30,45,11),(29,46,11),(30,46,11),(30,47,11),
   (26,48,1),(27,48,11),(28,48,11),(29,48,11),(30,48,11),(31,48,11),(30,49,1)])
zet('nabije poot',[(34,46,18),(35,46,18),(34,47,18),(35,47,18),(34,48,18),(35,48,18),(33,48,1),
   (31,49,10),(32,49,10),(33,49,10),(34,49,18),(35,49,18)])
zet('oogglans',[(30,19,14)])
np.save('r2.npy',o)
t=0
for z,l in R.items(): print('%-24s %2d px'%(z,len(l))); t+=len(l)
print('totaal t.o.v. r1',t)
