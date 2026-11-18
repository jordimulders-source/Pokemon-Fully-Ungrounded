# Shuppetto r8: kleine reparatieronde op r7 (r7.npy = ../r7/cur.npy), punten = keuring_r7. Registratie: spritepixel (i,j)
# = modelblok x 24+(i-1)*S, y 1+(j-4)*S, S = 968/62. Elke reparatie overgenomen uit het model (mch/mpx); kleur naar Gen 3.
# python3 build.py -> cur.npy, banette_evo.png; python3 vel.py; python3 controle.py cur.npy; python3 diff.py
import numpy as np
g=np.load('r7.npy').copy(); LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows):
    put(name,[((x0+dx,y0+dy),KEY[ch]) for dy,row in enumerate(rows) for dx,ch in enumerate(row) if ch not in ' _'])
K=1; GL,GM,GD=2,3,4; CYAAN,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
KEY={'k':K,'l':GL,'m':GM,'d':GD,'c':CYAAN,'r':RM,'R':RD,'b':MOND,'y':GEEL,'L':BL,'M':BM,'B':BD,'w':WIT,'n':NAV,'e':RL,'.':0}

# 1/2. buitenlijn poppetjes dicht
put('1 lijn popR',[((57,53),K)])
put('2 lijn popL',[((13,56),K)])

# 3. steeknaad muts: model naad van de rand (36,6) schuin naar (42,12), donkerrood (R) in mch op (37-38,7),(38-39,8),(39,9),(40-41,10).
#    Losse R-pixels weg (grond = middenrood zoals het model); één diagonale lijn (36,6)->(39,9) in R die doorloopt in het
#    bestaande zwarte kruis (40-42,10-12); bovenste kruisje op de lijn rond (38,8) in dezelfde X-vorm.
pts=[]
for y in range(6,13):
    for x in range(35,42):
        if g[y,x]==RD and not (y==6 and x<=36): pts.append(((x,y),RM))
put('3 naad',pts)
put('3 naad',[((41,10),RM)])
put('3 naad',[(p,RD) for p in [(37,7),(38,8),(39,9),(39,7),(37,9)]])

# 4. grijze lap (24-33,46-49): model = grijze lap met lichte bovenkant, korte scheur onder de naad bij (29,47), zwarte onderrand.
grid('4 voet',24,47,[
#  456789012
  "_klllkmmm",   # 47  (25) k; lichte bovenkant 26-28; scheur (29,47) aan de naad; (32,47) grijs, grenst aan het rood
  "kmmmddddk",   # 48  middengrijs links, schaduw rechts; (32,48) k = grens met het rood
 ])

# 5/6. bellen: zelfde opbouw links en rechts (model: glans lichtgrijs linksboven, sleuf met staartje, schaduw rechtsonder)
BEL=["lllm","lmmd","lkkd","ddkd"]
grid('5 bel links',6,34,BEL)
grid('6 bel rechts',50,18,BEL)

# 7. ogen poppetjes: iris lichtblauw, één pupil binnen-onder (model donkerst op (6,46), (49,52), (54,52)); geen dambord
for x0,y0,px in [(5,45,6),(11,45,11),(48,51,49),(54,51,54)]:
    put('7 ogen',[((x0,y0),CYAAN),((x0+1,y0),CYAAN),((x0,y0+1),CYAAN),((x0+1,y0+1),CYAAN),((px,y0+1),NAV)])

# 8. losse pixel (29,15) -> middenrood (model r)
put('8 los',[((29,15),RM)])

# 9. glans muts: kleiner en ronder (2 boven, 3 onder)
put('9 glans',[(p,RM) for p in [(33,8),(33,10),(34,10)]]+[(p,RL) for p in [(34,8),(35,8),(33,9),(34,9),(35,9)]])

np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
for k,v in LOG.items(): print('%-16s %3d'%(k,v))
