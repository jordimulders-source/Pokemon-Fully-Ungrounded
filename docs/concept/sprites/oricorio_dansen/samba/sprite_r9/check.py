# check.py: kleine tintvlakjes (4- en 8-buren) r8 vs r9, en pixelgelijkheid oog/snavel/poten met r8
import numpy as np, json
from scipy import ndimage
a=np.load('samba_r9.npy'); r8=np.load('../sprite_r8/samba_r8.npy')
def klein(a,conn):
    st=np.ones((3,3)) if conn==8 else None; out=[]
    for c in range(2,16):
        if c in (1,): continue
        lab,n=ndimage.label(a==c,structure=st)
        for i in range(1,n+1):
            p=np.argwhere(lab==i)
            if len(p)<3: out.append((c,[(int(x),int(y)) for y,x in p]))
    return out
# vrijgesteld: selout (grenst aan transparant), oog/snavel/poten (roze/wit/blauw-zwart) -> zone-uitsluiting
def rand(a,x,y): return any(a[y+dy,x+dx]==0 for dy,dx in((0,1),(0,-1),(1,0),(-1,0)))
def filt(a,l): return [(c,p) for c,p in l if c in (2,3,4,5,6,7,8) and not all(rand(a,x,y) for x,y in p)]
zones={'oog':(26,32,38,34),'snavel':(24,26,28,34),'poten':(17,46,40,62)}
res={}
for n,(x0,y0,x1,y1) in zones.items():
    m=np.zeros_like(a,bool); m[y0:y1,x0:x1]=True
    if n=='poten': m&=np.isin(r8,(11,12,13))|np.isin(a,(11,12,13))
    m=np.zeros_like(m)|m
    # poten/snavel: elke pixel met roze (11-13) in r8 of r9 plus hun directe buren (lijn)
    if n!='oog': m=ndimage.binary_dilation(np.isin(r8,(11,12,13)),np.ones((3,3)))&(np.arange(64)[:,None]>=(48 if n=='poten' else 26))&(np.arange(64)[:,None]<(64 if n=='poten' else 36))
    res[n+'_gelijk_aan_r8']=bool((a[m]==r8[m]).all()); res[n+'_px']=int(m.sum())
for nm,arr in (('r8',r8),('r9',a)):
    for conn in (4,8):
        l=filt(arr,klein(arr,conn)); res['%s_klein_groen_geel_%dconn'%(nm,conn)]=len(l)
        if nm=='r9' and conn==8: res['r9_rest_8conn']=l
# per zone tellen (4-conn)
Z={'1_vleugel':(47,12,57,26),'2a':(33,12,41,16),'2b':(15,17,21,21),'3':(28,24,38,25),'4':(26,42,42,48),'5':(13,42,24,46),'6':(24,34,44,38)}
for nm,arr in (('r8',r8),('r9',a)):
    l=filt(arr,klein(arr,4))
    for z,(x0,y0,x1,y1) in Z.items():
        res['%s_zone%s_4conn'%(nm,z)]=sum(1 for c,p in l if any(x0<=x<=x1 and y0<=y<=y1 for x,y in p))
json.dump(res,open('check_r9.json','w'),indent=1); print(json.dumps({k:v for k,v in res.items() if k!='r9_rest_8conn'},indent=0)); print(res['r9_rest_8conn'])
