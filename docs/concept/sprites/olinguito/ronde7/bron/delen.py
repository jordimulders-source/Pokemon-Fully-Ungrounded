"""Olinguito ronde 7: met de hand per lichaamsdeel, elk deel als pixelregels (rij, kolom, tekens).
Latere delen liggen vóór eerdere. Er wordt niets berekend: geen vormen, schaduw of omlijning."""
import sys

PAL = """. 98c890 transparant
a ffb870 oranje hooglicht
O e08a3a oranje basis
p b05a1c oranje schaduw
P 74340c oranje omlijning (lichtkant)
n 8a5434 bruin hooglicht
N 5c3424 bruin basis
B 3c2018 bruin schaduw
c fffaea creme hooglicht (ook klauwen)
C f8e0a8 creme basis
q d4a868 creme schaduw / creme omlijning lichtkant
Y f8c818 oog geel
y b88000 oog donkergeel
w ffffff glans, hoektand
# 201010 omlijning
FRAME2 30"""

W, H = 40, 46
G = [['.'] * W for _ in range(H)]


def put(r, c, s):
    for i, ch in enumerate(s):
        if ch != ' ':
            G[r][c + i] = ch


# 1. staart (achter alles): schacht met ringen en de haak bovenaan
put(0, 25, "PPPPPP#")
put(1, 23, "PPaaaaOOO##")
put(2, 22, "PaOOOpppaOOp#")
put(3, 21, "PnNN#####aOOp#")
put(4, 21, "#nNB#"); put(4, 29, "PaOOp#")
put(5, 21, "#nB#");  put(5, 29, "NnNNB#")
put(6, 21, "#N#");   put(6, 29, "NnNNB#")
put(7, 22, "#");     put(7, 29, "PaOOp#")
for r in (8, 9, 10):
    put(r, 29, "PaOOp#")
for r in (11, 12):
    put(r, 29, "NnNNB#")
for r in (13, 14, 15):
    put(r, 29, "PaOOp#")
for r in (16, 17, 18):
    put(r, 29, "NnNNB#")
for r in (19, 20, 21, 22):
    put(r, 29, "PaOOp#")
for r in (23, 24, 25):
    put(r, 29, "NnNNB#")
for r in (26, 27, 28, 29):
    put(r, 29, "PaOOp#")
for r in (30, 31, 32, 33):
    put(r, 29, "NnNNNB#")
put(34, 29, "PaOOOp#")
put(35, 29, "PaOOOp#")
put(36, 28, "PaOOOOp#")
put(37, 28, "aOOOOOp#")
put(38, 27, "OOOOOOp#")
put(39, 25, "OOOOOpp##")
put(40, 24, "######")

# 2. lijf (peervorm), buik creme, dij rechts
put(25, 9, "##############")
put(26, 8, "#pppppppppppppp#")
put(27, 7, "P" + "aappppppppppppp" + "p#")
put(28, 7, "P" + "aaOOOOOOOOOOOOOp" + "#")
put(29, 6, "P" + "aaaOOOOOOOOOOOOOOp" + "#")
put(30, 6, "P" + "aacCCCCCCCOOOOOOOp" + "#")
put(31, 6, "P" + "acCCCCCCCCCOOOOOOOp" + "#")
put(32, 6, "P" + "acCCCCCCCCCOOOOOOpp" + "#")
put(33, 5, "P" + "aacCCCCCCCCC" + "OO" + "P" + "aOOOpp" + "#")
put(34, 5, "P" + "acCCCCCCCCCCO" + "P" + "aOOOOpp" + "#")
put(35, 5, "P" + "acCCCCCCCCCC" + "P" + "aOOOOOpp" + "#")
put(36, 5, "P" + "aCCCCCCCCCCq" + "P" + "aOOOOOpp" + "#")
put(37, 6, "P" + "CCCCCCCCCq" + "P" + "aOOOOOOpp" + "#")
put(38, 6, "#" + "qCCCCCCCqq" + "P" + "OOOOOOOpp" + "#")
put(39, 7, "#" + "qqqCCqqq" + "#" + "pOOOOOOpp" + "#")
put(40, 8, "#" + "qqqqqq" + "#" + "pppppppp" + "##")

# 3. voeten
put(41, 6, "#nnNNNNB#");   put(41, 17, "#nNNNNNNB#")
put(42, 5, "#nNN#NNNNB#"); put(42, 17, "#NNN#NNNBB#")
put(43, 5, "#NNNNNNNBB#"); put(43, 17, "#BNNNNNBBB#")
put(44, 6, "#########");   put(44, 18, "#########")

# 4. oren (achter de kop)
put(5, 4, "PPP")
put(6, 3, "PaOO#")
put(7, 2, "PaCCq#")
put(8, 2, "PaCqp#")
put(9, 2, "Paqp#")
put(4, 16, "PPP#")
put(5, 15, "PaOOp#")
put(6, 15, "PaCCp#")
put(7, 15, "PCqqp#")
put(8, 15, "PaOOp#")

# 5. kop: rond, recht overeind
put(8, 8, "PPPPPPPP")
put(9, 6, "PPaaaaaaOOPP")
put(10, 5, "P" + "aaaaaaaOOOOO" + "P")
put(11, 4, "P" + "aaaaaaOOOOOOOO" + "#")
put(12, 3, "P" + "aaaaaOOOOOOOOOOp" + "#")
put(13, 3, "P" + "aaaaOOOOOOOOOOOp" + "#")
put(14, 2, "P" + "aaaOOOOOOOOOOOOOpp" + "#")
# masker: horizontale band, rechte bovenrand
put(15, 2, "N" + "nnnNNNNNNNNNNNNNNB" + "#")
put(16, 2, "N" + "nN" + "NYY" + "NNNNN" + "NYYN" + "NNN" + "B" + "#")
put(17, 2, "N" + "nN" + "Yw#" + "NNNNN" + "YYw#" + "NNN" + "B" + "#")
put(18, 2, "N" + "nN" + "Ny#" + "NNNNN" + "YY#y" + "NNN" + "B" + "#")
put(19, 2, "N" + "NN" + "NNN" + "NNNNN" + "NyyN" + "NNB" + "B" + "#")
put(20, 2, "P" + "aaOOOOOOOOOOOOOOpp" + "#")
# snuit met neus, mond en hoektand
put(21, 0, "#n" + "qqqqq" + "OOOOOOOOOOOOpp" + "#")
put(22, 0, "##" + "cCCCCq" + "OOOOOOOOOOpp" + "#")
put(23, 0, "q" + "cCCCCqq" + "OOOOOOOOOpp" + "#")
put(24, 1, "#" + "C##CCq" + "pOOOOOOOpp" + "#")
put(25, 2, "#w####" + "ppOOOOpp" + "##")
put(26, 3, "#")
put(26, 8, "########")

# 6. voorpoot met drie lange klauwen (één groep), vóór de borst
# klauwen zonder omlijning aan de lichtkant (pseudo-omlijning, gids): licht c, schaduwkant q + zwart
put(26, 6, "c");    put(26, 11, "c#")
put(27, 6, "c#");   put(27, 11, "c#");  put(27, 16, "c#")
put(28, 7, "c#");   put(28, 11, "cq#"); put(28, 15, "c#")
put(29, 7, "cq#");  put(29, 11, "cq#"); put(29, 14, "cq#")
put(30, 8, "cq#");  put(30, 11, "cq#"); put(30, 14, "cq#")
# poot (handpalm) waar de klauwen uit komen
put(31, 8, "#nnNNNNNB#")
put(32, 7, "#nNNNNNNNB#")
put(33, 7, "#NNNNNNNBB#")
put(34, 8, "#########")

out = sys.argv[1]
with open(out, 'w') as f:
    f.write(PAL + '\n\n' + '\n'.join(''.join(r) for r in G) + '\n')
