# Gnomad sprite r10: hele sprite volgens Dragonfly Cave (22 nov)

Bron: `../sprite_r9/gnomad.png`. Jordi: "ja en doe nu de hele sprite volgens dragonflycave".
Regels uit de gids (r. 89–91, 400–404, 425–428): outline shadows zwart; "the base outlining shade for every color" voor de rest van de lijn, 1 px breed; outline highlight (schaduwtint) ín de lijn op de meest belichte randen; geen anti-aliasing buiten de lijn.

Script: `r10.py` (+ `analyse.py`: per buitenlijnpixel het eigen kleurvlak en de normaal; zwart als de rand van het licht linksboven afwijst of onderkant is, anders de outline base van het vlak; twijfelgevallen volgens de tint aan de binnenkant). `beelden.py` maakt de vellen.
Controles: silhouet (alpha) diff 0, palet ongewijzigd (16 kleuren, niets vervangen), riem en gesp met hun zwarte lijnen diff 0, geen nieuwe 2×2-zwartclusters.

**Zwart: 235 → 198 px (15,4 % → 13,0 % van 1525).** 46 pixels gewijzigd.

## Per onderdeel
- **Muts (outline base 2 donkerlila):** bovenrand rechts en de schuine kant tot de schouder (35,10), (39,11)–(46,17) zwart → 2; vanaf (47,18) is de flank zwart (schaduwkant, binnenkant tint 3), één overgang, geen zwart/lila om en om. Linkeronderhoek rand (11,26) → 2. Staart: linkerkant langs het gaatje (44,26)–(47,33) → 2 (rand naar links); rechterkant van het gaatje en de onderkant van de staart blijven zwart. Staartpunt boven (57,34) → 2. **Outline highlight** 3 op (23,12), (24,11), (25,11) (top van de bolling, binnen de lijn).
- **Neus (outline base 6 donkerroze):** linker-/linksonderrand tegen de snor (14,28)–(14,30), (15,31), (16,32) zwart → 6; de onderkant (17..22,33) blijft zwart (diepste schaduw onder de neus). Losse zwarte pixel rechts van de neus (24,31) → 6 (las eerder als oog, sprite r1).
- **Snor (outline base e bruin, nooit roze):** linkerbuitenrand (10,32), (11,33), (11,34), (10,37), (12,38) zwart → e; losse zwarte pixels in de strengscheiding (12,34) en (15,37) → e. Rechtse plukje: bovenhoek (42,29) → e. Geen outline highlight op de snor: te licht, de gids (regel 4) zegt dan bij de outline base blijven.
- **Huid/handen (outline base 6):** linkerhand linksonder (4,45) blijft 6 (de automatische regel wilde zwart). Rechterhand bovenrand (48,41), (49,42) zwart → 6; rand naar rechts vanaf (49,43) zwart. Gezichtsrand onder het rechtse plukje: (41,37) 6 → zwart (lag als enige roze pixel tussen zwarte op die rand). **Outline highlight** 7 op linkerhand (5,40), (4,41).
- **Broek/schoenen (outline base 9):** (39,53) en (34,54) (bovenkant rechterschoen) en (13,57) (linkerkant linkerschoen) zwart → 9. **Outline highlight** a op (15,54), (16,54) (bovenkant linkerschoen).
- **Riem en gesp:** niets gewijzigd (Machoke-voorbeeld; de gids vraagt hier niets wat het Machoke-voorbeeld tegenspreekt).

## Welk zwart bleef en waarom
- **Schaduwkant (rechts/onder) van elk vlak:** mutsflank vanaf (47,18) en staartonderkant; gezichtsrand onder het rechtse plukje (40,36)–(43,38); rechterkant handen en onderkant handen/armen (incl. (5,45), (10,44)–(10,45), (11,43)–(12,43), oksel (13,42)); onderkant schoenen en rechterkant benen. Gids: "outline shadows are always black".
- **Diepste schaduwen:** onder de neus (17..22,33); onder de snor op het lijf (12..17,38) en (11,37); kruis tussen de benen (35..37,53); rand van het mutsgaatje aan de rechterkant.
- **Riem/gesp:** alle zwarte lijnen boven en onder de riem en om de gesp (bevroren); het 2×2-blokje zwart onder de gesp (19..20,49..50) zit in die bevroren zone.
- **Onderkant rechtse plukje** (42,34), (41,35), (42,35): schaduwkant; (42,35) maakt daar een kleine cluster, maar is een silhouetpixel; omkleuren zou een losse lichte pixel buiten de lijn geven (anti-aliasing), dus zwart gelaten.

## 1×-controle
`donker_1x.png`: op zwart en wit, 1× en 3×: muts, neus, snor, riem en schoenen blijven gescheiden; de donkerlila mutsrand en de bruine snorrand lezen op zwart nog als rand.
Bestanden: `gnomad.png`, `gnomad_8x.png`, `vergelijk_8x.png` (r9 | r10 | gewijzigd in magenta kader), `donker_1x.png`.
