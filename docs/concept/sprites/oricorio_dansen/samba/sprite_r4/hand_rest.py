# Handwerk rij 13-62 buiten de tooi: rechtervleugel (3 vingers + gele band + blauwe punten), kop (Pom-Pom-oog en -snavel), lijf
# (borstband, heupband, rokje met 4 gele hangers), linkervleugel, onderste rechterveren, poten (Baile). Afgelezen op modelzone.py-beelden.
# Volgorde: hand_tooi.py -> hand_rest.py -> hand2.txt
W1={13:[(49,"dd#")],14:[(48,"dab#")],15:[(48,"dab#")],16:[(48,"dab#"),(53,"dd#")],17:[(48,"dab#"),(52,"abb#")],
    18:[(49,"ab#"),(52,"abb#")],19:[(49,"ab#"),(52,"abc#")],20:[(48,"abb"),(51,"d"),(52,"abc#")],
    21:[(47,"abbc"),(51,"d"),(52,"abc"),(55,"#"),(56,"d#")],
    22:[(45,"d"),(46,"abbc"),(50,"d"),(51,"abc"),(54,"d"),(55,"ab"),(57,"#")],
    23:[(44,"d"),(45,"abbc"),(49,"d"),(50,"abc"),(53,"d"),(54,"abc"),(57,"#")],
    24:[(44,"d"),(45,"abbc"),(49,"d"),(50,"abc"),(53,"d"),(54,"bc"),(56,"#")]}
VL={25:[(44,"#dabcbyzccc#")],26:[(43,"dabbbbyyzcc#")],27:[(42,"dabbbbcyyyzBBC#")],28:[(41,"dabbbbcyyyzBBBC#")],
    29:[(41,"dabbbccyyyzBBC#")],30:[(38,"#d"),(40,"abbbbcyyyzBBC#")],31:[(38,"bb"),(40,"babbbcyyyz####")],
    32:[(38,"bb"),(40,"abbbcyyyyzBBC#")],33:[(37,"bbb"),(40,"bbbcyyyyzBBBC#")],34:[(38,"bb"),(40,"bbcyyyyzBB###")],
    35:[(38,"cb"),(40,"bcyyyyzBBC#")],36:[(38,"cc"),(40,"ccyzzcBBC#")],37:[(38,"cc"),(40,"dbbccBBC#")],38:[(38,"c"),(39,"##ccBBC##")],
    39:[(39,"######")]}
KOP={26:[(26,"d"),(27,"aaaaaa"),(33,"##"),(35,"bb"),(37,"#")],
     27:[(25,"d"),(26,"a"),(27,"rrr"),(30,"aa"),(32,"####"),(36,"b"),(37,"#")],
     28:[(25,"dr"),(27,"ppp"),(30,"r"),(31,"a"),(32,"#w##"),(36,"b"),(37,"#")],
     29:[(25,"r"),(26,"pppp"),(30,"r"),(31,"a"),(32,"#w##"),(36,"b"),(37,"#")],
     30:[(24,"r"),(25,"ppp"),(28,"##"),(30,"aaa"),(33,"##"),(35,"bb"),(37,"#")],
     31:[(24,"rpq#"),(28,"aaaaaabb"),(36,"c"),(37,"d")],
     32:[(24,"rp#"),(27,"aaaaabbb"),(35,"cc"),(37,"d")],
     33:[(24,"r#d"),(27,"abbbbbcc"),(35,"c"),(36,"d")]}
LIJF={34:[(25,"dyyybbbbyyyz"),(37,"#")],35:[(24,"dyyyyyyyyyyyz"),(37,"#")],36:[(24,"dyyyyyyyyyzzz"),(37,"#")],
      37:[(24,"dzzzzzzzzzzzz"),(37,"#")],38:[(25,"dzzbbbbbbzzc"),(37,"#")],39:[(25,"daaabbbbbccc"),(37,"#")],
      40:[(25,"daaabbbbbccc"),(37,"#")],41:[(25,"ddaabbbbbccc"),(37,"#")],42:[(25,"ddabbbbcyyyz"),(37,"z#")],
      43:[(25,"ddyyyyyyyyyyyz#")],44:[(25,"d#zzzzzzzzzzzz#")],45:[(25,"#ycyzbbbcyzcyz#")],46:[(25,"#zcyzbbcccyzcz#")],
      47:[(26,"#czzbcccxxc#")],48:[(27,"#xxcccccc#")],49:[(28,"#########")]}
LV={35:[(23,"d")],36:[(22,"dd")],37:[(19,"dddd"),(23,"a")],38:[(7,"dddd"),(15,"dddd"),(19,"aaaa"),(23,"bc")],
    39:[(6,"d"),(7,"aaaa"),(11,"dddd"),(15,"d"),(16,"aaabbbbbc")],40:[(7,"#"),(8,"aaaaaaa"),(15,"d"),(16,"bbccccccc")],
    41:[(8,"##"),(10,"aaaab"),(15,"dccccccccc")],42:[(9,"dd"),(11,"###"),(14,"c"),(15,"xyyyyxxyyz")],
    43:[(8,"d"),(9,"aaaaa"),(14,"cx"),(16,"zyyyx"),(21,"yyz"),(24,"c")],44:[(8,"#"),(9,"aaaab"),(14,"cc"),(16,"xyyyyxzz"),(24,"c")],
    45:[(9,"######"),(15,"ccc"),(18,"zzzz"),(22,"#"),(23,"BC")],46:[(11,"dd"),(13,"aaa"),(16,"d"),(17,"ccccc"),(22,"#"),(23,"C#")],
    47:[(11,"d"),(12,"aaaa"),(16,"#"),(17,"BBc"),(20,"#")],48:[(11,"#bbb#"),(16,"BBC#")],49:[(12,"####"),(16,"###")]}
OR={41:[(38,"#")],42:[(38,"#"),(39,"#dd")],43:[(39,"dbb"),(42,"ddd")],44:[(39,"dbbbbb"),(45,"dd")],45:[(39,"#bbbbbb"),(46,"BBB#")],
    46:[(39,"#ccccccBBBC#")],47:[(40,"#ddddcc"),(47,"BBC#")],48:[(41,"#bbbb"),(46,"BBBC#")],49:[(42,"##cc"),(46,"CCCC#")],50:[(44,"######")]}
POOT={50:[(27,"rppppp#"),(35,"rp#")],51:[(25,"rpp#####"),(35,"rp#")],52:[(26,"rr#"),(34,"rp#")],53:[(24,"rrppr#"),(34,"rp#")],
      54:[(23,"#pppqq#"),(34,"rp#")],55:[(23,"#######"),(33,"rp#")]}
# Baile-voet (frame 1, rij 56-61, kol 20-34) met DX=+5 (bovenkant sluit aan op het scheenbeen)
BAILE=['.......bdd3....','......bdddd3...','....bbddede3...','...bdeddbd3....','...331d36d3....','.....33.33.....']
BM={'b':'r','d':'p','e':'q','3':'#','1':'r','6':'#'}
for i,row in enumerate(BAILE):
    POOT.setdefault(56+i,[])
    for j,ch in enumerate(row):
        if ch!='.': POOT[56+i].append((20+j+5,BM[ch]))
rows=[list(r) for r in open('hand1.txt').read().split('\n')[:64]]
for r in range(13,25):
    for c in range(49,60): rows[r][c]='.'
for r in range(26,64):
    for c in range(0,64): rows[r][c]='.'
for c in range(44,60): rows[25][c]='.'
for T in (W1,VL,LV,KOP,LIJF,OR,POOT):
    for r,segs in T.items():
        for c0,s in segs:
            for i,ch in enumerate(s): rows[r][c0+i]=ch
open('hand2.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
