# Handwerk tooi (rij 2-27, kol 14-48): lijnen tussen de veren op de modelplekken (afgelezen op modelzone.py-beelden, 28x),
# vulling per veer: lichte helft links/boven (a/b), donkere helft rechts/onder (c), gele punten y/z. Rest van de rij blijft stap3.
# Letters: . transparant, # zwart, d G4 (donkergroene lijn), x Y3 (donkergele lijn), a/b/c groen licht/midden/schaduw, y/z geel licht/schaduw
SEG={
2:[(31,"d#")],
3:[(30,"dyy#")],
4:[(23,"dd#"),(30,"dyyy#"),(40,"dd#")],
5:[(23,"dyy#"),(29,"dyyyz#"),(38,"dyyy#")],
6:[(23,"dyz#"),(29,"dyyyz#"),(37,"dyyyz#")],
7:[(23,"dyzc#"),(29,"dyyzc#"),(36,"dbyyyz#")],
8:[(23,"dazc#"),(29,"dazcc#"),(36,"dbbyz#")],
9:[(23,"dabccd"),(29,"abbccd"),(35,"abbcc#")],
10:[(17,"dddd"),(23,"dabccd"),(29,"abbccd"),(35,"abbc#"),(43,"ddddd#")],
11:[(17,"dyyz"),(21,"dd"),(23,"dabccd"),(29,"abbccd"),(35,"abccd"),(40,"ddd"),(43,"byyyz#")],
12:[(17,"dyybbbd"),(24,"abccd"),(29,"abbccd"),(35,"abcd"),(39,"dd"),(41,"bbbyyz#")],
13:[(18,"#zbbcc"),(24,"d"),(25,"bccd"),(29,"abbccd"),(35,"abcd"),(39,"abbbcc"),(45,"##")],
14:[(19,"##cccd"),(25,"bccd"),(29,"axxccd"),(35,"abcd"),(39,"bccc##")],
15:[(16,"dd"),(20,"#"),(21,"ccd"),(24,"xyx"),(27,"cd"),(29,"xyzx"),(33,"d"),(34,"bc"),(36,"xyyx"),(40,"bcc#"),(44,"#")],
16:[(15,"dyyd"),(21,"#cx"),(24,"yyzx"),(28,"xyyzzx"),(34,"xyyzx"),(39,"cc##")],
17:[(15,"dyyb"),(19,"dd"),(21,"x"),(22,"yyyzx"),(27,"x"),(28,"yyzz"),(32,"x"),(33,"yyyzx"),(38,"ddddd"),(43,"dddd"),(47,"#")],
18:[(15,"dyyzb"),(20,"xyyx"),(24,"yyzzx"),(29,"yyzz"),(33,"x"),(34,"yyzx"),(38,"yyyyx"),(43,"bbcc"),(46,"yz#")],
19:[(14,"dyyzbc"),(20,"xyyyyx"),(26,"yzx"),(29,"yyzz"),(33,"xyzx"),(37,"yyyyyzx"),(44,"cc"),(46,"zcd")],
20:[(15,"#zbcc"),(20,"xyyyzzx"),(27,"yzx"),(29,"yyzz"),(33,"xyzx"),(37,"yyyzzz"),(43,"x"),(44,"ccc#")],
21:[(16,"##ccx"),(21,"yzzz"),(25,"xyzx"),(29,"yyzz"),(33,"xzx"),(36,"xyzzzz"),(42,"xx"),(44,"#"),(45,"c#")],
22:[(18,"##"),(20,"xyyyx"),(25,"xzx"),(28,"xyyzzx"),(34,"zx"),(36,"xxxyyyx"),(43,"#")],
23:[(18,"xyyyyyzx"),(26,"xx"),(28,"xyzzx"),(33,"#"),(34,"x"),(35,"xyyyyyyzx"),(44,"#")],
24:[(17,"xyyyyyzzzx"),(27,"#"),(28,"#xzx#"),(33,"##"),(35,"xyyyyyzzzx"),(45,"#")],
25:[(17,"#zzzzzzz#"),(26,"##"),(28,"aa"),(30,"#"),(31,"a"),(32,"aa"),(34,"##"),(36,"#zzzzzzz#")],
26:[(18,"########"),(37,"########")],
}
import numpy as np, sys
rows=open('stap3.txt').read().split('\n')[:64]; rows=[list(r) for r in rows]
for r,segs in SEG.items():
    for c in range(14,49): rows[r][c]='.'
    for c0,s in segs:
        for i,ch in enumerate(s): rows[r][c0+i]=ch
open('hand1.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
