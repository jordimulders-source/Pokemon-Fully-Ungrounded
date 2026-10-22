"""Frame 2 (actiepose): kop 1 px omhoog, pupillen wijd + mond open, nabije arm omhoog
met gespreide vingers (Psychic-gebaar), staartkrul hoger. Benen en verre arm als frame 1."""
import f1
ROWS = []
def R(y, x0, *pieces):
    ROWS.append((y, x0, ''.join(pieces)))

NE = {17: "..kkkkkk..", 18: ".kCCCCCCk.", 19: "kCBkkkBBCk", 20: "kBkwwkkBBk", 21: "kBkwkkkBBk",
      22: "kBkkkkkBBk", 23: "kAkkkkkBAk", 24: "kABkkkBAAk", 25: ".kAAAAAAk.", 26: "..kkkkkk.."}
FE = {17: "..kkkkk..", 18: ".kCCCCCk.", 19: "kCBkkBBCk", 20: "kBkwwkBBk", 21: "kBkwkkBBk",
      22: "kBkkkkBBk", 23: "kAkkkkBAk", 24: "kABkkBAAk", 25: ".kAAAAAk.", 26: "..kkkkk.."}

for y, x0, s in f1.ROWS:
    if y <= 32:
        if 18 <= y <= 25 and x0 == 16 and len(s) == 26:      # oogrij: wijde pupillen
            s = "4" + NE[y] + s[11:13] + FE[y] + s[22:]
        ROWS.append((y - 1, x0, s))
    else:
        ROWS.append((y, x0, s))
# mond open (rij 29/30 van frame 1 -> 28/29)
R(28, 25, "s", "k", "k", "k", "s")
R(29, 26, "k", "z", "k")
# lijf zonder nabije arm ervoor
R(32, 24, "0", "0", "4", "3", "3", "3", "3", "3", "3", "3", "3", "3", "k")
R(33, 23, "0", "0", "4", "1", "1", "2", "2", "2", "2", "2", "3", "3", "3", "k")
R(34, 22, "0", "0", "4", "1", "2", "x", "x", "2", "2", "2", "2", "2", "3", "3", "3", "k")
R(35, 21, "0", "0", "4", "1", "2", "2", "x", "x", "y", "y", "2", "2", "2", "3")
R(36, 20, "0", "0", "0", "4", "1", "2", "x", "x", "x", "y", "y", "y", "2", "2", "3")
R(37, 19, "0", "0", "0", "0", "4", "1", "x", "x", "x", "y", "y", "y", "y", "z", "2", "3", "3")
R(38, 18, "0", "0", "0", "0", "4", "1", "2", "x", "x", "y", "y", "y", "y", "y", "z", "2", "3", "3")
R(39, 18, "0", "0", "0", "0", "4", "1", "2", "x", "y", "y", "y", "y", "y", "y", "z", "2", "3", "3", "3")
R(40, 17, "0" * 5, "4", "2", "2", "y", "y", "y", "y", "y", "y", "y", "z", "2", "3", "3", "3")
R(41, 16, "0" * 6, "4", "2", "2", "y", "y", "y", "y", "y", "y", "z", "z", "3", "3", "3", "3")
# nabije knie (geen hand erop)
R(42, 15, "0", "0", "0", "0", "4" * 10)
R(43, 14, "0", "0", "0", "4", "1", "1", "1")
R(44, 14, "0", "0", "4", "1", "1", "1", "2")
R(45, 14, "0", "4", "1", "1", "2", "2", "2")
R(46, 14, "0", "4", "2", "2", "2", "2", "2")
R(47, 14, "0", "4", "2", "2", "2", "2", "2")

# hand omhoog met de hand (na de procedurele arm): x5..15
POST = [(y, 5, s) for y, s in (
    (14, "00000000000"),
    (15, "00000qr0000"),
    (16, "00000rs0qr0"),
    (17, "qr0002k0rs0"),
    (18, "rs0002k02k0"),
    (19, "02k002k2k00"),
    (20, "002k02k2k00"),
    (21, "00041222k00"),
    (22, "000412223k0"),
    (23, "000042223k0"),
    (24, "000004123k0"),
)]
