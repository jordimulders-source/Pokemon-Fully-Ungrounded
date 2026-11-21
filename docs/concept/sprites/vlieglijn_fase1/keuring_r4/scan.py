from PIL import Image
import sys
s=Image.open(sys.argv[1]); a=[[s.getpixel((x,y)) for x in range(64)] for y in range(64)]
seen=set(); small=[]
for y in range(64):
  for x in range(64):
    v=a[y][x]
    if v==0 or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
      cx,cy=st.pop(); comp.append((cx,cy))
      for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny=cx+dx,cy+dy
        if 0<=nx<64 and 0<=ny<64 and (nx,ny) not in seen and a[ny][nx]==v:
          seen.add((nx,ny)); st.append((nx,ny))
    if len(comp)<3: small.append((v,comp))
for v,c in small: print('klein', v, c)
# losse omlijning: index1 zonder transparante buur (8-buren) en met <=1 buur van index 1
for y in range(1,63):
  for x in range(1,63):
    if a[y][x]!=1: continue
    nb=[a[y+dy][x+dx] for dx in(-1,0,1) for dy in(-1,0,1) if dx or dy]
    if 0 not in nb and nb.count(1)<=1: print('losse lijn',x,y)
# lichte kleur op buitenrand
for y in range(64):
  for x in range(64):
    v=a[y][x]
    if v in (0,1): continue
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
      nx,ny=x+dx,y+dy
      if not(0<=nx<64 and 0<=ny<64) or a[ny][nx]==0: print('rand',v,x,y); break
