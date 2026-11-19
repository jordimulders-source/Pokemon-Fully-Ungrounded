# 2 kuifslierten: twee lijnen van 1 px, per kolom de rij met de hoogste zwartdekking in het 1024-model (dekkingskaart in het rapport).
# Krul (43-46,4-7) en haakje (40-42,9-10) blijven zoals in r2.
import numpy as np
U=[(17,6),(18,5),(19,5),(20,4),(21,3),(22,3),(23,3)]+[(x,2) for x in range(24,34)]+[(34,3),(35,3),(36,4),(37,4),(38,5),(39,6)]+[(x,7) for x in range(40,46)]
KRUL=[(43,6),(43,5),(44,4),(45,4),(46,5),(46,6),(44,5)]
L=[(x,5) for x in range(24,36)]+[(36,6),(37,6),(38,7),(39,8),(40,9),(40,10),(41,10),(42,9)]
def run(o):
    n=o.copy(); keep=set(U+KRUL+L)
    for y in range(0,11):
        for x in range(17,48):
            if (x,y) in keep: n[y,x]=1
            elif n[y,x]==1 and (y<=5 and x>=19 or x>=31 and y<=10): n[y,x]=0
    return n
if __name__=='__main__':
    o=np.load('_tmp/s1.npy'); n=run(o); np.save('_tmp/s2.npy',n); print('kuif px',(n!=o).sum())
