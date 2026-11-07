# opschonen: clusters < 3 px van vlaktinten opgaan in de meest voorkomende vlaktint ernaast
from collections import Counter
VL=set('56789A')
Zs=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
GL={(28,35),(29,35),(27,36),(28,36),(17,34),(17,35),(28,34),(29,34),(27,35),(28,35)}
KOP=set((x,y) for y in range(31,43) for x in range(14,39))   # handgetekend gezicht: niet aanraken
def comps():
    seen=set(); out=[]
    for y in range(64):
        for x in range(64):
            c=r[y][x]
            if c not in VL or (x,y) in seen or (x,y) in Zs: continue
            st=[(x,y)]; cp=[]; seen.add((x,y))
            while st:
                p=st.pop(); cp.append(p)
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+dx,p[1]+dy)
                    if 0<=q[0]<64 and 0<=q[1]<64 and q not in seen and r[q[1]][q[0]]==c: seen.add(q); st.append(q)
            out.append(cp)
    return out
for it in range(8):
    ch=0
    for cp in comps():
        if len(cp)>=3 or set(cp)<=GL or set(cp)&KOP: continue
        if any(any(not (0<=x+dx<64 and 0<=y+dy<64) or r[y+dy][x+dx]=='.' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for x,y in cp): continue
        cnt=Counter()
        for (x,y) in cp:
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                q=(x+dx,y+dy)
                if 0<=q[0]<64 and 0<=q[1]<64 and q not in cp and r[q[1]][q[0]] in VL: cnt[r[q[1]][q[0]]]+=1
        if cnt:
            c=cnt.most_common(1)[0][0]
            for (x,y) in cp: r[y][x]=c
            ch+=1
    if not ch: break
