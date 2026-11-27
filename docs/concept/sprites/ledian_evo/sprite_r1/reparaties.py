# Technische reparaties op de kale reductie k (64x64). Alleen buitenrand: geen lichte kleur op de buitenlijn.
# - rood (8 b0 / 9 e5 / 10 f4) op de buitenrand -> 7 (donkerrood selout, modelkleur van de vleugelrand)
# - vuistgrijs (4 a0 / 5 c3 / 6 wit) op de buitenrand -> 3 (grijs 64, modelkleur)
for y in range(64):
    for x in range(64):
        v=k[y,x]
        if v==0: continue
        nb=[k[Y,X] if 0<=Y<64 and 0<=X<64 else 0 for Y,X in((y+1,x),(y-1,x),(y,x+1),(y,x-1))]
        if 0 not in nb: continue
        if v in (8,9,10): REPARATIES.append((y,x,7,'rode buitenrand -> selout donkerrood'))
        elif v in (4,5,6): REPARATIES.append((y,x,3,'lichte vuistrand -> grijs 64'))
