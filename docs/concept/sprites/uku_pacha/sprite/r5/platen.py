# Uku Pacha r5: plaatgrenzen van de voorkant van beide nekken, gemeten op het natieve model (cellen),
# als polylijn geprojecteerd naar de sprite (factor 64/92, zelfde transformatie als geom.py r1-r4).
F=64/92; X0,Y0,OX,OY=5,7,0,2
def n2s(x,y): return OX+(x+0.5-X0)*F, OY+(y+0.5-Y0)*F
# (naam, modelcellen langs de lijn, tint in licht vlak, tint in medium vlak)
# tint naar de gemeten modelkleur van de lijncellen: L0/L1/L2/A ~ (73,102,120) -> s;
# B, kruislijn X, C, D ~ (42-52,59-74,75-92), zo donker als de bandranden (n) -> n
LIJNEN=[
 ('R-a',[(60,21),(62,22),(63,23),(67,23)],'n','n'),
 ('R-b',[(61,30),(62,31),(65,31),(67,30)],'n','n'),
 ('L0', [(57,34),(59,36),(60,37),(63,37),(65,36)],'s','n'),
 ('L1', [(53,40),(54,41),(55,41),(58,44)],'s','n'),
 ('L2', [(45,46),(48,46),(50,47),(51,48),(52,49)],'s','n'),
 ('X',  [(44,47),(41,50),(41,51),(38,54),(38,55),(36,57),(36,58),(34,60),(34,62)],'n','n'),
 ('LA', [(42,32),(39,35),(38,36),(37,36)],'n','n'),
 ('LB', [(37,41),(41,41),(43,39)],'n','n'),
 ('A',  [(30,56),(31,56),(33,59),(34,60)],'s','n'),
 ('B',  [(28,64),(31,67),(34,67),(37,65),(41,65),(44,64)],'n','d'),
 ('C',  [(26,71),(27,71),(29,73),(31,74),(35,74),(38,73),(42,71)],'n','n'),
 ('D',  [(27,79),(29,81),(31,82),(35,82),(38,80),(41,78)],'n','n'),
 # E: plaatgrens in de medium buik onder D (model lum ~60); r3/r4 hadden hem als d-stuk met n-stompjes
 ('E',  [(30,88),(32,88),(33,89),(39,89),(40,88),(41,88)],'n','n'),
]
# vaste rasterpaden waar de r3-lijn al op de gemeten plek ligt (B: r3 (18-20,44),(21,43))
VAST={'L1':[(34,25),(35,26),(36,27),(37,28)],   # (33,25) zou met de bandrand (32-33,24-25) een 2x2-klont maken
      'B':[(16,42),(17,43),(18,44),(19,44),(20,44),(21,43),(22,42),(23,42),(24,42),(25,42),(26,42)],
      'D':[(15,52),(16,53),(17,53),(18,54),(19,54),(20,54),(21,54),(22,53),(23,52),(24,52),(25,51)]}  # D: r3 (16-17,53)
def raster(pts,naam=None):
    if naam in VAST: return VAST[naam]
    "1 px, 8-verbonden polylijn door de geprojecteerde punten"
    P=[n2s(*p) for p in pts]; out=[]
    for (a,b),(c,d) in zip(P,P[1:]):
        n=max(1,int(round(max(abs(c-a),abs(d-b))*4)))
        for t in range(n+1):
            q=(int(a+(c-a)*t/n),int(b+(d-b)*t/n))
            if not out or out[-1]!=q: out.append(q)
    ch=True
    while ch:
        ch=False
        for i in range(1,len(out)-1):
            a,b=out[i-1],out[i+1]
            if abs(a[0]-b[0])<=1 and abs(a[1]-b[1])<=1:
                del out[i]; ch=True; break
    return out
if __name__=='__main__':
    for k,v,_,_ in LIJNEN: print(k,raster(v))
