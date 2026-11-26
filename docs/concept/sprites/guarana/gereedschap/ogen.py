# ogen.py: oogmaskers uit het model (natief) en dekking per spritepixel. Pupil = zwarte modelpixels binnen het oogwit (gemeten, zie NOTITIES).
import sys; sys.path.insert(0,'gereedschap')
import numpy as np; from klassen import klassen; from gemeen import *
a,c,L=klassen()
PUPIL={'boven':[(28,27),(27,28),(28,28),(29,28),(27,29),(28,29),(29,29),(28,30)],
       'rechts':[(43,31),(44,31),(42,32),(43,32),(44,32),(43,33)],
       'onder':[(25,44),(26,44),(24,45),(25,45),(26,45),(24,46),(25,46)]}
BOX={'boven':(25,33,24,32),'rechts':(38,47,29,35),'onder':(22,31,41,50)}   # u0,u1,v0,v1 natief (incl.)
def dekking(naam):
    pm=np.zeros(c.shape,bool)
    for u,v in PUPIL[naam]: pm[v,u]=True
    u0,u1,v0,v1=BOX[naam]
    wm=np.zeros(c.shape,bool); wm[v0:v1+1,u0:u1+1]=(c[v0:v1+1,u0:u1+1]==4)
    res={}
    for Y in range(64):
        for X in range(64):
            fp=fw=0
            for u,v,w in overlap(X,Y): fp+=w*pm[v,u]; fw+=w*wm[v,u]
            if fp+fw>0.05: res[(X,Y)]=(fp,fw)
    return res
if __name__=='__main__':
    for n in PUPIL:
        r=dekking(n); xs=[k[0] for k in r]; ys=[k[1] for k in r]
        print(n,'pupil/wit dekking per spritepixel')
        for Y in range(min(ys),max(ys)+1):
            print('%2d '%Y+' '.join(('%2d/%2d'%(100*r[(X,Y)][0],100*r[(X,Y)][1]) if (X,Y) in r else '  .  ') for X in range(min(xs),max(xs)+1)))
        print('   X',min(xs),'..',max(xs))
