# r5: stekels (achterkuif rechts) en poten netter; vorm/plek naar het model (_m_st.png, _m_poot.png). Daarna oogvarianten.
import numpy as np
o=np.load('r4.npy').copy(); R={}
def zet(z,l,arr=None):
    a=o if arr is None else arr
    for x,y,v in l:
        if a[y,x]!=v: R.setdefault(z,[]).append((x,y,int(a[y,x]),v)); a[y,x]=v
# 1 stekels: driehoeken, bovenrand selout (17), onderrand en punt zwart, binnen donkergeel; punten op modelplek (A x40 r11, B x41 r17)
zet('stekel A',[(37,11,1),(38,11,17),(39,11,17),(37,12,4),(38,12,4),(39,12,4),(40,12,1),(38,13,4),(39,13,1)])
zet('stekel B',[(39,16,17),(40,16,17),(40,17,4)])
# 2 poten: verre (links) donkergrijs 1 rij hoger, nabije licht+donker, beide voeten apart omlijnd
for y in range(45,51):
    for x in range(25,39):
        if o[y,x] in (10,11) or (y>=46 and o[y,x]==1): zet('poten wissen',[(x,y,0)])
P={ # (x,y): code
 (29,45):1,(30,45):11,(31,45):1,
 (29,46):1,(30,46):11,(31,46):1,(27,46):1,(28,46):1,
 (26,47):1,(27,47):11,(28,47):11,(29,47):11,(30,47):11,(31,47):11,(32,47):1,
 (27,48):1,(28,48):1,(29,48):1,(30,48):1,(31,48):1,
 (33,46):1,(34,46):10,(35,46):11,(36,46):1,
 (33,47):1,(34,47):10,(35,47):11,(36,47):1,(37,47):1,
 (32,48):1,(33,48):10,(34,48):10,(35,48):11,(36,48):11,(37,48):1,
 (33,49):1,(34,49):1,(35,49):1,(36,49):1,(37,49):1}
zet('poten',[(x,y,v) for (x,y),v in P.items()])
np.save('r5.npy',o)
for z,l in R.items(): print('%-14s %2d'%(z,len(l)))
# oogvarianten (alleen zone verre oog/snavelbovenrand)
V={'A':[],
   'B':[(21,18,11),(22,18,11),(23,16,1),(24,16,1)],
   'C':[(21,18,11),(22,18,11),(23,17,1)],
   'D':[(21,18,11),(22,18,11),(23,17,1),(23,16,1)]}
for k,l in V.items():
    a=o.copy()
    for x,y,v in l: a[y,x]=v
    np.save('var_%s.npy'%k,a)
