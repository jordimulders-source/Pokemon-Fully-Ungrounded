# r4: r3 bevroren buiten het potengebied; potengebied = de kale schrap-reductie (kaal_r3.txt, het model zelf)
# met alleen reparaties: omlijning dicht, glans aaneengesloten, ringen/klauwtjes op modelmaat.
import numpy as np
CH='.#kdgGLcChWwvpor'
kaal=np.loadtxt('kaal_r3.txt',dtype=int); r3=np.loadtxt('vlieg_r3.txt',dtype=int)[16:62,6:56]
H,W=kaal.shape
zone=np.zeros((H,W),bool); zone[23:,:39]=True; zone[30:,:]=True
g=[[CH[(kaal if zone[r,c] else r3)[r,c]] for c in range(W)] for r in range(H)]
REP=[]
def P(z,r,c,s):
    for k,ch in enumerate(s):
        if ch!=' ': assert zone[r,c+k],(r,c+k); g[r][c+k]=ch
    REP.append((z,r,c,s))
# --- poot 1: schuin vanonder het borststuk naar linksvoor (reductie), 2 px kabel, glans linksboven
P('p1',23,14,'#hc#'); P('p1',24,10,'###hc#'); P('p1',25,9,'#hhhc##'); P('p1',26,8,'#hccc#')
P('p1',27,7,'.#hcc#')
P('p1',28,7,'.#hc#')
P('p1',29,7,'#WWW#'); P('p1',30,7,'#vvv#'); P('p1',31,7,'chc#')
for r in (34,35,36): P('p1',r,7,'chc#')
P('p1',37,5,'.chc#')
# --- poot 2: dunne kabel uit de reductie met glans links erbij
P('p2',25,15,'#hc#'); P('p2',26,14,'#hc#'); P('p2',27,13,'#hc#')
P('p2',28,12,'#WWW#'); P('p2',29,12,'#vvv#')
for r in (30,31,32,33,34): P('p2',r,13,'#hc#')
P('p2',35,12,'#hc#')
# --- poot 3
P('p3',23,20,'#chc#'); P('p3',24,21,'#chc#'); P('p3',25,21,'#chc#'); P('p3',26,21,'#chc#')
P('p3',27,22,'#hc#'); P('p3',28,22,'#hc#'); P('p3',29,23,'#hc#'); P('p3',30,23,'#hc#')
P('p3',31,22,'#WWW#'); P('p3',32,22,'#vvv#')
for r in (33,34,35,36,37): P('p3',r,23,'#hc#')
for r in (38,39): P('p3',r,24,'#hc#')
for r in (40,41): P('p3',r,25,'#hc#')
# --- poot 4: boog (1 px zoals de reductie) vanonder het achterlijf, ring, schuin naar rechtsachter
P('p4',23,26,'###'); P('p4',24,26,'#hhhhC##'); P('p4',25,32,'hhC#'); P('p4',26,33,'hCc#')
P('p4',27,26,'##'); P('p4',27,34,'#hc#'); P('p4',28,34,'#hc#'); P('p4',29,27,'..###Gd#hc#k')
P('p4',30,34,'#WWW#'); P('p4',31,34,'#vvv#')
P('p4',32,35,'#hc#'); P('p4',33,35,'#hc#'); P('p4',34,35,'#chc#'); P('p4',35,36,'#chc#'); P('p4',36,36,'#chc#')
P('p4',37,37,'#chc#'); P('p4',38,38,'#chc#'); P('p4',39,39,'#hc#')
# --- resten van de reductie naast de verschoven kabelranden weg
for r,c in [(38,37),(39,38),(30,22),(30,27),(31,27),(32,27),(28,17),(29,17),(31,11),(35,16),(33,17),(34,17),(38,23),(39,23),(40,24),(41,24)]:
    P('rest',r,c,'.')
# --- klauwtjes: twee smalle koperpuntjes (licht o + donker r) vast aan het kabeleinde, modelrichting
P('kl1',38,2,'.#oo#o##.'); P('kl1',39,2,'#r###o#'); P('kl1',40,2,'.#.#r#.'); P('kl1',41,2,'....#..')
P('kl2',36,10,'#oor##'); P('kl2',37,10,'.##o#.'); P('kl2',38,10,'.#r#..'); P('kl2',39,11,'.#')
P('kl3',42,25,'#o#o##'); P('kl3',43,25,'.#r#o#'); P('kl3',44,26,'.#.#r#'); P('kl3',45,28,'..#.')
P('kl4',40,40,'##oo#'); P('kl4',41,41,'#o#r#'); P('kl4',42,42,'#r#.'); P('kl4',43,43,'#.')
open('r4_stap1.chr','w').write('\n'.join(''.join(r) for r in g)+'\n')
