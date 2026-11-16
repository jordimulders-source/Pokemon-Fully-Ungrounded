# Gengas v14: bol linksonder de mond rond (16 nov)

Jordi (bij `frame2/lijf_zonder_manen_8x.png`): "hij is niet rond" · "linksonder de mond is ook een puntje" · "o daar links is zoals in het originele model ook, goed dat we dat spotten, kan je de hoofdversie meteen beter maken".

**Het puntje:** linkerrand van de bol per rij 52–54 was x = 15, 15, 18: rij 53 bleef op x 15 staan (horizontaal lijnstukje x 15–17) en rij 54 sprong 3 px. Ellips die de rest van de bol volgt (x = 29,5 − 22,5·√(1 − ((y−34)/24)²)) geeft 14,6 / 15,75 / 17,1 → 15, 16, 17.

**Wijziging (3 px, in beide bestanden gelijk):**
- (15,53): lijn 1 → achtergrond 0 (puntje weg)
- (17,53): lijn 1 → 5 (lichte onderband loopt door, zoals de buurpixel (18,53))
- (17,54): achtergrond 0 → lijn 1 (omlijning schuift 1 px naar links)

Linkerrand rij 44–58 na: 9 9 10 11 11 12 13 14 15 **16 17** 19 21 24 27 (was … 15 **15 18** 19 …). Geen nieuwe indexen; linkermaan (x 0–11, rij 41–52) diff 0 (assert); rechtsonder ongemoeid. De zone is x 5–18 (de rand loopt hier tot x 17, net buiten de "ongeveer x 5–16" uit de opdracht).

Bestanden: `rond_linksonder.py`, `gengas_v14.png`, `lijf_zonder_manen_v14.png`, `voor_na.png` (boven 8×: hoofdsprite voor/na, lijf zonder manen voor/na; onder 16× uitsnede x 2–25, rij 40–59).
