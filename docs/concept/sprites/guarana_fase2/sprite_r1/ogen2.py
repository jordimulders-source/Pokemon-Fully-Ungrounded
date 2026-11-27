# Oogplekken in het natieve model (met de hand aangewezen op 10x-uitsneden, zie NOTITIES) + gemeten kijkrichting:
# wit = klasse 4 binnen straal 8 rond het aangewezen punt; pupil = zwart dat links+rechts of boven+onder binnen 4 cellen wit heeft.
import sys, numpy as np; sys.path.insert(0,'sprite_r1')
from klassen2 import klassen; from gemeen2 import *
OGEN={ # naam: (u,v, soort)   soort: open | lid (half dicht, ooglid van het model) | klein (deels verstopt)
 'L1':(33,100,'lid'),'L2':(51,93,'open'),'L3':(61,102,'klein'),'L4':(50,112,'open'),'L5':(59,120,'open'),
 'M1':(100,64,'open'),'M2':(85,71,'lid'),'M3':(72,82,'lid'),'M4':(98,83,'open'),'M5':(85,92,'klein'),
 'R1':(144,91,'open'),'R2':(162,92,'open'),'R3':(135,100,'klein'),'R4':(153,98,'lid'),'R5':(145,111,'open'),'R6':(136,118,'open')}
def meet():
    a,c,L=klassen(NATIEF); res={}
    for n,(u,v,s) in OGEN.items():
        W=[];P=[]
        for y in range(v-8,v+9):
            for x in range(u-8,u+9):
                if (x-u)**2+(y-v)**2>64: continue
                lw=a[y,x].min()>=150 and (a[y,x].max()-a[y,x].min())<40
                if lw: W.append((x,y))
        Ws=set(W)
        for y in range(v-8,v+9):
            for x in range(u-8,u+9):
                if (x-u)**2+(y-v)**2>64 or c[y,x]!=1: continue
                lr=any((x-d,y) in Ws for d in range(1,5)) and any((x+d,y) in Ws for d in range(1,5))
                ud=any((x,y-d) in Ws for d in range(1,5)) and any((x,y+d) in Ws for d in range(1,5))
                if lr or ud: P.append((x,y))
        W=np.array(W); P=np.array(P) if P else np.zeros((0,2))
        allp=np.vstack([W,P]) if len(P) else W
        m=allp.mean(0); pm=P.mean(0) if len(P) else m
        res[n]=dict(u=u,v=v,soort=s,nw=len(W),np=len(P),mid=m,pupil=pm,kijk=pm-m,
                    w=(allp[:,0].max()-allp[:,0].min()+1),h=(allp[:,1].max()-allp[:,1].min()+1),sprite=naar_sprite(*m))
    return res
if __name__=='__main__':
    for n,r in meet().items():
        print(n,r['soort'],'wit',r['nw'],'pupil',r['np'],'maat %dx%d'%(r['w'],r['h']),'kijk %+.1f %+.1f'%tuple(r['kijk']),'sprite %.1f %.1f'%r['sprite'])
