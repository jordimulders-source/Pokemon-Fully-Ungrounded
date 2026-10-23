# Keuring tegen FAKEMON_CHECKLIST.md: Cuyby, Cuychu, nachtaap, alpaca (23 okt)

Alle vier zijn door Jordi goedgekeurd. Deze keuring verandert niets aan de sprites: ze meet ze tegen de nieuwe checklist (A–E + bouwtype) en zet voorstellen klaar waaruit Jordi kan kiezen. Wat in NOTITIES.md staat als bewuste keuze van Jordi, telt niet als fout. Het wordt wel genoemd als een punt daardoor niet volledig voldoet.

- **Meting:** `vormstudie/tools` (`metrics()` en `shape()`), frame 1. Coördinaten zijn (x, y) in het 64×64-frame.
- **Vellen:** `cuyby.png`, `cuychu.png`, `nachtaap.png`, `alpaca.png`. Elk vel toont rij 1 op 1×, rij 2 op 3× en rij 3 als silhouet op 2×. De eigen sprite staat links, daarnaast 3 echte sprites van hetzelfde bouwtype.
- **Pixelaantallen** in de voorstellen zijn schattingen. **Klein** betekent < 30 px en raakt geen goedgekeurde vorm. **Groot** betekent dat vorm, pose of verhouding verandert.

## Overzicht metingen

| | Cuyby r3 | Cuychu r4 | Nachtaap r10 | Alpaca r15 |
|---|---|---|---|---|
| Oppervlak | 789 | 1416 | 1033 (zonder staart ±822) | 937 |
| Box b×h | 31×32 | 49×44 | 49×36 | 34×51 |
| Soliditeit | 0,874 | 0,838 | 0,707 | 0,657 |
| Symmetrie | **0,939** | 0,791 | 0,447 | 0,480 |
| Aandeel donker (E3) | 0,237 | 0,143 | 0,185 | 0,174 |
| Kleuren | 16 | 16 | 15 | 16 |

Referenties uit dezelfde metingen:
- Jigglypuff: 747 px, sol 0,86, sym 0,87.
- Wooloo: 983 px, sol 0,92, sym 0,89.
- Piloswine: 1515 px, sol 0,93, sym 0,90.
- Zigzagoon: 1315 px, sol 0,80.
- Aipom: 856 px, sol 0,65, sym 0,47.
- Teddiursa: 652 px, sym 0,75.
- Grookey: 814 px, sym 0,78.
- Ponyta: 1291 px, sol 0,69.
- Mudbray: 1080 px, 42×51, sol 0,68.
- Deerling: 638 px, sol 0,67.

**Over de grenzen voor bollen:** echte bollen gaan zelf over de H-grenzen van A4/A5 voor bollen (sol ≤ 0,85, sym < 0,85). Jigglypuff haalt sym 0,87, Wooloo 0,89 en Piloswine 0,90. Een te hoge waarde bij een bol of vachtdier is dus een signaal, geen automatische afkeur.

---

## 1. Cuyby (ronde 3): **voldoet, op twee frontaal-punten na die bij het goedgekeurde ontwerp horen**

Sjabloon:
- Bouwtype: bol.
- Fase: 1.
- Type: Normal; knuffelig, schattig.
- Pose: P14.
- Skelet: Jigglypuff, Whismur, Wooloo.
- Snuit: kort, twee ogen.
- Kenmerk: oren en driekleur.
- Tegenwicht: geen; dat is gebruikelijk bij een bol.

| Punt | H/R | Voldoet | Meting | Toelichting |
|---|---|---|---|---|
| A1 | H | ja | silhouet = bol met 2 oortjes | Leest als ronde knager ("Hamtaro-look", Jordi). |
| A2 | H | deels | oren 4×4 px (x19–23 en x39–43, y16–19) | Het hoofdkenmerk (de driekleur) zit in de kleur, niet in de omtrek. In het silhouet steken alleen de kleine oortjes en de lokpunten onderaan uit. Op 1× leest de driekleur wel heel sterk. |
| A3 | H | deels | gezichtsmidden x27,5, boxmidden x31 | Het gezicht staat 3,5 px links van het midden, zoals de bol-regel vraagt. Een diagonaal of tegenwicht is er niet; voor een bol is dat normaal. |
| A4 | H | deels | sol 0,874 (grens bol 0,85) | Ligt tussen Jigglypuff (0,86) en Wooloo (0,92). Bollen mogen massief zijn. |
| A5 | H | **nee** | sym **0,939** (grens 0,85) | Het silhouet is vrijwel gespiegeld, net als in de vormstudie. De kleur (zwart/crème/oranje) is wel sterk asymmetrisch. De ogen zijn verschoven kopieën: dezelfde 5×5, met glans en weerkaatsing op dezelfde plek. |
| A6 | R | deels | zijkanten recht: x17 over y28–33 (6 px), x46 over y28–35 (8 px) | Jigglypuff heeft ook rechte flanken. Licht. |
| B1 | H | deels | gezicht verschoven, lijf frontaal | Bij een bol zijn kop en lijf één vorm. Het naar links geschoven gezicht is de enige draai. |
| B2 | H | ja | neus (27–28, 34), 2 rijen onder de ogen | Korte snuit, twee ogen. |
| B3 | H | deels | ogen x20–24 en x30–34: beide 5 breed, op gelijke hoogte | De neus staat links van het midden (ja). Het linkeroog staat 3 px van de omtrek en is dus het verre oog, maar het is niet smaller. |
| B4 | H | n.v.t. | | Korte snuit. |
| B5 | R | deels | beide oortoppen op y16 | Ze verschillen in kleur en iets in vorm, niet in hoogte. |
| B6 | H | ja | | Bol: kop en lijf zijn één vorm. |
| B7 | H | ja | ogen, roze neus, Y-mondje (y35–36) | |
| C1 | H | ja | 2 oren, 2 ogen, 2 voorvoetjes + zijpootjes | |
| C2–C5 | H | n.v.t. | | Bol. |
| C6 | H | deels | voetkussens (26–27, 45) en (35–36, 45): gelijk | De pootjes staan op dezelfde hoogte en hebben hetzelfde patroon `1cd1`. P14 vraagt "verschillend van hoogte". Alleen de zijpootjes verschillen 1 px. |
| C7 | H | ja | | Rust op de voetjes. |
| C8 | R | n.v.t. | | Een cavia heeft geen staart. |
| C9 | R | ja | | Knuffelig en schattig. |
| D1 | H | ja | 789 px | Bol 31×32 (Jigglypuff 32×33). |
| D2 | H | n.v.t. | | Bol: kop = geheel. |
| D3, D4 | H/R | ja | breedte 31 | |
| D5 | R | deels | Cuychu/Cuyby = 1,79× (doel 1,5–1,7) | Licht boven de lijn. Cuychu is als "hooiberg" bewust een massa. |
| E1 | R | ja | | Oranje schaduwkant rechts. |
| E2 | R | ja | | |
| E3 | R | ja | 0,237 | Aan de bovenkant van de band, door de zwarte vacht. |

**Voorstellen (op impact):**
1. **A5/B3 – verre oog 1 px smaller (klein, ±5 px).** Kolom x24 van het linkeroog (y29–32) wordt vacht (crème `b`). Het linkeroog wordt 4 breed, het rechter blijft 5. Daarmee zijn de ogen geen kopieën meer en draait het gezicht leesbaar naar links. *Raakt:* de ogen die Jordi goedkeurde (de vorm, niet de kleur). Proeven naast ronde 3 op 1×: de glans (21–22) moet blijven.
2. **B5 – zwarte (verre) oor 1 px hoger (klein, ±6 px).** Een rij K/`a` boven (19–22, 16), zodat de oortoppen verschillen. *Raakt:* het silhouet bovenaan, 1 px.
3. **C6 – linker voetkussen 1 px hoger (klein, ±6 px).** Het kussen (26–27, 45) schuift naar y44 en (26–27, 46) wordt omlijning/transparant. *Raakt:* de onderrand. Op 1× nauwelijks te zien.
4. **A5 – silhouet asymmetrisch (groot, 40–80 px).** Bijvoorbeeld de bol rechts 1–2 px lager en breder laten uitlopen, of de lokpunten links hoger. *Raakt:* de goedgekeurde frontale bol en de middenscheiding. **Niet aanbevolen:** Wooloo en Jigglypuff zitten er zelf ook boven.

---

## 2. Cuychu (ronde 4): **voldoet; zwakste punt is de negatieve ruimte (bekend: "vachtkoepel")**

Sjabloon:
- Bouwtype: vachtdier/bol.
- Fase: 2.
- Type: Normal (of Normal/Grass); rustige hooiberg.
- Pose: P13/P14.
- Skelet: Piloswine, Wooloo, Zigzagoon.
- Snuit: kort. Eén oog in beeld, want het verre oog zit onder de pony.
- Kenmerk: kruinsprieten bovenop.
- Tegenwicht: geen; de rug daalt naar rechts.

| Punt | H/R | Voldoet | Meting | Toelichting |
|---|---|---|---|---|
| A1 | H | ja | | Langharige cavia/hooiberg; "duidelijk een Cuyby-evolutie" (Jordi). |
| A2 | H | ja | kruin x18–31, y11–20 | De sprieten breken de omtrek bovenaan. Op 1× te lezen. |
| A3 | H | deels | head-index −0,077 (massa boven links) | Het gezicht staat linksboven en de massa loopt naar rechtsonder. Rechts(boven) ontbreekt een tegenwicht: de rug zakt van y20 naar y30. |
| A4 | H | deels | sol 0,838 | Bolgrens is 0,85; Zigzagoon haalt 0,80 en Linoone 0,72. Lucht zit er alleen tussen de lokpunten onderaan (y48–53). Piloswine (0,93) laat zien dat een vachtberg massief mag zijn. |
| A5 | H | ja | sym 0,791 | Net onder 0,80. |
| A6 | R | ja | | Geen randstuk > 4 px (bouw9). De lokken lopen schuin. |
| B1 | H | ja | | Lijf 3/4 (rug daalt). De kop is 3/4 met de snuit naar links-voor. |
| B2 | H | ja | snuit x13–20, y36–42 | Neus (12–13, 39–40) is het meest linkse punt van het gezicht. Eén oog; dat is bewust zo ontworpen ("kleine ogen", pony). |
| B3 | H | n.v.t. | | Eén oog. |
| B4 | H | ja | | Oog en snuit wijzen naar links-onder. |
| B5 | R | ja | 1 oor (29–33, 27–29) | Het verre oor zit onder het haar. |
| B6 | H | ja | | Het gezicht zit in de vacht. |
| B7 | H | ja | oog, neus, mond (y41) | |
| C1 | H | ja | 4 voetkussens: (11,51), (19–21,52), (38,51), (42–43,49) | |
| C2 | H | deels | voethoogtes 49/51/52 | Er zijn 3 hoogtes (ja). Het meest linkse kussen (11,51) is niet het laagste: dat is (19–21,52). Daardoor staat een verre voorpoot vóór de nabije (zie C3). |
| C3 | H | deels | (11,51) links van (19–21,52) | Klein Escher-risico. Op 1× valt het nauwelijks op, omdat de kussens kleine roze stipjes in het haar zijn. |
| C4, C5 | H | n.v.t./ja | | De poten zitten in het haar. |
| C6 | H | deels | | De achterpoot rechts staat hoger (y49). De kussens zijn verder gelijk. |
| C7 | H | ja | | |
| C8 | R | n.v.t. | | Geen staart. |
| C9 | R | ja | | Rustig en log, past bij een hooiberg. |
| D1 | H | ja | 1416 px, 49×44 | Fase 2 vraagt 1100–1550 px en een box van ±47–53. |
| D2 | H | deels | gezicht y26–43 = ±41% | Doel is 30–35%. Bij een vachtberg zijn kop en lijf niet te scheiden. |
| D3, D4 | | n.v.t. | | Fase 1-regels. |
| D5 | R | deels | 1,79× | Zie Cuyby. |
| E1 | R | ja | | Rechterkant donker, zwart aan de schaduwkant 0,88. |
| E2 | R | ja | | Lokscheidingen in omlijningsbasis, K alleen onder de punten. |
| E3 | R | ja | 0,143 | |

**Voorstellen:**
1. **A4 – meer lucht tussen de lokpunten onderaan (klein, 10–15 px).** Twee à drie inkepingen 1 rij dieper maken, bijvoorbeeld tussen x25–28 en x32–35 op y49–51: transparant, met K als bovenrand. *Raakt:* alleen de onderrand van de lokken. Het silhouet wordt rafeliger, zoals Zigzagoon; de vorm blijft.
2. **C2/C3 – het meest linkse kussen weg (klein, 2–3 px).** (11,51) `e` wordt haar (`2`/`3`). De verre voorpoot zit dan onder het haar, zoals bij Piloswine, en de nabije voorpoot (19–21,52) is de meest linkse en laagste. *Raakt:* een van de 4 zichtbare pootjes ("korte pootjes", Jordi). Alternatief: laten zoals het is.
3. **A3 – plukje rechtsboven als tegenwicht (groot, 40–60 px).** Een opstaande pluk ichu-gras op de rug (x44–52, y17–24), zodat het silhouet rechts niet alleen daalt. *Raakt:* het goedgekeurde silhouet en de kruin als enig kenmerk. Alleen als variant.

---

## 3. Nachtaap (ronde 10): **voldoet niet helemaal; de punten liggen bij frontaal en formaat, en Jordi koos die bewust**

Sjabloon:
- Bouwtype: aap.
- Fase: 1.
- Type: Psychic; maangenezer, stil, starend.
- Pose: P5 (zittend), naar P8 in latere fases.
- Skelet: Aipom, Teddiursa, Grookey.
- Snuit: kort, twee ogen.
- Kenmerk: spiraalstaart.
- Tegenwicht: de spiraal rechtsboven.

Jordi: "dynamisch genoeg, we zitten er niet frontaal op"; geen vormronde.

| Punt | H/R | Voldoet | Meting | Toelichting |
|---|---|---|---|---|
| A1 | H | ja | | Zittende aap met grote ogen en een spiraalstaart. |
| A2 | H | ja | spiraal x44–57, y21–35 | Breekt duidelijk de omtrek. Op 1× te lezen. |
| A3 | H | ja | kop linksboven, staart rechtsboven | Kijkrichting: pupillen 1 px naar links. |
| A4 | H | ja | sol 0,707 | Lucht tussen staart en lijf. Arm en romp zijn gescheiden door omlijning, zonder lucht. |
| A5 | H | ja (silhouet) / deels (gezicht) | sym 0,447 | Het silhouet is asymmetrisch door de staart. Kop, middenstreep (x24–25) en mond staan wel exact op het kopmidden. |
| A6 | R | **nee** | romp rechts x35 over y40–46 (7 px); verre arm 10 px recht; bovenkant kop 8 px recht (y20) | Zuil van romp plus verre arm. NOTITIES noemt dit al. |
| B1 | H | deels | | Kop vrijwel frontaal, lijf ook. Perspectief zit alleen in de verre arm (smal en donker) en de knie. Jordi koos dit bewust. |
| B2 | H | ja | mond y38, 3 rijen onder de ogen | |
| B3 | H | **nee** | linkeroog x15–21 (7 breed, 3 px van de omtrek), rechteroog x27–32 (6 breed, 5 px van de omtrek); mond (24–25, 38) = kopmidden | Het perspectief spreekt zichzelf tegen. Het linkeroog staat als verre oog dicht bij de omtrek, maar is groter. De mond staat niet links van het midden. Het blijft frontaal, terwijl de blik naar links gaat. |
| B4 | H | n.v.t. | | |
| B5 | R | ja | linkeroor top y24, rechteroor y25; breedte 7 en 6 | |
| B6 | H | ja | | De kop overlapt de schouders en er is geen nek. |
| B7 | H | deels | ogen + mond van 2 px, geen neus | Een nachtaap heeft een klein neusje. Aipom heeft er ook geen, dus licht. |
| C1 | H | ja | 2 oren, 2 ogen, 2 armen, knie en 2 voeten, staart | |
| C3 | H | ja | | Armen onder de schouders. |
| C4 | H | deels | nabije arm x15–19, y40–52: bijna rechte kolom, 1 px verschuiving | Geen elleboog of pols. De verre arm is een rechte buis. De knie is wel aanwezig. |
| C5 | H | ja | | |
| C6 | H | ja | | Verre arm 3 px en in schaduwtint; verre voet hoger. |
| C7 | H | ja | | Zit. |
| C8 | R | ja | | De staart zet aan bij de heup (36–38, 45–48) en loopt in een boog omhoog naar de spiraal. |
| C9 | R | ja | | Kalm en starend, past bij P5/Psychic. |
| D1 | H | **nee** | 1033 px (fase 1: 700–950); zonder staart ±822 | De overmaat zit volledig in de staart (211 px). Aipom heeft 856 px inclusief staart. |
| D2 | H | ja (grens) | kop y20–39 = 20/36 = 56% | |
| D3 | H | ja | | De romp zit compact onder de kop. |
| D4 | R | deels | breedte 49 (max 48) | 1 px te breed, door de staart. |
| E1 | R | ja | | |
| E2 | R | deels | nabije arm over romp: scheiding x20 in K (zwart) | De checklist vraagt omlijningsbasis O. Aan de schaduwkant van de arm is K verdedigbaar. |
| E3 | R | ja | 0,185 | |

**Voorstellen:**
1. **B3 – mond 1 px naar links (klein, ±4 px).** `dd` op (24–25, 38) gaat naar (23–24, 38), en (25,38) wordt crème-schaduw `7`/`6`. Het gezicht kijkt dan echt naar links, zoals de pupillen al doen. *Raakt:* de positie van het mondje dat Jordi koos (neutraal, 2 px). De uitdrukking blijft gelijk.
2. **B3 – verre oog ook kleiner (klein, ±8–10 px).** Het linkeroog wordt 6 breed door de buitenste kolom x15 (y30–34) weg te halen, of het rechteroog wordt 7 breed. Dan zijn de grootte en de plek van de ogen consistent met een draai naar links. *Raakt:* de ogen uit ronde 10 (uitdrukking "stil, starend"). Altijd naast ronde 10 op 1× proeven (SPRITE_OPDRACHT §3).
3. **C4/A6 – elleboog in de nabije arm (klein, ±10 px).** Een knik van 1 px naar buiten rond y44–45 (x15) en de pols 1 px terug. *Raakt:* het lijf licht; Jordi keurde het lijf, niet de armvorm.
4. **D1 – oppervlak naar ≤ 950 (groot).** Dat kan alleen met een kleinere spiraal (−80 px). *Raakt:* de spiraal die na ronde 9–10 eindelijk goed las. **Niet aanbevolen**, want de romp zelf heeft het fase 1-formaat.
5. **B1 – kop 1–2 px draaien, middenstreep naar x23 (groot).** Jordi wees een vormronde af; alleen noemen.

---

## 4. Alpaca (ronde 15): **voldoet grotendeels; de grote open punten zijn de hals als zuil en de kopverhouding**

Sjabloon:
- Bouwtype: langnek/hoefdier.
- Fase: 1.
- Type: Fighting; bokser.
- Pose: P1/P2 met wat P7 in de voorpoten.
- Skelet: Ponyta, Mudbray, Deerling.
- Snuit: lang, één oog.
- Kenmerk: hals, oren en kuif, met de handschoenen als tweede kenmerk.
- Tegenwicht: staartje omhoog; dat koos Jordi.

| Punt | H/R | Voldoet | Meting | Toelichting |
|---|---|---|---|---|
| A1 | H | ja | | Alpaca, volgens de vorige keuring. |
| A2 | H | deels | handschoenen 102 px, de grootste kleurvlek | Hals, oren en kuif breken de omtrek. Toch is het accessoire op 1× de blikvanger (de checklist zegt: hooguit tweede). Voor Fighting is dat verdedigbaar. |
| A3 | H | ja | head-index −0,15 | Kop linksboven, romp rechtsonder, staart rechtsboven. |
| A4 | H | ja | sol 0,657 | Mudbray 0,68, Deerling 0,67. Lucht tussen alle poten. |
| A5 | H | ja | sym 0,48 | |
| A6 | R | **nee** | hals: linkerrand x21 (y23–27), rechterrand x30 (y21–27), even breed (±9 px); rug recht op y28 over x31–38 (8 px) | Zuil plus doosrug. De vormstudie noemde dit al. |
| B1 | H | ja | | Lijf 3/4-profiel met 4 voethoogtes; kop 3/4 met de snuit voor de verre kant. |
| B2 | H | ja | oog (26–29, 13–16); neus het meest links (x13–14) | Lange snuit, één oog. |
| B3 | H | n.v.t. | | |
| B4 | H | ja | | De snuit wijst naar links-onder. |
| B5 | R | ja | oortoppen y5 (ver) en y4 (nabij) | Andere vorm. |
| B6 | H | **deels** | hals verticaal, niet taps; de kop zit er recht bovenop | Bij Ponyta, Mudbray en Deerling loopt de nek schuin naar voren en taps toe. Hier zit de kop als een blok op een rechte zuil (STUDIE: "speelgoed"). De kop overlapt de hals wel. |
| B7 | H | ja | oog, neus, mondlijn (14–15, 20) | |
| C1 | H | ja | 4 poten, 2 oren, staart | Het verre oog zit achter de snuit; Jordi wilde dat zo. |
| C2 | H | deels | voeten op y54/50/51/47 = 4 hoogtes; nabije voorpoot laagst en meest links | De verre voorpoot staat 4 px hoger (doel 1–3). De verre achterpoot (x38–42) is de meest rechtse, niet "tussen de nabije in". |
| C3 | H | ja | | Elke poot staat onder borst of heup. |
| C4 | H | deels | nabije achterpoot: hak van 2 px naar achteren op y42–43; voorpoten rechte schuine stokken | |
| C5 | H | deels | buikrand y38–39 vrijwel recht, de poten zakken eruit | Heup- en borstbolling zijn er wel. |
| C6 | H | deels | | De verre achterpoot heeft schaduwtint. De verre vuist is even licht als de nabije (polijstpunt 4 uit de vorige keuring). |
| C7 | H | ja | | Staat op vier poten. |
| C8 | R | ja | | Kort staartje omhoog (x42–47, y25–30). Jordi: blijft. |
| C9 | R | ja | | Handschoenen, wijde voorpoten en een vastberaden oog lezen als vechter. |
| D1 | H | ja | 937 px | Box 34×51 is hoger dan ±42. Bij een langnek is dat normaal: Mudbray is ook fase 1, 42×51. |
| D2 | H | **deels** | kop y4–22 = 19/51 = 37% (doel 40–55%) | Ligt lager door de hals. |
| D3 | H | ja | | Compacte boonromp. |
| D4 | R | ja | breedte 34 | |
| E1 | R | deels | | Zie C6, verre vuist. |
| E2 | R | ja | | De verre vuist raakt de nabije achterpoot op (30–31, 48), met K ertussen. |
| E3 | R | ja | 0,174 | |

**Voorstellen:**
1. **C6/E1 – verre vuist een tint donkerder (klein, ±25 px, alleen kleur).** De vuist x24–31, y43–50 schuift `R→r` en `r→s`; de omlijning blijft. Diepte zonder vormwijziging. *Raakt:* de kleur van een goedgekeurde vuist; vorm en silhouet blijven.
2. **A6 – rugrand niet recht (klein, ±4–6 px).** Op y28, x31–38: één `6` 1 px omhoog bij x33–34 (schoft), of 1 px omlaag bij x36. *Raakt:* niets goedgekeurds van betekenis.
3. **C4 – knik in de nabije voorpoot (klein, ±6–8 px).** De poot schuift op y42 1 px naar rechts en eronder weer terug, zodat er een knie ontstaat. *Raakt:* de poot die net op Jordi's verzoek gerepareerd is. Alleen als Jordi dat wil.
4. **B6/A6 – hals schuin naar voren en taps (groot, 60–100 px).** Bovenste deel van de hals (y20–26) 1–2 px naar links. Onderaan bij de borst 1–2 px breder, bovenaan 1 px smaller. De kop schuift 1–2 px mee naar links en zit schuin op de hals. *Raakt:* de goedgekeurde hals- en kopstand en de aguayo-band (die schuift mee). Grootste winst richting "echte Pokémon" (Ponyta en Mudbray op het vel), maar alleen als variant naast ronde 15.
5. **D2 – grotere kop (groot).** **Niet aanbevolen:** dat verandert de goedgekeurde verhouding en botst met de langnek-regel.

---

## Algemene les voor de checklist (voorstel, niet doorgevoerd)
- Voor bollen en vachtbergen gaan echte sprites zelf over de H-grenzen van A4/A5: Jigglypuff sym 0,87, Wooloo 0,89/0,92 en Piloswine 0,90/0,93. Overweeg voor P13/P14 die punten als R te behandelen, of de grens te verhogen naar ±0,90/0,93.
- Langnekken halen D2 (kop 40–55%) en de box ±42 niet; Mudbray haalt 42×51. Overweeg een uitzondering voor langnekken in D1/D2.
