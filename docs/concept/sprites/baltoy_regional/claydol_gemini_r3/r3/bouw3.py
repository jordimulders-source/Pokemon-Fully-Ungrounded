# Ronde 3: onderkopzone (rijen 31-38, x 15-47, hoofdfiguur) terug naar g3; daarna alleen de r2-tintomzetting
# (steen 4->5, creme 5->4). Rest = r2. Niets gladmaken of middelen.
import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r2')
from cc import label
from creme import cremeMasker
G3=np.load('sprite.npy'); R2=np.load('r2/sprite_r2.npy')
comp,_=label(G3>0,diag=True); HOOFD=np.bincount(comp.ravel())[1:].argmax()+1
ZONE=np.zeros((64,64),bool); ZONE[31:39,15:48]=True; ZONE&=(comp==HOOFD)
S=R2.copy(); S[ZONE]=G3[ZONE]
M=cremeMasker(S)
G3T=G3.copy(); G3T[ZONE&M&(G3==5)]=4; G3T[ZONE&~M&(G3==4)]=5   # g3 na tintomzetting
S[ZONE]=G3T[ZONE]
np.save('r3/sprite_r3.npy',S)
if __name__=='__main__':
    print('zone px',ZONE.sum(),'| tintomzettingen in zone',int((G3T!=G3)[ZONE].sum()))
    print('BEWIJS onderkopzone == g3 (na tintomzetting):',bool((S[ZONE]==G3T[ZONE]).all()))
    print('BEWIJS rest == r2:',bool((S[~ZONE]==R2[~ZONE]).all()),'| px anders dan r2:',int((S!=R2).sum()),'(allemaal in zone:',bool(((S!=R2)&~ZONE).sum()==0),')')
    print('4 in zone:',int((S[ZONE]==4).sum()),'| tinten in zone',np.unique(S[ZONE]).tolist())
    c,n=label(S>0,diag=True); print('componenten',n)
