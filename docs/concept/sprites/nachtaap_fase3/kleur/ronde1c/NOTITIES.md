# Nachtaap fase 3: kleurronde 1c (5 nov)

Bestanden: `nachtaap_fase3.png`, `normal.pal` (ongewijzigd t.o.v. 1b), `raster.txt`, `vel.png` (1c 4× licht/donker, model, 3× 1c naast 3× 1b, 1× licht/donker naast 1b, fase 2 en Primeape/Medicham/Alakazam/Slaking/Aipom).
Bron: `bron/delen.txt` (= 1b, onaangeroerd) + `bron/ronde1c.txt` (alleen de opdrachtzones, met de hand geschreven, overschrijft 1b) → `bron/bouw.py` → `bron/check.py` (diff met 1b en silhouet per zone) → `bron/vel.py`.

Opdracht: Jordi "ja, je mag buiten het silhouet gaan" (hooguit 1–2 px per plek, hand/gloed, kruin + maan, spiraalgat) + ogen, plooi, vuist, dijrand binnen het silhouet. Eerder: "let ook op verhouding van benen, armen met lichaam, strepen etc" / "vooral verbinding van onderste been met lichaam, strepen laat maar weg" / "de maan mag nog iets groter" / "als er geen healing hand met de palm richting de tegenstander is dan mag je het altijd afkeuren".

## Diff met 1b (check.py)
- 193 px gewijzigd, **0 buiten de zones**: hand+gloed 102, kop+maan 32, spiraal 22, vuist 18, plooi 10, ogen 7, dijrand 2.
- Zones (x0,y0,x1,y1, exclusief): hand+gloed (5,45,25,64), kop+maan (1,26,21,35), spiraal (48,28,62,37), ogen (4,36,13,39), plooi (28,39,33,46), dijrand (42,47,48,52), vuist (0,13,13,23).

## Afwijking van silhouet ronde 1 (24 px; 1816 px totaal, was 1796)
- **Hand/gloed: 17 erbij**, overal 1–2 px links van het silhouet: (8,48) (8,49) (7,50–55) (8,53–55) (6,56–57) (7,56–57) (7,58) (8,59). Nodig om vier vingers van 2 px + scheidingslijnen + omlijning + gloedband te krijgen, en voor de duim.
- **Kruin: 3 erbij**: (7,28) (8,28) (8,27). De kruin ligt 2 px hoger (bovenkant rij 27 i.p.v. 29); rij 27 x9–12 lag al in het silhouet (de vuistarm erachter, nu bedekt door de kop).
- **Spiraalgat: 2 erbij, 2 eraf**: (53,31) (53,34) gevuld, (56,32) (56,33) open. Gat blijft 12 px, nu rond (2-4-4-2) i.p.v. 3×4.
- Silhouetcontrole nieuwe omtrek (`silhouet/korrel.py` op de 1c-omtrek): 0 uitsteeksels, 0 inkepingen, 0 tanden. Open randen: 0.
- Losse pixels: 32 (1b: 32), alle bewust: ogen, glans, neusgaten, knokkelgroeven vuist, maanpunt (5,34), hand-glimlichten (12,55) palm en (8,56) duim, vingerlijn-einde (12,54).

## Per zone
1. **Healerhand + gloed** (Gen 1-Drowzee, model):
   - Vier vingers van 2 px met een omlijning (D) ertussen, dicht tegen elkaar: wijsvinger x10–11, middel x13–14, ring x16–17, pink x19–20.
   - Lengte (binnenkant, tot de handpalm op rij 54): middelvinger 7 rijen (top rij 47), ring 6, **wijsvinger 5** (top rij 49), pink 4. Lichte waaier: middelvinger het hoogst, pink het laagst.
   - Ronde toppen: elke top is een D-kapje van 2 px; de hoekpixels ernaast zijn gloed, zodat de toppen los staan.
   - Licht van linksboven: wijsvinger helemaal M, de andere vingers M links/m rechts; de lijnen tussen de vingers worden op rij 54 m (overgang naar de palm).
   - Palm naar de kijker: rijen 54–58, licht linksboven (glimlicht W op 12,55), m naar rechtsonder en naar de pols.
   - Duim linksonder, schuin naar linksboven: 2 px breed (rijen 56–57, x8–10), met een glimlicht en een schuine plooi (D) naar de palm.
   - Gloed: G-omlijning + B-band links en boven (nu 1 px verder naar links), b-band rechts; de pols (V) aan de onderkant blijft zoals in 1b.
2. **Kruin + maan**:
   - De kruin is 2 px hoger; de linkeromtrek loopt rond (rij 27 x8, 28 x7, 29 x6, 30 x5, 31 x4, 32 x3). De rechteromtrek en de arm erachter zijn van 1b.
   - Boven de maan liggen nu 2 rijen vacht (28–29) plus de omlijning (27), met een lichte rand links (L).
   - Maan: sikkel met de hoorns omlaag, x5–14 (10 px breed, zelfde breedte als 1b, 5 rijen hoog).
     - Dik midden: 3 rijen (30–32, x8–11).
     - Hoorns lopen per rij 1 px naar buiten en omlaag tot een punt van 1 px: (5,34) links, (14,34) rechts.
     - Binnenkant: vacht met een S-schaduwrand direct onder het dikke midden (rij 33, x8–11), daaronder V.
     - Kleur: W boven/links, M aan de onderrand van het midden, m aan de rechterhoorn.
3. **Spiraalgat**:
   - Het gat is rond (rijen 31–34: 2-4-4-2 px).
   - De windinglijn (K) loopt via links, boven en rechts (x58) omlaag en eindigt via (57,33) in het gat.
   - De rest van de gatrand is D (schaduw van de binnenwinding), geen K. Zo is er één lijn die naar binnen draait, in plaats van een ring om een ring.
   - De binnenwinding wordt rechts smaller tot een punt bij het gat.
4. **Binnen het silhouet**:
   - **Ogen**: het nabije oog (rechts) is 3×2 met een lid van 3 px (K): W-glans, G-pupil, b boven, B/b onder. Het verre oog is 2×2, donkerder (G-pupil, geen glans), dus duidelijk kleiner en verder weg.
   - **Plooi romp/dij**: de D-voor (x29–31, rij 40–44) is S geworden, met één D-pixel van rij 43–44 die overgaat in de spleet van het silhouet.
   - **Vuist**: lichter dan de arm (L/V linksboven, knokkels L|L met V-groef, D-vingergroeven). De pols (rij 21) is donkerder (D), zodat de vuist loskomt van de S-onderarm.
   - **Dijrand**: het D/S-korrelpatroon bij de knie (x45–46, rij 49–50) is S geworden, zodat er één D-band (x43–44) overblijft.

## Checklist (SPRITE_NORM)
- 3/4 links-voor, ledematen, pose, omtrek: van 1b/silhouet, niet aangeraakt.
- Ogen geïntegreerd (lid, donker boven/licht onder, glans op het nabije oog): ok.
- Healerhand met de palm naar de tegenstander, vijf vingers: ok.
- Geen strepen of rugpatroon: ok.
- Omlijning: geen open randen. Zwart-aandeel van de omtrek 0,48 (1b: 0,50).

## Eerlijk: wat nog zwak is (1× en 3× naast 1b, het model en echte sprites)
- **Kop als geheel**: de maan leest op 3× als sikkel met vacht erboven en geen helmglans meer. Op 1× blijft de ronde vachtkap om het donkere gezicht met een witte boog erop nog wat aan een capuchon/helm doen denken. Dat komt door de kopvorm (bevroren silhouet en model), niet door de maan. Beter krijg ik het binnen deze zone niet.
- **Maanhoorns**: de punten zijn 1 px. Op 1× valt de linkerpunt (5,34) bijna weg, waardoor de sikkel daar als een boog leest.
- **Duim**: op 3× leest hij als duim, op 1× is het een klein uitsteeksel linksonder. De hand leest op 1× wel als open hand met vingers omhoog (vier lijnen, geen vlek meer).
- **Hand**: de vingers zijn recht (2 px breed laat weinig kromming toe). Drowzee's zachte kromming zit alleen in de toppen en de waaierhoogte.
- **Spiraal**: op 3× een spiraal met een rond gat. Op 1× nog vooral een krul met een gat; de lijn naar het gat is 1 px.
- Het verre oog is nu kleiner en donkerder. Of het sinister genoeg oogt, moet Jordi beoordelen; het nabije oog kijkt nu "wakker" met glans.

## Lessen
- Een override-bestand (`ronde1c.txt`) bovenop de bevroren `delen.txt` plus een zone-diff in `check.py` bewijst direct dat er buiten de zones 0 px veranderd is.
- Let op met override-strings: één teken te veel verschuift de rechterkant (kopomtrek) ongemerkt. Controleer de diff per zone, niet alleen de totale alpha-diff.
- Een sikkel leest pas als sikkel als het midden dikker is dan de hoorns, die naar 1 px aflopen, en als er vacht boven ligt. Een even dikke boog leest als hoofdband of vizier.
- Een spiraal leest als spiraal als de windinglijn in het gat eindigt en de rest van de gatrand een schaduwtint is in plaats van omlijning.
