# Lama fase 2: kleur ronde 2 (maker-agent, 2 nov)

Op het bevroren silhouet `../../silhouet/ronde2.txt` (1278 px, goedgekeurd), met de goedgekeurde vachtramp. Jordi (letterlijk): "ja hij moest wat meer fluffy zijn vooral". Afgekeurd (AFGEKEURD.md): hoekige poten, een poot als rechte lijn, doffe vacht met veel bruintinten, hert/geit-lezing, halsband als sjerp, aguayo als koffer, plat lijf. Diagnose: `DIAGNOSE.md`.

## Bestanden
- `lama.png` (P, 16 kleuren, transparency=0), `normal.pal` (JASC), `raster_grid.txt`.
- `vel.png`:
  - onderlaag, ronde 2 op 4× (licht en donker), ronde 1c op 4× ernaast, 1× (licht, donker en 1c);
  - op 3× en op 1× (licht en donker) naast de alpaca, Stantler, Flaaffy, Mareep, Ponyta en Girafarig.
- `bron/raster.txt`: met de hand getypt per onderdeel (`rij x0 pixels`).
- `bron/pas2.py` en `bron/pas3.py`: twee met de hand gekozen tintpassen, alleen wissels van letter in benoemde zones of op benoemde pixels, geen vormen. Zie de docstrings.
- `bron/bouw.py`, `bron/controle.py`, `bron/vel.py`, `bron/zoom.py` (+ `zoom_licht.png`, `zoom_donker.png`, 8×).

Bouwen: `python3 bron/bouw.py && python3 bron/controle.py && python3 bron/vel.py`. De passen zijn al in `raster.txt` verwerkt en hoeven niet opnieuw te draaien.

## Controles
```
mode P transparency 0 | pixels 1278 | alpha-diff 0
kleuren gebruikt: 16
open randen: 0
losse pixels: 57, allemaal bewuste details
```
De losse pixels zijn:
- oogglans (w) en blauwe reflectie (u);
- pompons (p/y/t) met hun schaduwpixel;
- nagels (h/l boven d) en de handschoenglans;
- de kwastpunten van de oren;
- ±10 hooglichtjes (h) op de wolpunten;
- het neusgat en de splitlip;
- de gewrichtspixels (knie/hak b) op de verre poten.

Er zit geen ruis in de grote vlakken.

## Palet (16)
| # | letter | kleur | gebruik |
|---|---|---|---|
| 0 | . | 98d0a0 | transparant |
| 1 | k | 2a161a | omlijning, alleen aan de schaduwkant (onder en rechts) |
| 2 | d | **6c3a20** | selout lichtkant, scheidingen, omlijning rechtsboven (overgang zwart → omlijningsbasis) |
| 3 | s | **a8683a** | schaduw, snuitmasker, verre poten |
| 4 | b | **d69a52** | basis karamel |
| 5 | l | **efc27a** | licht (hoofdtint van de wol) |
| 6 | h | **f8e2a8** | hooglicht: wolpunten, kruin, snuitrug, handschoennagels |
| 7–15 | q r m n y t p u w | ongewijzigd (1c) | rood, polsband/hoeven, halsband/aguayo, oog |

## Verdeling vachttinten (948 vachtpixels)
| tint | hele vacht | zonder de verre poten (825) |
|---|---|---|
| h f8e2a8 | 2,6% | 2,9% |
| l efc27a | **23,1%** | **26,4%** |
| b d69a52 | 19,8% | 21,9% |
| s a8683a | 34,2% | 28,7% |
| d 6c3a20 | 20,3% | 20,0% |

- **Zwart k: 128 px = 10,0%** van de sprite (was 13,5% vóór de omlijningspas, en 14% in 1c).
- In 1c was licht 6%; nu is licht de hoofdtint van de wol (±25%). De schaduw is hoger dan de 20% uit het plan doordat de verre poten bewust volledig in de schaduwtint staan (87 px s) en de buik een kernschaduw heeft. Dat is vergelijkbaar met Stantler (b48331 22% + 7b4100 17%).
- d is als lijnkleur (selout en scheidingen) 20%, verdeeld over alle randen. Er zijn geen donkere vlakken.

## Wat er per onderdeel gebeurde
- **Wol als klonten (fluffy):**
  - De wolhals heeft een lichte linkerkant (l/h), het midden b en de schaduwkant s. Onder elke klont loopt een rustige boog in b/s (r20 x21–23, r23 x22–23). De kop steekt uit de nekwol (d-naad achter het oor).
  - De borst (wolkraag) bestaat uit lichte klonten (l/h) onder de halsband.
  - De flank heeft drie klonten met een lichte bovenkant (r33–34) en een schulprand in s eronder (r36–37). De buik hangt in klonten (b-tongen in s).
  - Het achterwerk heeft twee lichte plukken. De staart is een lichte pluim met een hooglicht.
  - De wolmouw (opgetilde poot) en de wolbroek (nabije dij) zijn licht.
- **Gladde onderbenen:** de slanke onderbenen hebben alleen b/s met een d-rand links en een k-rand rechts, zonder wolpunten. Dat contrast laat de wol wolliger lezen.
- **Kop:**
  - De kruin heeft een wolkuifje (h/l) en het voorhoofd en de snuitrug zijn licht. Het snuitmasker in s zit alleen op de onderste helft van de snuit.
  - Neusgat k op (11,20) en de splitlip als donkere naad (14,22) in de stompe snuit.
  - Het oog is zoals in 1c: zwart bovenlid, glans, blauwe reflectie, de d-wenkbrauw direct op het lid.
  - Banaanoren met rode kwast aan de punt; het verre oor in de schaduwtint met een donkere kwast.
- **Kleding:**
  - De halsband is een ring om de wolhals: een U met t/y-blokjes, een rode rij (q vooraan) en een rand m. Vijf pompons van 2 px hangen aan de onderkant. Rechts draait hij in r/m achter de hals weg.
  - De aguayo, de handschoenen (polsband n, lichte nagels) en de verre handschoen komen uit 1c en staan op dezelfde plek.
  - De rechte rechterrand van de nabije handschoen is rond geschaduwd: de hoeken (27,51) en (27,55) zijn m en de binnenkolom m.
- **Verre poten:**
  - volledig in de schaduwtint s, met de lichtkant in d en zwart alleen rechts;
  - een paar b-pixels als licht op de wolmouw (r43–44) en als gewricht (knie (33,50), hak (43,51)).

## Eigen keuring (4×, 3× en 1×, licht en donker, naast 1c, Stantler, Flaaffy en Mareep)
- **Pokémon-kleur:** warm goud-karamel, helder en met hue-shift, naast Stantler in dezelfde familie. Op donker leest het warm, niet modderig.
- **Fluffy:** hals, borst, flank, buik, mouw, broek en staart lezen als wolklonten, met gladde poten eronder. De hertenlezing van 1c is weg.
- **Lama:** dikke lichte wolhals, kleine kop met banaanoren en rode kwasten, stompe snuit met masker, en een rechte rustige stand.
- Ik zie geen zelfgenoemd zwak punt dat nog gerepareerd moet worden.

## Lessen
- Wollig lezen komt door contrast: klonten met een lichte bovenkant en een schulprand in de schaduwtint, tegenover gladde onderbenen met maar twee tinten.
- Een hoofdtint licht van ±25% vraagt dat je meteen bij het typen licht neerlegt op elke bovenkant. Achteraf ophogen kostte een aparte pas.
- Om zwart ≤ 10% te houden bij dunne poten: laat de omlijning langs de omtrek overgaan van zwart (onder en rechts) naar de omlijningsbasis d (rechtsboven: oren, achterhoofd, nek, achterwerk boven), zoals in SPRITING §8.
