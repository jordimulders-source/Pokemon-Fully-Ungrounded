import sys; sys.path.insert(0,"r5"); from zones import *
for nm,Z in [('onderkop',ONDERKOP),('lijf',LIJF)]:
  for i in (3,4,5,6):
    s=Z&(E==i)
    if s.sum()==0: continue
    ml=L(M[s]); 
    print(nm,i,'n',s.sum(),'pal',PAL[i],'model lum pct',np.percentile(ml,[10,25,50,75,90]).round(), 'model med rgb',np.median(M[s],0))
