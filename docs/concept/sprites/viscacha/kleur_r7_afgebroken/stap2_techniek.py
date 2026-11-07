"""Stap 2 r7: alleen technisch opschonen van onderlaag.txt -> stap2.txt.
a) buitenlijn: elke randpixel (4-buur transparant) die geen lijnkleur is -> lijn: rand aan boven/links = selout van de groep (lijf 2, geel 8, creme F, staartbruin B), anders 1.
b) tintvlakjes < 3 px (vlaktinten 3-7,9,A,C) samenvoegen met de meest voorkomende vlaktint ernaast (lijnpixels blijven staan: featurelijnen).
De snorhaar- en rafelpixels ('+' in het masker) blijven B."""
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/'
r=[list(l.rstrip('\n')) for l in open(D+'onderlaag.txt')][:64]
sil=[l.rstrip('\n') for l in open(D+'silhouet_r7.txt')][:64]
LIJN=set('128BF'); VLAK=set('345679AC')
GROEP={'3':'2','4':'2','5':'2','6':'F','7':'F','8':'8','9':'8','A':'8','C':'B','B':'B','F':'F','2':'2','1':'2'}
o=[l[:] for l in r]
at=lambda x,y: r[y][x] if 0<=x<64 and 0<=y<64 else '.'
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c=='.' or sil[y][x]=='+' or c in '128': continue
        up,lf,dn,rt=at(x,y-1)=='.',at(x-1,y)=='.',at(x,y+1)=='.',at(x+1,y)=='.'
        if not (up or lf or dn or rt): continue
        if c in 'BF':   # grijze randmenging: groep van de binnenburen
            nb=[o[yy][xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=xx<64 and 0<=yy<64 and o[yy][xx] in VLAK]
            if not nb: continue
            c=max(set(nb),key=nb.count)
        r[y][x]=GROEP[c] if (up or lf) and not (dn or rt) else ('1' if (dn or rt) and not (up or lf) else GROEP[c] if up else '1')
for it in range(4):
    seen=set(); ch=0
    for y in range(64):
        for x in range(64):
            c=r[y][x]
            if c not in VLAK or (x,y) in seen: continue
            st=[(x,y)]; comp=[]; seen.add((x,y))
            while st:
                u,v=st.pop(); comp.append((u,v))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(u+dx,v+dy)
                    if at(*q)==c and q not in seen: seen.add(q); st.append(q)
            if len(comp)<3:
                cnt={}
                for u,v in comp:
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        n=at(u+dx,v+dy)
                        if n in VLAK and n!=c: cnt[n]=cnt.get(n,0)+1
                if cnt:
                    n=max(cnt,key=cnt.get)
                    for u,v in comp: r[v][u]=n
                    ch+=1
    if not ch: break
open(D+'stap2.txt','w').write('\n'.join(''.join(l) for l in r)+'\n')
