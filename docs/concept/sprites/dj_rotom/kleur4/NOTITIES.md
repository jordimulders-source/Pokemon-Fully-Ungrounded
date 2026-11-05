# DJ Rotom – kleur4 (bliksem + ogen; rest = kleur3)

Basis: `../kleur3/dj_rotom.png` (kop, conussen, hoek, snoer bevroren).
Jordi: "silhouet naar sprite is niet 1 op 1 te vertalen"; "bliksem noot mag idd dikker"; "het zijn nog geen typische rotom ogen".

## Bestanden
- `dj_rotom.png` (64×64, geïndexeerd, transparency=0), `normal.pal` (ongewijzigd), `vel.png`.
- `bron/dj_rotom.txt` (tekstraster). Het raster wordt opgebouwd met `python3 bliksem.py zonderrand && python3 ogen.py && python3 render.py`:
  - `bliksem.py`: de vorm per rij met de hand (L/R-randkolommen), de opbouw rand `1` → `2` → kern `3`, en de noot.
  - `ogen.py`: de Frost-ogen pixel voor pixel.
  - `controle.py`: diff per zone en de checks; `vel.py`: het vel.

## Bliksem (zone x17–31, y0–25; 95 px gewijzigd)
- Hoogte y10–25 (16 rijen, tot in de spitspunt (27,26)), breedte x20–30.
- **Bovenwig y10–16:** een schuin parallellogram dat van rechtsboven (x25–30) naar linksonder (x21–27) leunt, in mint `2`, met de witte achtste noot erin: steel x26 y11–15, vlag (27,11)+(28,12), kop 2×2 x24–25 y15–16.
- **Knik 1:** rechts loopt de rand diagonaal naar binnen (x30→x27, y11–16), daarna steekt de middenband y17–18 uit tot x30.
- **Knik 2:** links springt de onderkant van de wig (x20–23, y18) naar de staart (x24/25).
- **Staart y19–25:** wordt smaller van 6 naar 4 px, met een lichte kern `3` van 2 px (x26–27) tot in de spits.
- Gloed: een rand `1` + een ring `2` rond de lichte kern, net als de plasma van de game-Rotom.
- Geprobeerd en verworpen:
  - een donkere ring om de noot (vlekkerig in een smal blok);
  - een recht blok met een uitsteker (las als zeepaardje).

## Ogen (links x18–23 y35–41, rechts x25–31 y34–41; 19 + 19 px)
- Sjabloon: **de Frost-ogen pixel voor pixel**. Frost-index → eigen index: wit→`f`, lichte iris→`d`, donkere iris→`c`, zwart→`8`, grijs→`b`, f8a880→`4`, e87028→`5`, c04818→`6`.
- Opbouw zoals de game:
  - wit alleen boven en aan de buitenkant;
  - iris met 1 lichte pixel bovenaan en 2×2 donker eronder, en een witte glans linksonder;
  - zwarte pixels opzij in de middenrij, grijs onderaan;
  - schaduw `6` naast het oog.
- Het rechteroog is het gespiegelde Frost-rechteroog, 1 rij hoger.
- De iris is blauwgroen uit de bron (indexen 12/13).

## Checks (`bron/controle.py`)
- Buiten de zones gewijzigd t.o.v. kleur3: **0 px**. Alpha verschilt 62 px, allemaal in de bliksemzone.
- Open randen: **geen**.
- Losse pixels: geen in de bliksem. Wat er nog is, is bewust:
  - in de ogen: (29,35), (19,37), (26,37), (29,38), (18,39), (21,39), (25,39), (26,40), (18,41). Ze komen 1-op-1 uit het Frost-sjabloon; Frost heeft ze zelf ook.
  - 4 glanspixels in de conussen, en de equalizer van 1 px (zoals in kleur3).

## Toets op 1×
- **Bliksem:** leest als ⚡ (schuine wig, knik, staart in de spits), op licht en donker. Niet meer als blad of klodder.
- **Noot:** op 1× een wit ♪-vormpje boven in de bliksem. Op 2–3× duidelijk een achtste noot. Groter kan niet zonder de bliksem breder dan ±10 px te maken.
- **Ogen:** lezen naast Frost en Rotom als dezelfde Rotom-ogen (zelfde amandelvorm: wit boven, iris met glans, zwart opzij).

## Wat nog niet (helemaal) klopt
- De noot is op 1× klein (11 px). Leesbaar als ♪-vorm, maar niet zo uitgesproken als op 3×.
- De staart (y19–25) is een rechte hals; in de bron loopt hij iets schuin naar de spits.

## Lessen
- Een bliksem van ±10 px breed leest pas als ⚡ als de bovenwig echt schuin leunt (rechtsboven → linksonder) en de middenband aan de andere kant uitsteekt. Een recht blok met een nokje leest als blad of zeepaardje.
- Een donkere ring om een witte noot in een smal blok maakt het vlekkerig; wit op de middentint is genoeg contrast.
- Rotom-ogen: neem een game-oog letterlijk als sjabloon (Frost 4–5×6). Een eigen "wit vlak + iris"-oog leest als bril; het game-oog heeft wit alleen boven en buiten.
