# === ZONE OGEN (toegestane afwijking: groter en lichter) ===
# oude kozijnen terug naar steen
hl('a',37,14,16); put('+',[(15,36)]); vl('a',14,38,41); vl('a',16,38,41); hl('a',41,14,16)
vl('a',22,38,41); vl('a',25,38,41); hl('a',42,23,25); hl('a',41,22,25)
for x0 in (13,22):
    hl('+',38,x0,x0+3); hl('+',42,x0,x0+3); vl('+',x0,38,42); vl('+',x0+3,38,42)
    vl('p',x0+1,39,41); vl('o',x0+2,39,41)
# === ZONE DEUR + LATEI ===
put('a',[(14,43)])
hl('b',44,8,9) if False else None
hl('+',44,13,22); put('b',[(23,44)])
hl('+',45,23,25); vl('+',12,45,46)
hl('a',45,13,22); hl('b',46,13,22)
hl('+',47,13,21); put('c',[(22,47),(23,46),(24,46),(23,47),(24,47)])
vl('+',25,46,48); hl('+',48,22,24)
put('c',[(24,49),(24,50)]); put('+',[(25,49),(25,50)])
# === ZONE GEVELS ===
# bovenste linker gevel: raampje 1x2 (rij 14-15, model), rechterrand als lijn
put('a',[(31,13)]); put('+',[(36,12),(37,13)])
# onderste linker gevel: rechterrand (model (26.3,18.8)->(30.2,27))
put('+',[(26,19),(27,20),(27,21),(28,22),(28,23),(29,24),(29,25),(30,26)])
hl('+',27,27,29)
# onderste rechter gevel: linkerrand (34,19.6)->(30.3,27) en rechterrand (38.6,19.5)->(41,27)
put('+',[(33,20),(33,21),(32,22),(32,23),(31,24),(31,25)])
put('+',[(39,20),(39,21),(39,22),(39,23),(40,24),(40,25),(40,26)])
# === ZONE TERRASSEN RECHTS (lijnen die de reductie miste, gemeten op het model) ===
# bovenrand terrasvlak midden (model (38.6,29.2)->(53.6,25.4))
hl('+',28,40,41); hl('+',26,46,49)
# donker middenblok: bovenrand + linkerrand
hl('+',29,42,46); put('+',[(47,28)]); vl('+',40,30,37); vl('+',41,38,40)
# bovenrand onderste rechterblok (model (35.4,41.5)->(41.8,41.3)->(55,36.3))
hl('+',41,39,42); put('+',[(43,40),(44,40),(45,39),(46,39),(47,39),(48,38),(49,38),(50,38),(51,37),(52,37),(53,37),(54,36),(55,36)])
# rechterrand onderste blok (gemeten 58.3@37 -> 60.6@47), muurstrook erachter e
vl('+',58,37,39); vl('+',59,40,44); vl('+',60,45,48)
for y in range(38,40): put('e',[(59,y)])
for y in range(40,45): put('e',[(60,y)])
for y in range(45,49): put('e',[(61,y)])
# hoek voorvlak/zijvlak onderste blok (gemeten 41.9@45 -> 43.4@60)
vl('+',42,45,56); vl('+',43,57,60)
# grote voeg (doorlopende laag) op het zijvlak, gemeten 53.4@40 -> 43.1@59; korte losse voegen weg
for y in range(43,58):
    for x in range(44,59):
        if R[y][x]=='+': R[y][x]='d'
put('e',[(43,53),(44,52),(45,51),(46,51),(47,50),(48,50),(49,49),(50,48),(51,47),(52,47),(53,47),(54,46),(55,46),(56,45),(57,44),(58,44)])
put('+',[(40,53)])
# === lijnklonten weg ===
put('e',[(28,27),(29,27)])
put('+',[(24,36)]); put('b',[(24,37)])
hl('a',42,39,41)
# terrasbovenlijn niet onderbreken door mos; hoek boventerras (gemeten 48.4@11..48.2@13)
put('+',[(36,10)]); vl('+',48,11,15)
# kistje: bovenlijn recht (model 14.8), voorvlak licht, onderlijn tot 44
hl('+',14,37,44); hl('a',15,37,44); put('+',[(45,15)]); hl('b',16,37,44); hl('+',17,36,44)
# === ruis: tintclusters < 3 px opgaan in buren (niet: gevelrandjes, voeg, ogen) ===
import numpy as _np
C='.X+abcdemnopz'
keep={(34,20),(34,21),(33,22),(33,23),(19,23),(19,24),(40,29),(41,29),(43,53),(44,52),(45,51),(46,51),(47,50),(48,50),(49,49),(50,48),(51,47),(52,47),(53,47),(54,46),(55,46),(56,45),(57,44),(58,44)}
for it in range(3):
  G=[[C.index(ch) for ch in r] for r in R]; seen=set()
  for y in range(64):
    for x in range(64):
      v=G[y][x]
      if v<3 or v in (10,11,12) or (x,y) in seen: continue
      comp=[(x,y)]; st=[(x,y)]; seen.add((x,y))
      while st:
        px,py=st.pop()
        for qx,qy in ((px+1,py),(px-1,py),(px,py+1),(px,py-1)):
          if 0<=qx<64 and 0<=qy<64 and (qx,qy) not in seen and G[qy][qx]==v: seen.add((qx,qy)); comp.append((qx,qy)); st.append((qx,qy))
      if len(comp)<3 and not any(p in keep for p in comp):
        nb=[G[qy][qx] for px,py in comp for qx,qy in ((px+1,py),(px-1,py),(px,py+1),(px,py-1)) if 0<=qx<64 and 0<=qy<64 and G[qy][qx]>=3 and G[qy][qx] not in (10,11,12) and (qx,qy) not in comp]
        if nb:
          w=max(set(nb),key=nb.count)
          for px,py in comp: R[py][px]=C[w]
put('+',[(16,27)])
# dubbele lijn onder de buitenlijn weg (buitenlijn = model-silhouet)
put('a',[(36,10),(37,10),(16,27),(15,28),(16,28)])
# r2: bovenste rechtergevel linkerrand doorgetrokken (model 44.6@4 -> 43.2@9)
if R2: put('+',[(44,4),(44,5),(44,6)])
# === korte losse voegstompjes weg (te veel detail), ontbrekende pixel terrashoek ===
put('b',[(10,52),(11,52),(28,54),(29,54),(29,55),(29,56),(27,45),(28,45),(29,45)])
for p in [(38,59),(38,60)]: put('b' if R[p[1]][p[0]]=='+' else R[p[1]][p[0]],[p])
put('+',[(50,24)])
# === BUITENLIJN: selout aan de lichtkant (linksboven) in lijntint '+', schaduwkant zwart ===
import numpy as _np
M=_np.array([[ch!='.' for ch in r] for r in R])
for y in range(64):
  for x in range(64):
    if R[y][x]!='X': continue
    nx=ny=0
    for dy in (-1,0,1):
      for dx in (-1,0,1):
        yy,xx=y+dy,x+dx
        if not(0<=yy<64 and 0<=xx<64) or not M[yy,xx]: nx+=dx; ny+=dy
    if SELOUT and (nx+ny)<0 and ny<=0 and nx<=0: R[y][x]='+'
# === ZONE OGEN: modelgloed rond de ogen niet overnemen (geen glow): licht 'a' rond de ogen -> steen 'b' ===
for y in range(37,44):
  for x in range(10,22):
    if R[y][x]=='a': R[y][x]='b'
