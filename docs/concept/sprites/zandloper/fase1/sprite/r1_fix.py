# r1: benoemde pixelreparaties op kale reductie + ogen. Elke pixel met reden.
import sys; from gemeen import *
IN=sys.argv[1] if len(sys.argv)>1 else 'r1_ogen.npy'; OUT=sys.argv[2] if len(sys.argv)>2 else 'r1/zandloper_fase1_r1.png'
S=np.load(IN).copy()
FIX=[  # (x,y, van, naar, reden)
 (32,14,12,11,'bovenkap bovenrand: geen middentint op de buitenrand -> donkere selout'),
 (33,14,12,11,'idem'),(39,16,12,11,'idem'),(40,16,12,11,'idem'),
 (12,30,13,11,'linkerhand bovenrand: lichte tint op de buitenrand -> selout'),(13,30,13,11,'idem'),
 (49,39,13,11,'rechterhand bovenrand: idem'),(50,39,13,11,'idem'),
 (16,46,12,11,'onderkap linkerbovenrand: middentint op de buitenrand -> selout'),
 (19,42,10,8,'onderbol linkerrand: lichtblauw op de buitenrand -> glas-donker zoals de rest van die rand'),
 (42,36,8,7,'bovenbol rechtsonder: losse glas-donker in de glaslijn -> glaslijn'),
 (14,37,11,1,'linkerhand onderrand (schaduwkant) -> zwart zoals de rest van de onderrand'),
 (48,44,11,1,'rechterhand onderrand -> zwart'),(51,44,12,1,'rechterhand onderrand -> zwart'),
]
for x,y,a,b,r in FIX:
    assert S[y,x]==a,(x,y,S[y,x],a); S[y,x]=b
np.save(OUT.replace('.png','.npy'),S); opslaan(S,OUT)
P=np.pad(S,1); fout=[]
for y in range(64):
    for x in range(64):
        if S[y,x] and S[y,x] not in (1,7,8,11) and 0 in (P[y,x+1],P[y+2,x+1],P[y+1,x],P[y+1,x+2]): fout.append((x,y,NAAM[S[y,x]]))
print('buitenrand-fouten',fout); print('kleuren',len(np.unique(S)),'gevuld',(S>0).sum())
