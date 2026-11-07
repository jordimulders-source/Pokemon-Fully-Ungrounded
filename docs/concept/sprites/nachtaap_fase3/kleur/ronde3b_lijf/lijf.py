# Ronde 3b lijf: vanaf ronde3_lijf; handmatige toontabel per rij.
from PIL import Image
src=Image.open('../ronde3_lijf/nachtaap_fase3.png'); s1=Image.open('../ronde1s/nachtaap_fase3.png')
P=src.load(); Q=s1.load()
W=[['.' if P[x,y]==0 else '%X'%P[x,y] for x in range(64)] for y in range(64)]
def S(y,*spans):
    for sp in spans:
        if len(sp)==2: x0,c=sp; x1=x0
        else: x0,x1,c=sp
        for x in range(x0,x1+1):
            assert W[y][x] in '12345',(x,y,W[y][x]); W[y][x]=c
# 4. vuistarm terug naar 1s (vuist, pols, arm tot de schouder)
for y in range(14,31):
    for x in range(0,26): W[y][x]='.' if Q[x,y]==0 else '%X'%Q[x,y]
for x in range(19,23): W[31][x]='%X'%Q[x,31]
# 1+2. lichte kern linksboven (gebogen grens), bovenarm healer als eigen vorm
S(31,(23,34,'5'),(35,38,'4'))
S(32,(21,33,'5'),(34,39,'4'))
S(33,(21,32,'5'),(33,39,'4'))
S(34,(21,24,'5'),(25,26,'4'),(27,31,'5'),(32,40,'4'))
S(35,(22,24,'5'),(25,26,'4'),(27,30,'5'),(31,40,'4'))
S(36,(22,24,'5'),(25,26,'4'),(27,29,'5'),(30,40,'4'))
S(37,(22,24,'5'),(25,26,'4'),(27,28,'5'),(29,39,'4'))
S(38,(22,23,'5'),(24,25,'4'),(26,'3'),(27,39,'4'))
S(39,(22,23,'5'),(24,25,'4'),(26,'3'),(27,38,'4'))
S(40,(22,23,'5'),(24,25,'4'),(26,'3'),(27,37,'4'))
S(41,(22,23,'5'),(24,25,'4'),(26,'3'),(27,'3'),(28,36,'4'))
S(42,(22,23,'5'),(24,26,'4'),(27,'3'),(28,35,'4'))
# 3. buik/dij lichter: basis zakt lager, 2 alleen aan de onderrand
S(43,(24,26,'4'),(27,28,'3'),(29,35,'4'),(36,44,'3'))
S(44,(24,26,'4'),(27,28,'3'),(29,34,'4'),(35,44,'3'))
S(45,(27,31,'3'),(32,35,'4'),(36,43,'3'))
S(46,(32,'3'),(33,35,'4'),(36,44,'3'))
S(47,(34,'3')); S(48,(35,'3')); S(49,(36,'3')); S(50,(37,'3')); S(51,(38,'3'))
im=Image.new('P',(64,64)); im.putpalette(src.getpalette())
im.putdata([0 if W[y][x]=='.' else int(W[y][x],16) for y in range(64) for x in range(64)])
im.save('nachtaap_fase3.png',transparency=0)
open('lijf.txt','w').write('\n'.join(''.join(r) for r in W)+'\n')
