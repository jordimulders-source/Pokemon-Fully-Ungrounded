# Rock r11 (23 nov): schaduwronde

Jordi over r10: "de schaduw mag wat meer uberhaupt op het lichaam vallen, de neus is niet meer rond nu, de schaduw is gewoon vrij inconsitent nog of niet?"

**Basis:** r10. Alleen tintindexen zijn veranderd binnen bestaande vormen.
- Silhouet-diff 0 (script).
- 105 pixels gewijzigd.
- Er is één lijnpixel gewijzigd: de neushoek (25,16) wordt mutsschaduw (zie Neus).
- Het palet is gelijk aan r10.

**Bouw:** `bouw.py` (edits per onderdeel, met een bewaking die alleen wissels binnen één tintfamilie toestaat). Verder:
- metingen: `meet_schaduw.py`, `vlek.py`;
- kaart: `kaart.py` + `schaduwplan.py`;
- vel: `vel.py`.

## Schaduwplan (één lichtbron linksboven)
- **Grote schaduwzone:**
  - de rechterkant van de romp: schouderschijf onderaan, de plaat rechtsonder, de rechterarm en -hand;
  - de onderkant van de romp (rij 33–36);
  - slagschaduw onder de mutsrand (plaat tussen neus en baard), onder het haar rechts en rechts naast de baard (smalle strook);
  - de rechterkant van de riem, het rechterbeen, de rechterzool en de rugrots.
- **Lichte zone:** het midden-links van de romp.
  - Het enige grote hooglicht op het lijf staat op de middenplaat; de schouderschijf heeft een klein hooglicht op zijn bovenvlak.
  - Elke plaat houdt zijn eigen ronding (licht linksboven, sikkel rechtsonder), binnen het grote plan.
- **Weggehaald, want tegen het plan in:**
  - losse F-hooglichten verspreid over het lijf: van 16 naar 6 px;
  - de lichte band onderin de linkerdij;
  - het grote C-hooglicht op het rechterbeen en de rechtervoet: nu 1 px glans;
  - baardlicht (D) en lichte facetten bovenop de achterste rugrots;
  - lichte onderkant van de buik.
- **Ongewijzigd, want al consequent:** muts (links licht, rechts schaduw), baard, haar, linkerhand en onderarm, stok en linkerbeen.
- **Kaart:** `schaduwplan.png` (r11 | kaart r11 | kaart r10 | Gnomad | kaart Gnomad; geel = licht, grijs = midden, blauw = schaduw). In r11 staat geen vlak meer tegen de lichtrichting in belicht.

## Aandeel schaduwtint per groot vlak

Binnenpixels, zonder lijnen. Schaduw = S/(S+M+H).

| vlak | r10 | r11 |
|---|---|---|
| lijf (romp, roze) | 43 % | **62 %** |
| lijf links / rechts (x < 41 / ≥ 41) | 34 / 58 % | 56 / 71 % |
| onderkant lijf (rij 33–37) | 55 % | 82 % |
| F-hooglicht op het lijf | 16 px | 6 px |
| armen + handen | 38 % | 45 % |
| neus | 28 % | 30 % |
| riem | 49 % | 55 % |
| broek | 70 % | 76 % |
| muts / baard / stok / zolen | 43 / 47 / 28 / 40 % | 43 / 45 / 28 / 40 % |

De lijf-percentages zijn gemeten in het vak x 26–49, rij 19–37. De overige rijen komen uit de (oudere) onderdelenkaart `sprite/zone_af.npy`, dus die zijn bij benadering.

**Referenties:**

| sprite | vlak | schaduw |
|---|---|---|
| Gnomad | muts | 30 % |
| Gnomad | roze | 33 % |
| Gnomad | blauw | 74 % |
| welp | steen | 32 % |
| steenjaguar | blauw | 32 % |
| steenjaguar | bruin | 46 % |
| bloedmaan | maan | 41 % (incl. donkerste tint) |
| Regirock | grijs | 35 % |
| Regirock | oranje | 38 % |

**Duiding:**
- Het lijf zit met 62 % boven de referenties (30–46 %). Dat is bewust, omdat Jordi meer schaduw op het lijf vroeg.
- Het verschil met r10 zit vooral in de verdeling: r10 had al 43 %, maar verspreid over sikkels per plaat met hooglichten aan beide kanten. Nu is de schaduw één zone: rechts, onder en onder muts/haar/baard.
- Vindt Jordi het te donker, dan kunnen de plaat rechtsonder en de onderste plaat één stap terug. Dat komt uit op ±52 %.
- De broek (76 %) zit gelijk aan Gnomad-blauw (74 %).

## Neus
- **Oorzaak in r10:**
  - De ronde omtrek had een dubbele hoekpixel rechtsboven: (24,16) én (25,16) waren lijn, met (25,17) eronder. Daardoor werd de hoek vierkant.
  - Een 5-diagonaal in de baard, (25,21)–(23,23), lag tegen de 6-lijn rechtsonder. Dat maakte een dikke schuine kant (achthoek).
  - De sikkel was 2 px breed in een rechte kolom (x 23–24).
- **Reparatie:**
  - (25,16) 6 → 3 (mutsschaduw, het enige gewijzigde lijnpixel). De omtrek loopt nu (23,15)→(24,16)→(25,17).
  - De baarddiagonaal 5 → D.
  - Bolschaduw: F-hooglicht linksboven (4 px), midden 8, sikkel 7 die rechtsboven 1 px is en naar rechtsonder breder wordt.
  - De Popplio-boog bleef: zwart van linksmidden (17,19) via linksonder tot onder-midden (21,23), de rest 6.
- **Grens:** de zwarte hoek (17,22) linksonder hoort bij het buitensilhouet en kon niet weg.

## Netheid
- Vlekjes < 3 px: 217 → 178.
- Nieuw zijn alleen: de lijnhoek (24,16) van de neus, 1 px glans op de rechterarm (52,28) en de C-glans op het rechterbeen en de rechtervoet.

## Zelf bekeken (8× en 1×)
- Het lijf leest op 1× als bol: licht midden-links en donker rechts en onder.
- De neus leest weer als bal.
- **Zwak punt:** de lichte zijkant van de plaat rechtsonder (x 37–43, rij 29–33) is een smalle diagonale band van 2–3 px. Dat is binnen het plan, maar de keurder moet hierop letten.
