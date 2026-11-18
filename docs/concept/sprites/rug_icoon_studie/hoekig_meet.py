"""Hoe hoekig is een silhouet? Over de buitenomtrek van frame 1:
- recht: aandeel van de randpixels in rechte horizontale/verticale stukken van >= 4 px
- trapjes: aantal diagonale stapjes (lege pixel in een L van 3 volle) per 100 randpixels; hoger = ronder/schuiner
python3 hoekig_meet.py [icon.png]   -> zonder argument: normen in-game iconen Gen 1-3 en Gen 9"""
import os,re,sys,numpy as np
from PIL import Image
def maat(f1):
    m=f1>0
    if not m.any(): return None
    pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    n=edge.sum(); recht=np.zeros_like(edge)
    for arr,T in ((edge,False),(edge.T,True)):
        r=np.zeros_like(arr)
        for i,row in enumerate(arr):
            j=0
            while j<len(row):
                if row[j]:
                    k=j
                    while k<len(row) and row[k]: k+=1
                    if k-j>=4: r[i,j:k]=True
                    j=k
                else: j+=1
        recht|= (r.T if T else r)
    # rechte buitenhoek: lege pixel met precies 2 orthogonale vol-buren die een L vormen, en de diagonaal ertussen vol
    e=~m; P=np.pad(m,1); c=0
    for (a,b,dg) in [((0,1),(1,0),(1,1)),((0,1),(-1,0),(-1,1)),((0,-1),(1,0),(1,-1)),((0,-1),(-1,0),(-1,-1))]:
        A=P[1+a[0]:P.shape[0]-1+a[0],1+a[1]:P.shape[1]-1+a[1]]
        B=P[1+b[0]:P.shape[0]-1+b[0],1+b[1]:P.shape[1]-1+b[1]]
        D=P[1+dg[0]:P.shape[0]-1+dg[0],1+dg[1]:P.shape[1]-1+dg[1]]
        c+=(e&A&B&D).sum()
    return recht.sum()/n, 100*c/n
if __name__!='__main__': pass
elif len(sys.argv)>1:
    r,h=maat(np.array(Image.open(sys.argv[1]))[:32]); print(f'recht {r:.2f}  trapjes/100 rand {h:.1f}')
else:
    gen={}
    for g in range(1,10):
        for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]',open(f'src/data/pokemon/species_info/gen_{g}_families.h').read()): gen[mm.group(1).lower()]=g
    G='graphics/pokemon'; out={'in-game 1-3':[],'gen 9':[],'vanilla gba':[]}
    for sp in os.listdir(G):
        d=f'{G}/{sp}'
        if os.path.exists(d+'/icon.png') and gen.get(sp) in (1,2,3): out['in-game 1-3'].append(maat(np.array(Image.open(d+'/icon.png'))[:32]))
        if os.path.exists(d+'/icon.png') and gen.get(sp)==9: out['gen 9'].append(maat(np.array(Image.open(d+'/icon.png'))[:32]))
        if os.path.exists(d+'/icon_gba.png'): out['vanilla gba'].append(maat(np.array(Image.open(d+'/icon_gba.png'))[:32]))
    for k,v in out.items():
        v=np.array([x for x in v if x]); print(k,'recht p10/50/90',np.percentile(v[:,0],[10,50,90]).round(2),' trapjes',np.percentile(v[:,1],[10,50,90]).round(1))
