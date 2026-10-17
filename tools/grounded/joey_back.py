# Project Grounded: Joey's rugsprite (partner tegen Gabby & Ty), Red's FRLG-rugsprite omgekleurd: blauwe pet en rugzak, geel shirt.
# Draaien vanuit de repo-root: python3 tools/grounded/joey_back.py graphics/trainers/back_pics
from PIL import Image
import sys
SP=sys.argv[1]
r=Image.open('graphics/trainers/back_pics/red.png')
W,H=r.size; px=r.load()
REDS={11,12,8}
out=r.copy(); o=out.load()
for f in range(H//64):
    seen=set(); comps=[]
    for y in range(f*64,f*64+64):
        for x in range(W):
            if px[x,y] in REDS and (x,y) not in seen:
                st=[(x,y)]; seen.add((x,y)); c=[]
                while st:
                    a,b=st.pop(); c.append((a,b))
                    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                        n=(a+dx,b+dy)
                        if 0<=n[0]<W and f*64<=n[1]<f*64+64 and n not in seen and px[n] in REDS:
                            seen.add(n); st.append(n)
                comps.append(c)
    cap=max(comps,key=lambda c:(len(c)>40, -min(p[1] for p in c)))
    # cap = largest component that starts highest
    comps.sort(key=lambda c:min(p[1] for p in c))
    cap=[c for c in comps if len(c)>30][0]
    capset=set(cap)
    capy=max(p[1] for p in cap)
    wh=[y for y in range(f*64,f*64+64) for x in range(W) if px[x,y] in (9,10) and y>capy]
    collar=min(wh) if wh else capy+8
    for y in range(f*64,f*64+64):
        for x in range(W):
            v=px[x,y]
            if (x,y) in capset:
                o[x,y]={11:13,12:14,8:6}[v]   # pet: blauw
            elif v==8 and y<collar:
                pass                          # haar (donker)
            elif v==8:
                o[x,y]=1                      # schaduw van het shirt
            elif v in (5,6) and y>capy:
                o[x,y]={5:11,6:12}[v]         # mouwen: geel shirt
pal=r.getpalette()[:48]
def s(i,c): pal[3*i:3*i+3]=c
s(13,[98,164,222]); s(14,[49,123,156]); s(6,[41,57,98])     # blauw (pet), 6 = donkerblauw
s(11,[255,222,65]); s(12,[222,172,90]); s(1,[164,115,41]); s(8,[49,41,49])   # geel shirt
s(4,[82,65,65])                                             # donker haar
out.putpalette(pal+[0]*(768-48))
out.save(SP+"/joey.png")
