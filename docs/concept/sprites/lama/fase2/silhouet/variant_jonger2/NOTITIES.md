# Lama fase 2: silhouetvariant jonger2 (getekend) + ruwe kleurproef (maker-agent, 2 nov)

## Jordi (letterlijk)
- Over 2c: "de vacht is idd te klonterig. Daarnaast lijkt die nu iets te volwassen denk ik?"
- Aanvulling: "fase 3 moet echt meer buff zijn dan 2, die mag nog wt meer fluffy zijn/jonger dus"

## Opdracht
Fase 2 is een jonge, pluizige tussenvorm (Marshtomp/Charmeleon-idee), als contrast met fase 3: gespierd, geschoren, met de wol alleen als kleding.
- `variant_jonger` (rijen weghalen) ging terug: te weinig anders. Deze variant is helemaal opnieuw getekend.

## Analyse (zie ook `../variant_jonger/NOTITIES.md`)
- **Tussenvormen:** 1100–1370 px. De kop is ±38–45% van de hoogte, het oog is groot, de ledematen zijn kort en dun, de vorm is rond en compact, met weinig versiering.
- **Eindvormen:** 1,3–2,2× zo zwaar, met brede schouders en lange ledematen.
- **Maatstaf op het vel:** Charmander → Charmeleon en Mudkip → Marshtomp.

## Wat er getekend is (`spans.txt`, met de hand getypt: `rij x0-x1 ...`)
- **Kop (y1–25, 41% van de hoogte):** opnieuw getekend als ronde lamakop:
  - banaanoren dicht bij elkaar, rechtop, met een brede voet en de punten iets naar binnen, 9 rijen lang;
  - een ronde wolkruin;
  - een voorhoofd met een kleine stop op y17;
  - een korte stompe snuit naar linksonder (voorkant x9–10);
  - de kin los van de hals, met een inham op x18.
  - In het silhouet is ruimte voor een groot oog (proef: 4×4 op x16–19, y15–18).
- **Hals:** kort en wollig. Hij komt achter de kaak tevoorschijn (rechts, x26–33) en heeft zachte bobbels in de achterrand.
- **Lijf (y28–43, x14–53):** rond en compact, met zachte wolbobbels van 1 px in de omtrek: borst links, achterwerk rechts. De staart is een pluim omhoog.
- **Poten (y44–61, korter dan in ronde 2: 18 rijen in plaats van 22):**
  - **Nabije voorpoot:** opgetild, met een wolmouw die naar voren buigt. De handschoen (x10–17, y49–55) hangt vóór de borst en staat 6 rijen los van de grond.
  - **Verre voorpoot:** een staande wolmouw, een knie en een slank onderbeen, met een handschoen op de grond.
  - **Verre achterpoot:** wolbroek, hak en hoef, hoger geplaatst.
  - **Nabije achterpoot:** dikke wolbroek, hak, slank onderbeen en hoef.
  - Elke poot staat in een eigen kolom met lucht ertussen.
- **Formaat:** 1350 px, box 45×61.
- **Wat blijft:** de pose (driekwart, rustige stand, telgang zoals bij kameelachtigen) en de kleding (halsband, aguayo met kwastjes, MMA-handschoenen, oorkwasten).

## Ruwe kleurproef (`proef_lama.png`, `proef.txt`): **PROEF, niet afgewerkt**
- Met de hand getypt met de tinten van kleur ronde 3:
  - licht linksboven, rustige vlakken, kernschaduw onderaan;
  - halsband als U, aguayo met strepen, rode handschoenen met polsband en nagels;
  - een groot oog: zwart bovenlid, glans, blauwe reflectie.
- `bouw_proef.py` bouwt en controleert alleen: alpha-diff 0 met `variant_jonger2.txt`, 0 open randen, 16 kleuren, palet gelijk aan ronde 3.

## Bestanden
- `spans.txt` (bron), `variant_jonger2.txt`, `variant_jonger2_1x.png`, `bouw.py`;
- `proef.txt`, `proef_lama.png`, `bouw_proef.py`;
- `vel.png` (`vel.py`):
  - 4×: ronde 2 | jonger2 | proef | alpaca | fase 3Y;
  - 2×: ronde 3 | proef | Charmander → Charmeleon | Mudkip → Marshtomp;
  - 1×: alles op een rij, met 2c en ronde 3.

## Eigen keuring
- Op 1× en 4× is jonger2 duidelijk anders dan ronde 2: een grotere ronde kop met een groot oog, korte poten, een rond pluizig lijf en een korte wolhals.
- De verhouding ligt tussen Charmeleon en Marshtomp.
- Lama-herkenning: lange banaanoren met rode kwasten, een stompe snuit, de wolstaart omhoog en de aguayo.
- Naast fase 3Y (lang, recht, zwaar) is de stap groot: van jong en pluizig naar volwassen en gespierd.

## Wat eerlijk nog niet werkt
- **Buikonderkant:** in het silhouet een rechte lijn van ±29 px (y42–43). De wolbobbels zitten aan de zijkanten, niet onderaan. Bobbels kunnen daar alleen tussen de poten (x23, x32–34, x43) en zijn dan maar 1–2 px.
- **Hals:** de voorkant onder de kin is maar ±4 rijen zichtbaar. Op 1× zit de kop dicht op het lijf. Lange oren en snuit houden hem lama, maar hij schuift richting alpaca. Een rij langer kost kop-%.
- **Kop:** zo groot dat hij op 1× iets naar veulen/hondje neigt. Dat is het effect dat gevraagd is, maar het verschil met de alpaca (fase 1) is kleiner geworden.
- **De proef is ruw:**
  - halsband en pompons zijn een grove lappendeken;
  - de aguayo is een plat blok met strepen;
  - de bovenkant van de wolmouw van de opgetilde poot is een rij omlijning;
  - de buikschaduw loopt in rechte stappen;
  - nagels en hoeven zijn niet afgewerkt.
  Alleen het oog, de leeftijd en de verhoudingen zijn te beoordelen.

## Lessen
- "Jonger" is alleen te zien als het silhouet opnieuw getekend wordt. Rijen weghalen of een paar pixels toevoegen leest op 1× als dezelfde sprite.
- Bij een grotere kop moeten de oren mee groeien, anders verdwijnt de lama-herkenning (eerste schets: oren als hoorns, kop als paard).
- Wolbobbels in de omtrek: bobbels van 1 px over 2–3 rijen, afwisselend; enkele losse pixels lezen als ruis.
