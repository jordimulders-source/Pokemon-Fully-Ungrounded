# Keuring lama fase 2, kleur ronde 2b (verse, onafhankelijke keurder, 2 nov)

Eerst zelf geoordeeld (1×, 3×, 8×, licht en donker, naast de alpaca, ronde 1c, het ontwerp `lijn_ronde2.png`, foto 1 en 13 Gen 3-sprites: Stantler, Girafarig, Ponyta, Rapidash, Mareep, Flaaffy, Ampharos, Altaria, Mightyena, Linoone, Furret, Eevee, Marshtomp; `anim_front.png` frame 1 + `normal.pal`). Pas daarna NOTITIES.md (2b, 2) en `ronde1b/KEURING.md` gelezen. Vel: `keuring_vel.png` (boven 1× en 3× op licht en donker; onder de FAIL-zones op 8× met rode kaders, raster om de 5 px).

## Technische controle (script)
- `lama.png`: mode P, 64×64, transparency 0, 16 kleuren gebruikt.
- **Alpha-diff met `silhouet/ronde2.txt`: 0** (1278 px). Silhouet ongewijzigd.
- Vachtramp ongewijzigd: f8e2a8/efc27a/d69a52/a8683a/6c3a20 (+ 2a161a zwart).
- Open randen (vul-/lichtkleur naast transparant): **0**. Zwevende pixels: **0**.
- Geïsoleerde pixels (geen 8-buur met dezelfde index): 71; de meeste bewust (oog, halsbandpatroon, nagels). Echte vachtspikkels: zie V2.
- Rechte randlopen ≥ 4 px (alle in het bevroren silhouet): achterhoofd x21 y9–13 (+ oor y7–8), handschoen rechts x27 y49–55, handschoen onder x28–34 y62 (grond, ok), aguayo boven y25 x38–43.
- Tintgebruik vacht: s 329 px (44%), l 206, b 193, h 27. Schaduw is de grootste vachttint.

## Tabel

| # | Punt | Oordeel | Waar | Reparatie |
|---|---|---|---|---|
| N1 | Leest op 1× als een echte Pokémon | PASS | geheel | Houdt stand naast Stantler/Ponyta/Girafarig; duidelijk lichter en warmer dan 1c. |
| N2 | 3/4 links-voor, kop meer naar de kijker, één oog | PASS | kop x10–22 | Eén oog, snuit linksonder, verre poten rechts/hoger in schaduw. |
| N3 | Ledematen tellen, verre in schaduw, gewrichten | **FAIL** | verre voorpoot x30–36 y41–56 | Vier poten tellen. Nabije achterpoot heeft een hak (y49–52), nabije voorpoot een buiging (y44–45). De verre voorpoot is een effen s-paal zonder knie; (33,50) is één losse b-pixel. → zie R2. |
| N4 | Geen Escher | PASS | | Nabije dij (x45–50 y41–45) ligt over de verre achterpoot; poten aan schouder/heup. |
| N5 | Geen rechte lijnen waar het dier rond is | **FAIL** (kleur) | buik y38 x22–49 | Een doorlopende s-band van 28 px leest als liniaal (zelfde fout als 1b punt 4). → R1. Rechte silhouetranden: zie "Voor Jordi". |
| N6 | Kopgrootte | PASS | y2–23 | ±34% (fase 2: 30–35%). |
| N7 | Ogen geïntegreerd | PASS | x17–19 y13–16 | Zwart bovenlid, glans (18,14), lichter blauw onder (19,16); lijn van de alpaca (bijna zwart). |
| N8 | Kenmerken op 1× leesbaar | **FAIL** | snuit, nagels | Splitlip en nagels lezen niet → R4, R5. |
| N9 | Omlijning per kleurgroep, zwart alleen aan de schaduwkant | **FAIL** (klein) | (37,24), (45,24), (51,24) | Drie zwarte k-pixels aan de bovenkant (lichtkant). (45,24) zit als nopje op de aguayo → R3. Rest ok: lichtkant d, schaduwkant k, rood met m. |
| N10 | Geen Chernobyl | PASS | | Geen misvorming, niets zwevend. Het grijze blok op de aguayo is een vlak uit het niets → R3. |
| V1 | Kop als helm | PASS | kop | Eén familie, licht links, snuit in s. |
| V2 | Ruis | **FAIL** | romp y35–38; spikkels (23,35), (28,32), (32,33), (33,50), (43,51), (48,56) | Schulpen op exact x34, x40, x46 (om de 6 px, gelijke vorm) lezen als stempel/hark → R1. Losse h/b-spikkels opnemen in een klont of weghalen. |
| V3 | Plat (2D) | **FAIL** | romp y32–38 | Romp = drie horizontale banden over de volle breedte (l y32–34, b y35–37, s y38): dezelfde "trappetje"-fout die in 2b uit de hals is gehaald → R1. |
| V4 | Mini-oog | PASS | | n.v.t. (licht gezicht). |
| V5 | Verre ledematen in schaduwtint, gescheiden met de basis | PASS | | Verre poten links d, rechts k (1b-reparatie gelukt); k op x38–40 y41–44 valt in de buikschaduw. |
| V6 | Open randen / losse pixels (script) | PASS | | 0 / 0. |
| J1 | Jordi: "poten te hoekig" | PASS | poten | Silhouet ronde 2 (door Jordi goedgekeurd) heeft gelijkmatige 1-px-stappen, knie/hak; de kleur volgt de cilinders (licht links). Alleen de handschoenen zijn nog blokken (Voor Jordi). |
| J2 | Jordi: "1 is een rechte lijn" | **FAIL** | verre voorpoot x30–36 y41–56 | Vorm heeft een lichte S, maar in effen s leest hij op 1× nog als bruine paal → R2. |
| J3 | Jordi: "kleurgebruik nog niet helemaal pokemon like, vooral de vacht" | **FAIL** | romp | Ramp en hals zijn goed (de hals leest nu als wol). De romp is gestreept en gestempeld; Game Freak (Stantler, Ponyta, Mareep) legt één ronde lichtvlek linksboven en laat de schaduw de vorm volgen → R1. |
| J4 | Jordi: lama-herkenning | PASS | geheel | Banaanoren met rode kwasten, wolhals breder dan de kop, stompe snuit, staart omhoog, aguayo: leest op 1× als lama, niet meer als hert. |
| J5 | Jordi: "meer fluffy" | **FAIL** | romp, buik | Hals, borst en staart zijn wollig; de romp (grootste vlak) leest als kortharige vacht met banden. → R1: de hals-recept (verspringende klonten) ook op de romp. |
| K1 | Halsband als ring (leitmotif) | PASS | x17–31 y25–33 | U-band om de hals die rechtsboven (30–31,25–26) achter de nek wegdraait; op 1× een kleurige halsband zoals bij de alpaca. Pompons: Voor Jordi. |
| K2 | Aguayo-doek | **FAIL** | x36–52 y24–32 | Grijs blok n (45–47,28)/(45–46,29) naast het blauw + zwart nopje (45,24) erboven lezen als slot en handvat: koffer (AFGEKEURD) → R3. |
| K3 | MMA-handschoenen met nagels | **FAIL** | (21,55),(23,55); (28,61),(30,61) | Rood + grijze polsband lezen; nagels zijn 1 px h tussen rood en zwart en vallen op 1× weg → R5 (en Voor Jordi). |
| K4 | Oorkwasten | PASS | y2–4 | Rode toppen op beide oren lezen op 1×. |
| K5 | Banaanoren | PASS | x12–23 y2–9 | Beide oren buigen in het midden naar buiten met de punt naar binnen. |
| K6 | Splitlip | **FAIL** | x10–17 y19–23 | Neusgat k (11,20) plakt aan de omlijning (leest als dikke rand); de mond (12–17,22) is een zigzag k/d die als open bek/donkere kin leest → R4. |
| L1 | Dezelfde lijn als de alpaca | PASS | | Rode handschoenen met band, rode oorkwasten, halsband, bijna zwart oog. |
| L2 | Evolutie | PASS | | Groter, langere hals, donkerder vacht, aguayo erbij; ruimte voor fase 3. |

## Reparaties (alleen kleur; alpha-diff 0; buiten de zones pixeldiff 0)

- **R1 Romp: banden en stempel → wolklonten** (x20–50, y31–38). Breek de lichtband y32–34: één ronde lichtvlek op de schouder/flank linksboven (ongeveer x22–38), naar rechts aflopend in b; 2–3 klonten van verschillende maat, diagonaal verspringend, elk met l/h-kap en een s-boog rechtsonder (het recept van de hals in 2b). Vervang de drie gelijke schulpen (x34/40/46, y35–37) door 2 ongelijke. Laat de b in het midden (x30–42) tot y38 zakken zodat de s-band geen liniaal meer is. Spikkels (23,35), (28,32), (32,33) laten opgaan in een klont. **Budget ±45 px.**
- **R2 Verre voorpoot: knie** (x30–35, y44–56). Een smalle b-strook aan de voorkant (links, naast de d) die de S volgt, met een knie van 2×2 b rond (32–33,48–49); (33,50) daarin opnemen. Rest s, rechterrand k. **Budget ±10 px.**
- **R3 Aguayo: geen koffer** (x36–52, y24–31). Grijs n (45–47,28), (45–46,29) → schaduw van de strepen (m/k), zodat de doek naar rechts over de rug wegbuigt i.p.v. een slot te tonen. Nopje (44–45,24) → m m (kwastje van de doek). (37,24) en (51,24) k → d. Per streep links 1 px lichter waar het palet het toelaat (q voor rood, h voor geel). **Budget ±12 px.**
- **R4 Snuit: neusgat en splitlip** (x10–17, y19–23). Neusgat naar (12,20) (één pixel binnen de rand; (11,20) terug naar d/s). Splitlip als verticale d-naad van 2 px op x13 y21–22; (14–15,22) naar s zodat er een lichte onderlip onder de mondlijn ligt. **Budget ±6 px.**
- **R5 Nagels** (21,55),(23,55),(28,61),(30,61). Binnen het silhouet kan een nagel maar 1 px hoog; maak ze leesbaarder door de pixel ernaast in de rand (22,55) en (29,61) donker (m) te houden en de d eronder op (21,56),(23,56),(28,62),(30,62) als s te zetten (nagel 1×2, licht boven, schaduw onder). Lukt het op 1× niet: Voor Jordi. **Budget ±4 px.**
- **Spikkels** (43,51), (48,56) opnemen of weghalen. **Budget 2 px.**

## Eindoordeel: **BIJNA**
Silhouet exact, ramp exact, geen open randen; hals, kop, oren, halsband en lama-lezing zijn goed. Open: R1 romp (±45), R2 verre voorpoot (±10), R3 aguayo (±12), R4 snuit (±6), R5 nagels (±4), spikkels (2). **Totaal ±80 px**, buiten deze zones pixeldiff 0.
R1 is de kern: dat is precies Jordi's "kleurgebruik, vooral de vacht" en "meer fluffy". Lukt R1 in één ronde niet (weer banden of stempels), dan stoppen en de romp eerst als krabbel met Jordi kiezen (2-rondesregel).

## Na het lezen van NOTITIES.md en de oude keuring
- De maker werkte in 2b alleen aan de hals en zag "geen zwak punt"; de hals is inderdaad opgelost. De romp heeft dezelfde bandfout, maar viel buiten zijn zone.
- Uit 1b zijn opgelost: verre poten met zwart aan de lichtkant, halsband als ring, spikkels (36,36)/(40,36). **Nog open uit 1b:** buiklijn als liniaal (1b punt 4, nu y38 in s i.p.v. d), nagels (1b punt 3, derde keer), aguayo plat/hoekig (1b punt 2; nu met grijs blok).
- `bron/pas2.py`/`pas3.py` wisselen tinten per regel in zones (b→l op de lichtkant). Dat is een scriptkleuring en verklaart waarschijnlijk de banden over de volle breedte; R1 met de hand typen (zoals `hals.txt`).

## Voor Jordi (smaak / bevroren silhouet, geen opdracht aan de maker)
- **Handschoenen zijn blokken:** rechte rand x27 y49–55 en vlakke bovenkant; MMA (open vingers) is op 64 px niet te tonen. Nagels van 2 px vragen 1 px silhouet onder elke handschoen. Accepteren als "rode handschoen met nagels", of 4 px silhouet vrijgeven?
- **Achterhoofd recht** (x21 y9–13, silhouet ronde 2). Klein; alleen met silhouetwijziging te verhelpen.
- **Pompons van de halsband** zijn 1-px-stippen (confetti), geen 5 pompons zoals in het ontwerp. Dit is de derde ronde voor de halsband; niet doorpatchen maar Jordi laten kiezen: zo laten, of 3 pompons van 2 px.
- **Formaat** 1278 px = 1,25× fase 1 (norm 1,5–1,7×); door het goedgekeurde slanke silhouet. Ter kennisname.
- Het oog blijft klein en "brutaal" t.o.v. de alpaca (past bij het ontwerp).
