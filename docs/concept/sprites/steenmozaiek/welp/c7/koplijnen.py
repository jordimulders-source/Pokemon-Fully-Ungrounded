# Koplijnen c6: drie varianten, elk één idee. Coordinaten (x,y) van de groef (tint 2), lip direct onder/rechts
# (14 op licht vlak, 5 op midden/donker), geen lip tussen groeven op 1 px. Gezicht (oog/neus/mond) niet geraakt.
# Voorhoofd eerst rustig gemaakt (één licht vlak x12-20, 4 x21-22, schaduw 3 x23-24, rij 21-24), zodat de lijnen niet
# met toonovergangen verward worden. Kop: ver oog x11-13, nabij oog x17-21 (bovenlid rij 26), oren x11-15 en x25-30.
VOORHOOFD={y:[(12,'555555555'),(21,'44'),(23,'33')] for y in (21,22,23,24)}
VAR={
 # a: Chavin-wenkbrauwvoluut: boog over het nabije oog die achteraan omhoog krult, korte boog boven het verre oog,
 #    en één rechte middenlijn van de neusrug naar de kruin.
 'a': [(17,24),(18,23),(19,23),(20,23),(21,23),(22,22),(22,21),(21,21),
       (12,24),(13,24),
       (15,24),(15,23),(15,22),(15,21)],
 # b: symmetrisch kruinmotief: een U vanaf de neusrug omhoog naar de kruin tussen de oren, plus een korte boog boven het nabije oog.
 'b': [(14,23),(14,22),(14,21),(15,24),(16,24),(17,23),(17,22),(17,21),
       (19,23),(20,23),(21,23),(22,24)],
 # c: naar de foto: één voluut boven het nabije oog; de buitenlijn loopt naar voren uit als wenkbrauw, de krul draait naar binnen.
 'c': [(16,24),(17,24),(18,24),(19,24),(20,24),(21,23),(21,22),(20,21),(19,21),(18,22)],
}
