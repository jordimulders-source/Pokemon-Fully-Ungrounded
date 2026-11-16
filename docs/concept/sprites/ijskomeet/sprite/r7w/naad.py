import sys; sys.path.insert(0,'r7w')
from body import *
Fl=np.load('r7w/Fl.npy')
eye=isin(R,'erCg')
eyez=np.zeros((64,64),bool)
for j,i in zip(*np.where(eye)): eyez[j-1:j+2,i-1:i+2]=True
inter=body&~outer
thr=float(sys.argv[1]) if len(sys.argv)>1 else 0.12
cand=inter&(Fl>=thr)&~eyez
fixed=outer.copy()
fg=cand|fixed
N8=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
def removable(j,i):
    nb=[fg[j+dy,i+dx] for dy,dx in N8]
    n=sum(nb)
    if n<2: return False   # eindpunt/los: laat staan (los wordt later gefilterd)
    tr=sum((not nb[k]) and nb[(k+1)%8] for k in range(8))
    if tr!=1: return False
    return True
ch=True
while ch:
    ch=False
    pts=sorted(zip(*np.where(fg&~fixed)),key=lambda p:Fl[p])
    for j,i in pts:
        if fg[j,i] and removable(j,i):
            # niet weghalen als het een endpoint wordt van een lijn: n==2 aangrenzend -> wel weghalen (staart inkorten) alleen als Fl laag
            nb=[fg[j+dy,i+dx] for dy,dx in N8]
            if sum(nb)==1: continue
            fg[j,i]=False; ch=True
seam=fg&~fixed
np.save('r7w/seam_auto.npy',seam)
for j in range(22,62):
  print('%2d '%j+''.join(('o' if outer[j,i] else ('#' if seam[j,i] else ('e' if eye[j,i] else ('.' if not body[j,i] else ' ')))) for i in range(0,36))+'   '+''.join('.' if R[j,i]<0 else CH[R[j,i]] for i in range(0,36)))
