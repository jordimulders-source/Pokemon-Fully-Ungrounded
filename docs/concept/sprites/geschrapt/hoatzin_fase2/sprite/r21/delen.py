# onderdelenkaart van r19 (alpha = r19-vorm): kuif, verre vleugel, kop, nek, vleugel, buik, staart, poten, oog/snavel
import numpy as np, sys
from meet import cel
sys.path.insert(0,'../r17'); import importlib.util
spec=importlib.util.spec_from_file_location('bev','../r17/bevroren.py'); bev=importlib.util.module_from_spec(spec)
import os; cwd=os.getcwd(); os.chdir('../r17'); spec.loader.exec_module(bev); MS=bev.maskers(); os.chdir(cwd)
STAART=bev.schuif(MS['staart'],-1,0)
LIJN={23:27,24:27,25:27,26:27,27:26,28:25,29:25,30:24,31:23,32:23,33:23,34:23,35:24,36:25,37:26,38:26,39:27,40:26}
NAMEN=['leeg','kuif','verre','kop','nek','vleugel','buik','staart','poot','gezicht']
def delen(o):
    P=np.zeros((64,64),int); A=o>0
    for y in range(64):
        for x in range(64):
            if not A[y,x]: continue
            v=o[y,x]
            if v in (11,12,13): p='buik'
            elif y>=51 and x<=36: p='poot'
            elif STAART[y,x] or (y>45 and x>=37): p='staart'
            elif v in (8,9,10) or (v in (14,15) and y<30): p='gezicht'
            elif y>=51 and x<=37: p='poot'
            elif y<=22 and x<=29 and not (x>=26 and y>=17):
                c=cel(x,y); p='kuif' if ((c and c['bruin']>=5) or x<=8) else 'verre'   # r20: kuif = vol bruin in het model; rest = mauve veren erachter
            elif 23<=y<=40 and x>=LIJN[y]: p='vleugel'
            elif y<23 and x>=26: p='vleugel'
            elif y>40 and x<26: p='buik'
            elif y>40: p='vleugel'
            elif y>=27: p='nek'
            else: p='kop'
            P[y,x]=NAMEN.index(p)
    return P
if __name__=='__main__':
    o=np.load('r19.npy'); P=delen(o)
    ch='.KVkNWbSPg'
    for y in range(64): print('%2d '%y+''.join(ch[v] for v in P[y]))
