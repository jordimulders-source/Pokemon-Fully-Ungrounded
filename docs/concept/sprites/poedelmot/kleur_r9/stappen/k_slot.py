from collections import Counter
VL='67A'
for it in range(3):
    seen=set()
    for y in range(64):
        for x in range(64):
            c=r[y][x]
            if c not in VL or (x,y) in seen: continue
            st=[(x,y)]; comp=[]; seen.add((x,y))
            while st:
                p=st.pop(); comp.append(p)
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+dx,p[1]+dy)
                    if 0<=q[0]<64 and 0<=q[1]<64 and q not in seen and r[q[1]][q[0]]==c: seen.add(q); st.append(q)
            if len(comp)>=3 or (27,34) in comp or (17,34) in comp: continue
            cnt=Counter()
            for a,b in comp:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(a+dx,b+dy)
                    if q not in comp and r[q[1]][q[0]]!='.': cnt[r[q[1]][q[0]]]+=1
            if cnt:
                n=cnt.most_common(1)[0][0]
                for a,b in comp: r[b][a]=n
