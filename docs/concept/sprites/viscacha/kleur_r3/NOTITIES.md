# Viscacha frontsprite, kleur ronde 3 (maker-agent, regels uit docs/lessen/GEMINI.md)

## Aanpak
1. **Onderlaag** (`onderlaag.py` → `gemini64.png`, `onderlaag.txt`): het Gemini-plaatje verkleind met dezelfde schaal en positie als het silhouet (1:9,97, offset 1,10) en gekwantiseerd naar het palet (vlaktinten + 1), alleen binnen silhouet_r2.
2. **Vergelijking onderlaag ↔ r2:**
   - Gemini-lijf en -kop zijn overwegend licht zand (5), met oker (4) alleen als schaduw rechts en onder; r2 was overwegend 4.
   - Het nabije oor heeft in Gemini een grote donkere binnenschelp (x17–21, rij 14–19); in r2 was die smal.
   - De wangpluk is in Gemini een sikkel "(" op de wang (voet x15–17, rij 30–33, horen naar rechtsboven tot (24,26)); r2 was een schuine band.
   - Buik: in Gemini een lichte crème vlek met donkerder crème (6) langs de onderkant.
3. **Met de hand opgeschoond en gerepareerd** (`reparaties_r3.py`, zones A–D op het r2-raster). Geen kale scriptuitvoer: de onderlaag is alleen als gids gebruikt.

## Diff r2→r3 (289 px)
| zone | px | wat |
|---|---|---|
| A oor (Gemini) | 13 | Nabij oor: binnenschelp B/C over x18–21, rij 14–19 (rand 5 aan de lichtkant, 1 px), zoals in Gemini. |
| B wangpluk/kopcontour | 35 | Sikkel op de kop: punt (21–24,26) en (20–22,27) buiten de kop, breedst rij 29–31 (x15–18), voet afgerond op (15–17,32) met een 8-randje op (15–16,33). Daaromheen 1–2 px kopvacht (4) en de eigen kopcontour als tapse binnenlijn: 2 op (21,28)–(21,31), (20,32), (18,33), daarna 3 op (16–17,33–34) → (12–16,35). Kaakschaduw 4 als korte sikkel (10–17,33–35). De 2-lijn en de 33-strook naast het geel (de "riem") zijn weg. |
| C snuit/kin | 9 | Losse 2 op (5,33) weg. Mondlijn: (4,31) 2, aansluitend op de randpixel (3,31). Neus nu als 2 px donker óp de punt (1,28)–(1,29) i.p.v. een inkeping (2,29). Kin: (5,36) en (6,36) F, een ronder hoekje. |
| D rug/lijf/buik | 232 | Rug als boog. Lijf licht (5) zoals Gemini. Schaduw als sikkel om de bil: 4 dun bovenaan (42,31), breder naar onder (35–40, rij 41–45); 3 als binnenste sikkel aan de achter- en onderkant (43–44 vanaf rij 36, breed onderaan). De dijlijn (rechte naad) is weg. Een vormgevende overgang 4 voor de buik (23–25, rij 40–46). Nekschaduw 4 onder de kop (19–23, rij 28–34). Crème buik: bovenrand als boog (28–30,41) → (27–31,42) → (26–32,43), donkere crème 6 als sikkel langs de onderkant (rij 45–50). |

**Silhouet** (t.o.v. silhouet_r2, 4 px weg): (34,27), (35,27), (36,27) en (38,28). De rug loopt nu in stukken van 4–6–4–3–2–1–1 px: (24–27,28), (28–33,27), (34–37,28), (38–40,29), (41–42,30), (43,31), (44,32). Nieuw silhouet: `silhouet/silhouet_r3.txt`.

## Afwijkingen van Gemini (bewust)
- **Wangpluk** iets kleiner en hoger dan in Gemini: de onderpunt (Gemini ±(17–18,34)) eindigt op rij 33 boven de kaaklijn, en er ligt 1–2 px kopvacht tussen het geel en de kopcontour. Reden: zo blijft het geel op 1× op de kop en leest het niet als kraag (keuring r1 en r2).
- **Snorharen** weg: in Gemini dunne grijze lijnen, op 64 px rommelig.
- **Lichtrichting** consequent linksboven: de schaduw is een sikkel om de bil. In Gemini is de vacht vlakker, met een donkerder rand.
- **Rug**: de vachtpiek (losse haren, afgekeurd in de SPEC) staat er niet in, en de contour is een gladde boog.
- **Verre oor**: de binnentint staat rechts (C); in de Gemini-onderlaag is het oor aan beide kanten donker, wat bij Gemini een omlijning is.

## Controle (`controle_uitvoer.txt`)
- Silhouetdiff t.o.v. r2: 4 px, allemaal in zone D (rug).
- Open randen 0, losse pixels 0.
- Clusters < 3 px: alleen het oog (E, D) en de gele kern (57,12) in de pluimtop, die keuring r1 vroeg.
- 16 kleuren incl. transparant; png = raster.
- Keurvel: `vel.png` (werk naast `gemini64.png`, r2, Pachirisu en Dedenne; close-ups van kop en lijf).

## Niet gedaan / zwakke punten
1. Kinlijn (6–10,37) is nog recht; ronden kan alleen in het silhouet (de randpixels moeten een lijnkleur houden).
2. Onderrand van de verre voet (22–29,58) en de knik in de scheen (44–49,55–58) niet aangepakt (keuring r2 punt 6, laag in prioriteit).
3. De wangpluk is kleiner dan in Gemini (zie boven); als Jordi de Gemini-maat wil, moet hij lager doorlopen tot (17–18,34), met het kraagrisico.
4. Het lijf is lichter dan in r2; de rug heeft geen aparte hooglichtplaat meer, zodat het grote 5-vlak vlak kan ogen (de bilsikkel moet het lijf rond maken).
Niets gecommit.
