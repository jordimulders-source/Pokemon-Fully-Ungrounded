# Olinguito ronde 16: kop, gezicht en staart (reparatie na de keuring van ronde 15)

Jordi na de keuring (`../ronde15/KEURING.md`): palet blijft donker (Dark-type), lijf/poten/armen/klauwen en pose blijven; alleen keuringspunten 2–4 (kop, gezicht, staart). Toon voortaan vergelijken met Dark-types.

**Bevroren:** `normal.pal` identiek aan ronde 15; delen `been_achter`, `lijf`, `been_voor`, `arm_achter`, `arm_voor` in `bron/delen_abs.txt` pixel voor pixel ronde 15 (gecontroleerd met diff). Snuit, neus, grijns met hoektand en crème onderkaak (x9–27, y30–38) letterlijk overgenomen uit ronde 15. Animatie ongewijzigd (kop, staart, armen 1 px omhoog in frame 2).

## Wat er veranderde
1. **Kop rond (punt 2):** bolle schedel met de top als boog (y22 x24–26 → y23 x21–28 → y24 x18 → y25 x16; runs 3 / 3+2 / 3 / 2 / 1). Achterkant bolt uit (x36, 37, 38, 38, 39×4, 38, 38, 37×3) in plaats van verticaal x37–39. Voorhoofd met een kleine stop vóór de snuit (x14 twee rijen). Kin zacht: y38 x16–18 → y39 x19–24 → y40 x25–30. Wang en kaak in basistint (niet meer schaduw), zodat de kop zich van de nek scheidt.
2. **Oren groter en rond:** nabij 7×6 (x29–35, y19–24) met crème binnenkant (7/6/5, niet roze), ver 6×5 (x15–20, y20–24) half achter de schedel, binnenkant in roomschaduw. Toppen y19–20 (was y22).
3. **Masker gebogen (punt 3):** twee lobben met een neusbrug van 3 px kopkleur (x20–22, y28–29); de nabije lob loopt achter het oog als vleugel omhoog (y27 x31–33) tot een punt naar het oor (34,26) en zakt onderaan naar (31–32, 35). De onderrand is een golf: verre kant y34, onder het nabije oog y33 (de crème wang komt omhoog tot y34 x22–29), vleugel y34–35. Boven elk oog een crème wenkbrauwboogje (nabij y26 x24–26 + uiteinden y27; ver y26–27 x16–19) met kopkleur ertussen. Masker blijft index 2 (44,28,28); leesbaar door de lichte rand eromheen (basis/hooglicht, crème wang en boogjes), niet door een lichter lijf.
4. **Ogen amandel (punt 3):** nabij: bovenlid zwart (x24–28, y29) met flick omhoog op de buitenhoek (29,28); iris donkergoud bovenaan, goud onderaan; pupil 2 px tegen het lid met glans linksboven (26,30); rijen 5-5-5-3; zijkanten en onderrand in maskerkleur, geen zwarte lijst. Ver: 3 px breed, 1 rij lager, glans 1 px. Blik schuin en half dicht (sluw), niet nors.
5. **Staart taps met haak (punt 4):** schacht met de hand per rij: rechts runs 4,4,4,4,3 (helt licht naar rechts), links runs 1,2,2,1,2,2,2,2,3; 9 px breed aan de voet (y35–38), 5 px bij y22. Bovenaan een haak die naar links terugkrult (kap y15 x53–56, punt omlaag tot (51,21)) met lucht in de bocht (x53–55, y19–21) en een donkere weerhaak (index 2/1) op de punt. Twee subtiele schuine ringen in schaduwtint (y25–26, y30–31), loodrecht op de helling.

## §0-checklist (SPRITING.md)
1. **Lichaam én blik diagonaal:** ok. Kop 3/4 naar links-voor (verre oor/oog kleiner, lager en in schaduw), lijf ongewijzigd 3/4.
2. **Geteld en verbonden:** ok. 2 oren, 2 ogen, neus, mond met hoektand, 4 poten, 4 klauwen, staart vast aan de romp. bouw9: geen open randen in frame 1 en 2 (ook geen schaduwkleur naast transparant; een eerste versie had er drie: oorvoet (34,24)/(35,25) en kin (24,39), opgelost).
3. **Geen rechte lijnen:** ok. bouw9: geen rechte randstukken > 4 px in beide frames (eerste versies: schedeltop 8 en 5, staartrand 5 en 6; alle gladgestreken). Kinrij y39 x19–24 (6) ligt tegen de arm en is geen buitenrand.
4. **Ogen geïntegreerd:** ok. Bovenlid donkerste lijn, iris donker boven/licht onder, glans, verre oog kleiner en geen kopie.
5. **Silhouet op 1×:** ok. Ronde teddykop met ronde oren, maskerband met golf, en een vraagteken-/haakstaart die op 1× leest (compare.png, licht en donker).
6. **Formaat:** 1170 / 1187 px (ronde 15: 1049). Groter door grotere oren en de bredere staartvoet. Fase 1-starters Gen 2–3 liggen op 602–903; polijstpunt 8 van de keuring (2–3 romp-kolommen eruit) is bewust niet gedaan, want het lijf is bevroren. Zie open punten.
7. **Pose niet stijf:** ok (ongewijzigd).

## Meting en toon
- Meest gebruikte kleur is nu de basis (3: 312 px) in plaats van de schaduw (2: 236); ronde 15 was schaduw 283 / basis 220. Palet zelf ongewijzigd.
- Naast Poochyena, Sneasel en Umbreon (compare.png): donker als Umbreon, het accent is het goud van de ogen (zoals Umbreons ringen/Poochyena's ogen), het masker leest als tekening.

## Open punten (niet gevraagd, niet gedaan)
- Keuring 5–8 (achterpoten, dijnaad, klauwen, formaat): het lijf is bevroren.
- Het gekozen concept B (rechtop zittend) versus de huidige sluiphouding: ontwerpkeuze voor Jordi (KEURING, ontwerpnotities).

## Lessen
- **Schedel als lijst van (y, links, rechts) met regels voor de vulling, details als overlay-segmenten** (`bron/kop16.py`): de omtrek valt in één oogopslag te controleren op runs, en masker/ogen/snuit liggen er los bovenop. Sneller en foutlozer dan hele rijen tellen.
- **Een staart met de hand per rij (links, rechts) uitschrijven**, niet met een formule: afronden gaf telkens rechte stukken van 5–6 px.
- **Een donker masker op een donkere kop wordt leesbaar door wat eromheen ligt:** basis/hooglicht rond de vleugel (schaduw naar de uiterste 2 px van de achterkant), crème wang die onder het oog omhoogkomt en wenkbrauwboogjes. Het lijf hoeft niet lichter.
- **Een haak leest op 1× pas met lucht in de bocht** (≥ 2 px) en een punt die terug omlaag wijst; een haakje van 3 px zonder gat leest niet.
- **Oorvoet aan de schaduwkant:** de onderste rij van een oor dat over de schedelomtrek steekt, eindigt ook met de omlijningskleur, anders ontstaat een open rand waar oor en schedel samenkomen.

## Bestanden
- `anim_front.png`, `normal.pal` (= ronde 15), `compare.png` (ronde 15 f1, ronde 16 f1/f2, Poochyena, Sneasel, Umbreon; 3× en 1× op licht en donker).
- Bron: `bron/kop16.py` schrijft de delen `kop` en `staart` in `bron/delen_abs.txt` (rest = ronde 15). Bouwen: `sh bron/bouw.sh <ronde16-map> [preview.png]`. Vergelijking: `python3 bron/vergelijk16.py <repo-root>`.
