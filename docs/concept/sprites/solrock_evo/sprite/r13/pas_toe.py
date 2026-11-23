# Ronde 13: barsten in de plaat een stap lichter (Jordi: "barsten iets lichter").
# - barst (9) in het lichte vlak (meeste buren 7/5) -> 8; in de schaduw (buren 8) blijft 9
# - Y-barst bovenaan in 10 -> 9; lidcontouren (10) rond de ogen blijven
from PIL import Image
im=Image.open('r12/sprite.png'); px=im.load(); src=im.copy().load()
n=[]
for y in range(21,46):
    for x in range(13,38):
        if src[x,y]==9:
            b=[src[x+dx,y+dy] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
            if sum(v in (5,7) for v in b)>=sum(v==8 for v in b) and any(v in (5,7) for v in b):
                px[x,y]=8; n.append((x,y))
for p in [(26,23),(25,24),(24,25),(21,26),(22,26)]: px[p]=9
im.save('r13/sprite.png',transparency=0)
print('9->8:',n)
