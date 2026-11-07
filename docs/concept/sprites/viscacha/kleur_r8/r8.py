"""r8: alleen benoemde zones op r7 (raster_r7.txt): snorharen/gezicht, pluim, voorpoten, nabij oor."""
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r8/'
G=[list(l.rstrip('\n')) for l in open(D+'raster_r7.txt')][:64]
def seg(y,x,s):
    for i,c in enumerate(s):
        if c!=' ': G[y][x+i]=c
def pts(c,L):
    for x,y in L: G[y][x]=c
# 1a. snorharen nabij: wortel (6,36) gedeeld door boven en midden, onder vanaf de snuithoek
for y in range(34,44):
    for x in range(0,8):
        if G[y][x]=='F': G[y][x]='.'
pts('F',[(6,36),(5,35),(4,35),(3,36),(2,36),(1,36),(0,37)])          # boven
pts('F',[(5,37),(4,37),(3,38),(2,38),(1,39),(0,40)])                 # midden
pts('F',[(7,37),(6,38),(5,39),(5,40),(4,41),(3,42)])                 # onder
# 1b. snorharen ver: 2 lijnen, 1 px, crème/vacht ertussen; geen pixel op kin/mond/neus
seg(36,13,'55'); seg(37,14,'6'); seg(37,16,'66'); seg(38,16,'66'); seg(38,19,'4'); seg(39,15,'66')
pts('F',[(13,35),(14,35),(15,36),(16,36),(17,36),(18,37),(19,37),(20,38),(21,38),(22,39)])   # boven
pts('F',[(15,37),(16,38),(17,39),(18,39),(19,40),(20,41),(21,42),(22,43)])                   # onder
# 2. pluim: punten 1 px, meer bleek (A), smalle kerven
seg(14,58,'8.'); seg(16,53,'.')
seg(18,56,'A'); seg(19,56,'A'); seg(20,56,'A');  seg(21,57,'A')
seg(23,55,'AA'); G[19][54]='1'; G[24][51]='1'
# 3. voorpoten: twee teenlijntjes in middentint 3
seg(47,12,'25541'); seg(48,12,'25541'); seg(49,12,'23431'); seg(50,13,'111')
G[47][16]='1'; G[47][17]='1'
seg(48,20,'255541'); seg(49,20,'255541'); seg(50,20,'253531'); seg(51,20,'243431'); seg(52,21,'1111')
# 4. nabij oor: brede ronde top (r17 x21-26), linkerrand x20 op r18
seg(17,21,'225551'); seg(18,20,'255114')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
