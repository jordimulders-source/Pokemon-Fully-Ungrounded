# Lama fase 2: silhouet ronde 3 (maker, 3 nov)

Bron: `direct.txt` (poppetje ronde 3, `bron.py 0.98`: 1071 px, box 36×62; opnieuw gedraaid, identiek). Met de hand gerepareerd als spans per rij in `spans_ronde3.py` (elke rij met de hand gezet, geen automatische vormen) → `ronde3.txt` / `ronde3_1x.png`. Vel: `vel_ronde3.png` (`vel.py`). Controles: `controle.py` → `controle_uitvoer.txt`.

**Resultaat:** 1224 px (1,20× fase 1 = 1019; bron 1071), box 37×62, y1–62, één component, 0 losse pixels, 0 gaten.

## Zones en wat ik deed
| Zone | +px / −px t.o.v. direct | Max. afstand tot de bron | Wat |
|---|---|---|---|
| 1 kop (y0–20, + onderlip y21 x≤19) | +48 / −17 | 3,2 px (oortoppen) | Oren als twee bladvormige banaanoren in een lichte V zoals het poppetje (links 2–4 px breed, rechts/ver iets kleiner en 1 rij lager), widest in het midden waar de kwast zit, top iets naar binnen; 2–6 px lucht ertussen (y1–9). Schedel rond, korte kuif als ronde kruin tussen de oorbases (y10), voorhoofd schuin naar een stompe ronde snuit (x14, y15–18), hangende onderlip als bolling x16–18 y21 met 2 px lucht naar de keel. Kop bijna haaks op de hals. Oogruimte hoog op de zijkant (x20–23, y13–14) blijft vlak. |
| 2 hals (y21–28, x≤32) | +4 / −5 | 1,0 | Kaarsrecht (gemiddelde rand x20 en x29–30, als de bron). Ruig: 5 hangende plukken (voor y22–24 en y26–28; achter y14–18, y20–22, y24–26), elk 3–5 rijen die naar onder uitgroeien en dan 2 px terugspringen. Geen zaagtand van 1 px. |
| 5 halsband (y29–33, x≤32) | +7 / 0 | 2,0 | Ring 1 px breder dan de hals aan de voorkant (x17, y30–31), pompons als kleine bolling eronder (x18, y32–33). |
| 3 lijf + staart (y21–44) | +59 / −7 | 2,2 | Omtrek als Mareep/Flaaffy: de ronde massa van de bron met zachte bobbels van 3–5 rijen en 1–2 px diep, geen ruis. Borst: 2 plukken (y34–38, y39–42); achterwerk: 3 hangende plukken (y28–31, y33–36, y38–40) rond de bronrand x48–49; aguayo als lichte welving op de rug (y24 x38–42, geen koffer); staart als ronde pluim (y21–26, x45–50); buik: één franjepluk tussen de poten (x34, y44). |
| 4 poten (y45–63) | +163 / −99 | 5,0 (verre achterpoot in eigen kolom) | Pose van de bron: nabije voorpoot opgetild met de handschoen in dekking (x16–23, y49–55, rond), verre voorpoot dragend met handschoen op de grond (x24–32, y56–62). Achter: verre poot x35–42 (voet y58, hoger), nabije x42–50 (voet y61) met hak naar achteren (y51–52). Wolmouw/-broek tot y46–47 (1–2 px breder, met een terugspringende pluk), daaronder slanke benen van 5 px met een zachte knie/hak. |

Buiten de zones: 0 px verschil (alle rijen vallen in een zone; de afstandskolom bewijst dat de massa van de bron komt: hals ≤1 px, lijf ≤2,2, kop ≤3,2 alleen aan de oortoppen).

## Controles (script)
- **Rechte randen ≥ 4 px:** verticaal 0. Horizontaal: bovenrand van de rug y24 x38–42 (5; de top van de welving, lamarug is recht: SPEC "rug recht") en de hoefzool y61 x43–47 (5; grondcontact, zoals bij echte sprites).
- **Poten (breedte / lucht per rij, zie `controle_uitvoer.txt`):** alle benen ≥ 5 px (behalve de onderste afrondingsrij van handschoen/hoef); lucht 2–5 px tussen alle vier poten vanaf y45; ruimte onder de buik (x33–34) leeg vanaf y45.
- **Kop:** y1–21 = 21/62 = **34 %** (fase 1: 40 %); 214 px.
- **Formaat:** 1224 px, iets boven ±1050–1200: vier poten in eigen kolommen met 2 px lucht kosten ±70 px t.o.v. de bron (waar de poten samenvielen).

## Toets op 1× (naast Flaaffy, Mareep, Girafarig, Ponyta en de alpaca)
- **Lama:** ja. Rechte lange hals + twee rechte banaanoren in een V + pluimstaart omhoog + rechte rug; geen hoorns (de kwast zit binnen de oorbreedte, geen uitstekende knoppen meer), geen paardenhoofd (stompe ronde snuit, korte kop).
- **Niet alpaca:** langere hals, lange oren, slanke onderbenen, kop klein t.o.v. het lijf.
- **Fluffy:** golvende omtrek op hals, borst en achterwerk; op 1× subtiel, zoals Mareep (Game Freak doet de wol vooral met de kleur, de omtrek blijft rond met kleine bobbels).

## Eerlijk: wat (nog) niet leest of aandacht vraagt
- **Kop 34 %** ligt net onder de gevraagde ±35–40 %. Groter maken kost hals (en Jordi wil de kaarsrechte lange hals) of breekt de verhouding van het goedgekeurde poppetje; 34 % = de bron. Keuze voor Claude/Jordi; het jonge zit dan in oog en kleur.
- **Oortoppen** wijken 2–3 px van het poppetje af (V iets wijder), bewust: anders kleven de oren op 1× samen tot één punt.
- **Handschoenen** zijn in het silhouet ronde bollen; MMA (open vingers, nagels) komt pas in de kleur.

## Lessen
- Game Freak-wol (Mareep, Flaaffy) is in het silhouet **rond met bobbels van 3–5 px lang en 1 px diep**; mijn eerste poging (elke 3 rijen 1–2 px in en uit) las op 4× als zaagtand. Hangende plukken: 3–5 rijen uitgroeien, dan in één keer 2 px terug; maximaal 5 per onderdeel.
- Kwasten die buiten de oorrand uitsteken + toppen naar binnen = lier/gewei op 1×. Kwast binnen de oorbreedte, oren in de V van de bron.
- Een randcheck (rechte runs ≥ 4, lucht per rij, losse px) als script na elke handronde scheelt kijkwerk; de overlay op de onderlaag met 64-raster toont waar de massa afwijkt.
