# Plakt de ogen uit het ingedikte natieve blok (variant B) op de kale reductie.
import sys; from gemeen import *; from ogen import blok
IN=sys.argv[1] if len(sys.argv)>1 else 'kaal.npy'; OUT=sys.argv[2] if len(sys.argv)>2 else 'r1_ogen.npy'
VAR=sys.argv[3] if len(sys.argv)>3 else 'B'
FORCE=[int(v) for v in sys.argv[4].split(',')] if len(sys.argv)>4 else None
FORCEY=[int(v) for v in sys.argv[5].split(',')] if len(sys.argv)>5 else None
S=np.load(IN).copy(); B,cols,rows=blok(VAR)
# eerst de oogresten van de kale reductie in het gezicht wissen (oogkleuren -> zandtint van de buren)
ZAND=[2,3,4,5,6]
for _ in range(3):
    for y in range(23,34):
        for x in range(27,47):
            v=S[y,x]; nb=[S[y+a,x+b] for a,b in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))]
            zn=[n for n in nb if n in ZAND]
            if v in (1,14,15,7) and sum(n in ZAND+[1,14,15] for n in nb[:4])>=3:
                if zn: S[y,x]=max(set(zn),key=zn.count)

w=np.pad(B==14,1); w8=np.zeros(B.shape,bool)
for a in (-1,0,1):
    for b in (-1,0,1): w8|=w[1+a:1+a+B.shape[0],1+b:1+b+B.shape[1]]
B=B.copy(); B[(B==9)&w8]=15
oog=np.isin(B,[1,14,15])|((B==7)&w8)
# kas: zandpixels die 4-buur zijn van een oogpixel
pad=np.pad(oog,1); buur=pad[:-2,1:-1]|pad[2:,1:-1]|pad[1:-1,:-2]|pad[1:-1,2:]
kas=buur&~oog&np.isin(B,[2,3])
mask=oog|kas
# uitlijnen per oog: zwaartepunt van de oogpixels (natief -> sprite)
lab=np.zeros(B.shape,int); lab[:, :cols.index(51) if 51 in cols else 8]=1; lab[:, (cols.index(54)):]=2
lab[:, cols.index(51) if 51 in cols else 8:cols.index(54)]=0
n=0; offs=[]
for e in (1,2):
    oe=oog&(lab==e); me=mask&(lab==e)
    yy,xx=np.where(oe)
    nx=np.array([cols[i] for i in xx])+0.5; ny=np.array([rows[j] for j in yy])+0.5
    sx,sy=m2s(n2m(0)+nx.mean()*NP, n2m(0)+ny.mean()*NP)
    dx=int(round(sx-xx.mean()-0.5)); dy=int(round(sy-yy.mean()-0.5))
    if FORCE: dx=FORCE[e-1]
    if FORCEY: dy=FORCEY[e-1]
    # hele oogkader (bbox van het oog) overnemen, behalve glas
    yy2,xx2=np.where(oe); kad=np.zeros(B.shape,bool); kad[yy2.min():yy2.max()+1,xx2.min():xx2.max()+1]=True
    me=me|(kad&np.isin(B,[1,2,3,4,5,6,14,15]))
    offs.append((dx,dy))
    for j,i in zip(*np.where(me)):
        t=S[j+dy,i+dx]
        if t in (2,3,4,5,6,1,14,15,7) or (t==9 and B[j,i] in (1,14,15)):
            if t!=B[j,i]: n+=1
            S[j+dy,i+dx]=B[j,i]
print('offsets',offs,'pixels veranderd',n)
np.save(OUT,S); json.dump(dict(offs=offs,var=VAR),open('ogen_geo.json','w'))
