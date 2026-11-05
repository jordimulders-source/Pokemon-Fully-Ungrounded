# Lama fase 2: kleur ronde 1 (maker-agent, 2 nov)

Op het bevroren silhouet `../../silhouet/ronde1b.txt` (1188 px, goedgekeurd: "goedgekeurd en laat het bij de rustige lama stand passen, want dat is vrij iconisch").

## Bestanden
- `lama.png`: 64×64, mode P, 16 kleuren (alle 16 in gebruik), index 0 transparant, opgeslagen met transparency=0.
- `normal.pal`: JASC-PAL.
- `raster_grid.txt`: de sprite als tekstraster (één letter per paletindex), gegenereerd uit `bron/raster.txt`.
- `vel.png`:
  - de onderlaag, de lama op 4× (licht en donker) en de alpaca (fase 1) op 4×;
  - de lama, de alpaca, Girafarig, Stantler, Ponyta, Mareep en Mightyena op 3×;
  - dezelfde op 1×, licht en donker.
- `bron/`:
  - `raster.txt`: met de hand getypt, `rij x0 pixels`, per onderdeel;
  - `bouw.py`: letters naar paletindex, PNG en pal, met een controle op dubbele pixels en tegen het silhouet;
  - `controle.py`: alpha-diff gelezen uit de PNG, open randen, losse pixels;
  - `klassen.py` / `klassen.txt`: kaart van de onderdelen uit de onderlaag. Alleen als kaart gebruikt; er is niets uit gekopieerd;
  - `vel.py`;
  - `zoom.py` en `zoom_licht.png` / `zoom_donker.png` (8×).

Opnieuw bouwen: `python3 bron/bouw.py && python3 bron/controle.py && python3 bron/vel.py`

## Bewijs
```
mode P transparency 0 | pixels 1188 | alpha-diff 0
kleuren gebruikt: 16
open randen: 0 []
```
De open randen zijn getoetst als randpixels naast transparant die geen omlijningskleur (k, d, m, n) zijn. Het script vindt 45 "losse pixels", allemaal bewust:
- oogglans en de reflectie in het oog;
- pompons en hun schaduwpixel;
- nagels;
- de glans op de handschoen;
- een paar hooglichtjes (h);
- de 1 px brede binnenkant van de oren.

Er is geen ruis in grote vlakken.

## Game Freak-studie (anim_front_gba, eerste frame, op 6–8×)
| | tinten per groep | selout / zwart | licht | vacht/wol | oog |
|---|---|---|---|---|---|
| **Stantler** (bruine hert-viervoeter) | vacht 4 (ffde83, e6b45a, b48331, 7b4100) + 101010 | bruin (b48331) als selout aan de lichtkant, zwart onder en rechts | linksboven; **veel lichte tint** op rug, hals en dij (R/S-stijl) | spieren als lichte vlakken met gebogen schaduwgrens | klein en donker, met een lichte rand |
| **Girafarig** (langnek) | geel 4 + olijf 4 + zwart | gekleurde selout boven en links, zwart onder | linksboven; poten met een lichte voorkant en een donkere achterkant | vlekken als rustige vlakken | kraaloog met glans |
| **Ponyta** | crème 4 + vuur 4 | lichte selout bovenop, donker onder | linksboven; verre poten in de schaduwtint | – | groot en donker met glans |
| **Mareep / Flaaffy** (wol) | wol 3–4 + zwart | wol met een gekartelde rand en bobbels in de omtrek | linksboven | **wol = rustige grote vlakken, de kartel zit in de rand en in de schaduwgrens**, geen spikkels | – |
| **Mightyena** | donker 4 + grijs 3 | zwart aan de schaduwkant | linksboven | vacht in plukken aan de rand | zwart bovenlid |
| **Alpaca (fase 1, familie)** | crème 4, rood 4, omlijning 281628 (paars-zwart) | paars-zwart rondom, de schaduwtint als selout links | linksboven | grote rustige vlakken | 3×4: bovenlid 2 px, glans middenboven, **gekleurde reflectie rechtsonder** (paars) |

**Toegepast:**
- Omlijning bijna-zwart warm (2a161a, familie van de alpaca 281628) aan de schaduwkant. Aan de lichtkant is de selout gekleurd: d (bruin) voor de vacht, m voor rood en doek.
- Licht van linksboven:
  - een lichte strook op de voorkant van kop en hals, op de borst, de dij en de voorkant van de nabije poten;
  - schaduw (s) onder de doek, op de buik en het achterwerk, met een gekartelde grens (wol);
  - de verre poten in s/d met een k-rand.
- Oog naar het alpaca-oog:
  - 3×4, bovenlid zwart, glans (w) bovenin, reflectie rechtsonder in blauw (u, uit de aguayo, zoals de paarse reflectie van de alpaca);
  - een donkere wenkbrauwschaduw (d) direct op het bovenlid, naar voren omlaag. Dat geeft de brutale tienerblik, niet boos;
  - één oog (lange snuit).

## Palet (16, index 0 transparant)
| # | letter | kleur | gebruik |
|---|---|---|---|
| 0 | . | 98d0a0 | transparant (zoals de alpaca) |
| 1 | k | 2a161a | omlijning schaduwkant, oog, neusgat, mond |
| 2 | d | 74401f | vacht donker: selout lichtkant, kopschaduw, scheidingen, wenkbrauw |
| 3 | s | a86a3a | vachtschaduw = kop basis (poppetje #A86A3A) |
| 4 | b | c88e55 | vacht karamel basis (poppetje #C88E55) |
| 5 | l | e2b47c | vacht licht |
| 6 | h | f6dcae | vacht hooglicht (6 px) |
| 7 | q | f2705e | rood licht (handschoen, oorkwast, doek) |
| 8 | r | d8343c | rood basis (handschoen, oorkwast, doek, halsband) |
| 9 | m | 98203a | rood schaduw, selout van doek en handschoen |
| 10 | n | 4a3c40 | donkergrijs: polsband, nagels, hoeven |
| 11 | y | f8c030 | geel: halsband, pompon, doek (= alpaca f8c030) |
| 12 | t | 20aca8 | teal: halsband, pompon (= alpaca 20aca8) |
| 13 | p | de3084 | roze: doekrand, pompons (= alpaca de3084) |
| 14 | u | 4c5ca8 | blauw: doek; reflectie in het oog |
| 15 | w | faf6ec | glans oog en handschoen |

Gedeelde tinten: het aguayo-rood is hetzelfde rood als de handschoen en de oorkwast. Geel, teal en roze komen van het halsbandje van de alpaca (familie).

## Per onderdeel (kleurindeling volgt de onderlaag, `bron/klassen.txt`)
- **Vacht:**
  - effen karamel, iets donkerder dan de crème alpaca;
  - de kop een tint donkerder (basis s), met de lichte voorkant b/l;
  - de wol als rustige vlakken met een gekartelde schaduwgrens, de plukken in de omtrek uit het silhouet.
- **Oren:** de nabije met een rode kwast (q/r/m) aan de punt, de verre met een rode punt in de schaduwtint.
- **Snuit:** neusgat k vooraan, splitlip als donker inkepinkje (k) in de donkere mond (d), de kin met een k-onderrand.
- **Halsband (leitmotif):**
  - drie strepen t/y/r die als een U om de halsbasis lopen, laag aan de voorkant;
  - eronder 5 pompons (p, y, t, p, y), elk met een schaduwpixel;
  - op 1× leest hij als een gekleurde halsband.
- **Aguayo op de rug:**
  - strepen roze, blauw (2), geel, rood (3), met een m-zoom;
  - de strepen buigen aan beide uiteinden 1 rij omlaag (de doek valt over de ronde rug) en de hoeken hangen lager;
  - rood met q links en m rechts; slagschaduw s op de vacht eronder.
- **MMA-handschoenen:**
  - rood q/r/m met een glanspunt (w), zwarte polsband (n met k-rand);
  - de twee donkere teennagels (n) aan de voorkant onder de handschoen;
  - de verre handschoen in de schaduwtint (r/m, minder q).
- **Poten:** nabij met een d-rand links, b/l en s rechts; ver in s/d met een k-rand. De achterhoeven zijn donker met twee nagels (n).

## Checklist (SPRITING §0 + SPRITE_NORM)
1. 3/4 naar links-voor, kop meer naar de kijker: ok (bevroren silhouet).
2. Alle ledematen, oren en ogen geteld en verbonden: 4 poten, 2 oren, 1 oog; de verre poten in de schaduwtint. Ok.
3. Geen rechte lijnen waar het dier rond is: silhouet bevroren. De doekstrepen buigen mee met de rug. Ok.
4. Ogen geïntegreerd (bovenlid, glans, reflectie, één oog bij de snuit): ok.
5. Silhouet leest op 1× als de soort: ok (goedgekeurd); in kleur leest het op 1× als een lama met doek, halsband en rode handschoenen.
6. Formaat: 1188 px, fase 2 (fase 1 is 1019).
7. Pose niet stijf: goedgekeurde rustige lamastand (Jordi: "vrij iconisch").
- Norm 9 (omlijning per kleurgroep, zwart alleen aan de schaduwkant, licht linksboven, geen open randen): ok, 0 open randen (script).
- Norm 10 (geen Chernobyl, geen beige vlakken uit het niets): het hooglicht h zit alleen in 6 punten op belichte plekken.
- Valkuilen uit stap 3:
  - helm: de kop is één kleurfamilie met een gebogen grens kop/hals;
  - ruis: plukken alleen in de omtrek en in de schaduwgrens;
  - plat: lichte voorkanten en een donkere buik;
  - mini-oog: het oog is groot en heeft een glans;
  - de verre poten zijn gescheiden met s/d en een k-rand;
  - losse pixels: alleen bewuste details.

## Eerlijk: wat ik zelf zie
- Naast Stantler en Ponyta is de lama donkerder en minder glanzend. Dat komt door de keuze "iets donkerder dan de alpaca" en "effen karamel"; ik heb wel een hooglichtpas gedaan (voorkant van kop, hals, borst, rug en dij).
- De halsband loopt schuin over de halsbasis, zoals in de onderlaag. Op 1× leest hij als halsband; op 3× ook als een sjerp-achtige band.
- De doek is groot en fel en springt eruit; in het poppetje is hij net zo groot.

Ik zie geen zwak punt dat ik zelf nog zou repareren. Een keurder moet de kop op 3× beoordelen (een tiener-lama of te veel paard/hert?): dat is een smaakvraag over het bevroren silhouet, niet over de kleur.

## Lessen
- Een getypt raster dat per rij uit benoemde stukken bestaat (de vacht links, de doek in het midden, het achterwerk rechts) houdt elke rij nameetbaar. Laat een script na elke wijziging de rijlengtes tegen het silhouet toetsen; mijn eerste versie had 12 pixels fout door verkeerd getelde rijen.
- De streepdoek las als een plat rechthoekig plakkaat tot de strepen aan beide uiteinden 1 rij zakten en de hoeken lager hingen (Furret-banden: strepen volgen de ronding).
- Kleine spikkels s/b in de flank lezen op 4× als ruis; één gekartelde grens tussen b en s is rustiger.
- Een hooglichtpas met maar 6 h-pixels en een paar l-pixels op de voorkanten maakt de sprite al merkbaar minder modderig. Plan het hooglicht meteen in plaats van achteraf.
