"""r9: rugtop (r28-32, x30-42) boller; basis kleur_r8/raster.txt. Rest bevroren."""
V='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
R=[list(l.rstrip('\n')) for l in open(V+'kleur_r8/raster.txt')][:64]
def put(y,x0,s):
    for i,c in enumerate(s): R[y][x0+i]=c
# nieuwe boog: runs 2 (r30 x30-31) - 3 (r29 x32-34) - 4 (r28 x35-38, top) - 2 (r29 x39-40); rechterflank (r30-33) = r8
put(28,35,'2222')           # selout top
put(29,32,'222'); put(29,35,'5555')
put(30,32,'5'); put(30,38,'55')   # x38 (selout) en x39 (dubbele hoekpixel) worden lijf
open(V+'kleur_r9/raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')

# ---- uitbreiding r9 (Jordi: "perfect, doe maar"): kleur- en schaduwronde ----
R=[list(l.rstrip('\n')) for l in open(V+'kleur_r9/raster.txt')][:64]
def put(y,x0,s):
    for i,c in enumerate(s): R[y][x0+i]=c
# 0. paletplek: B (bruin donker 122,84,46) samengevoegd met 2 (selout); B wordt hooglicht
for y in range(64):
    for x in range(64):
        if R[y][x]=='B': R[y][x]='2'
# 2. hooglicht B: rugboog en voorhoofd (lens, linksboven)
put(29,35,'BBB'); put(30,33,'BBBBB'); put(31,33,'BBB')
put(27,12,'BBBB'); put(28,11,'BBBB'); put(29,11,'BB')
# 3. staart: licht links/boven (4), basis C, schaduw rechts/onder (2), selout 2 links
for y,s in [(23,'44'),(24,'44C'),(25,'44C'),(26,'44C'),(27,'44CC')]: put(y,53,s)
T={28:(51,'444CC2'),29:(51,'444CC2'),30:(52,'444CC2'),31:(52,'444CC2'),32:(53,'444CCC2'),
   33:(54,'444CC2'),34:(55,'444CC2'),35:(55,'444CC2'),36:(56,'44CC2'),37:(56,'44CC2'),
   38:(57,'44C2'),39:(57,'44C2'),40:(56,'44CC2'),41:(56,'44CC2'),42:(56,'44CC2'),
   43:(55,'44CC2'),44:(55,'44CC2'),45:(54,'44CC2'),46:(53,'44CC2'),47:(51,'444CC2')}
for y,(L,s) in T.items():
    R[y][L]='2'; put(y,L+1,s)
R[31][60]='2'                        # rechterlok: schaduwkant
put(46,52,'2'); put(47,49,'22')      # selout bovenrand van de bocht
put(48,48,'CCCCCCC'); put(48,55,'22')
# 4. verre voorpoot een tint donkerder (vorm en teenlijntjes blijven)
put(44,15,'EE'); put(45,14,'EEEE'); put(46,13,'443EEE'); put(47,13,'443'); put(48,13,'443'); put(49,13,'E3E')
# 5. bil: een sikkel in 4 (breder naar onder), onderaan een wig 3; geen 1px-laagjes
S={33:(42,2),34:(43,2),35:(43,2),36:(43,2),37:(43,3),38:(43,3),39:(43,4),40:(43,4),
   41:(44,4),42:(44,4),43:(43,5),44:(44,5),45:(43,5),46:(43,5),47:(43,4)}
for y,(x0,w) in S.items():
    put(y,x0,'4'*w)
R[41][43]="5"
put(45,47,'3'); put(46,46,'33'); put(47,45,'33')
open(V+'kleur_r9/raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
