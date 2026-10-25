# Olinguito v2: kleursprite ronde 1

**Bestanden:**
- `olinguito.png`: 64×64, geïndexeerd (mode P), 16 kleuren, index 0 transparant, opgeslagen met transparency=0.
- `vel.png`, met:
  - de sprite op 4× op licht en op donker, en op 1× op licht en op donker;
  - het gekozen ontwerp;
  - de vorige poging (`front.png`, afgekeurd) op 4× en 1×;
  - Linoone, Zigzagoon, Poochyena, Sentret en Furret op 4× en 1×.
- `bron/raster.txt`: het met de hand getypte raster (`y x pixels`, één letter per kleur).
- `bron/bouw.py`: zet het raster om naar de PNG en controleert het tegen het silhouet.
- `bron/vel.py`
- `bron/vorige_front.png`: kopie van de afgekeurde poging, als vergelijking.

## Bevroren silhouet: alpha-bewijs
Het silhouet komt uit `silhouet_hand/ronde5/silhouet.txt` (1174 px).
- `bouw.py` meldt **0 afwijkingen**: elke gekleurde pixel valt binnen het silhouet en elke silhouetpixel is gekleurd.
- Een losse controle (index ≠ 0 tegen `#`) geeft **alpha-diff 0**, met 1174 px.
- Er is dus niets verschoven, ook niet de ±1 die mocht.

## Game Freak-studie (Gen 3 `anim_front.png` + palet, bekeken op 6–10×)
| | tinten per kleurgroep | omlijning / selout | licht | schaduw volgt vorm | vachttextuur | oog / masker |
|---|---|---|---|---|---|---|
| **Linoone** | vacht 4 (d8c8b8, b8a090, a08878, 806858) + 2 donkere omlijningstinten (585048, 604f3e) + zwart 181818 | Zwart onder en rechts (buik, poten). Bovenrand en kop in donkerbruin 585048/604f3e. | Linksboven; de rug is het lichtst. | De strepen volgen de lijfboog; de buik is donker. | Strepen en kartelranden in de haarrichting; geen losse stippen. | Klein blauw oog: zwarte rand, witte glans linksboven, lichtblauw onderaan. |
| **Zigzagoon** | vacht 4 (e6decd, bdac9c, b49c8b, 947b6a) + bruin 524131 + zwart | Zwart bij pluk en schaduw, bruin 524131 aan de lichtkant. Veel zwarte haarlijntjes in de vacht. | Linksboven. | Kartelgrens tussen licht en donker. | Plukjes als korte zwarte/donkere V-streepjes. | Masker donkergrijs 414141 met een donkerder kern 202029 en zwarte rand. Oog bruin met een witte stip, binnen het masker. |
| **Poochyena** (donker type) | grijs 4 (b8c0c0, 9098a0, 505858, 303838) + zwart 101010 | Zwart rondom, maar aan de lichtkant 303838. | Linksboven; hooglicht als vlekken op kop en schouder. | Schaduw onderaan het lijf en aan de verre kant. | Pluimen aan de staart; weinig textuur in het lijf. | Geel oog met rood, zwart bovenlid. |
| **Sentret** | bruin 4 (cda483, bd835a, a4734a, 8b5a41) + donkerbruin 624131/4a3120 + zwart | Selout donkerbruin 4a3120 aan de buitenkant; zwart alleen onder. | Linksboven, met een groot licht vlak. | Ringen op de staart volgen de ronding. | Nauwelijks; tekenfilmstijl. | Kraaloog: zwart met witte glans. |
| **Furret** | crème 3 + bruin 3 (9c624a, 7b4139, 522920) + zwart | Donkerbruin 522920 als selout rond het lijf, zwart spaarzaam. | Linksboven. | Banden volgen de ronding. | Geen. | Kraaloog zwart met glans. |

**Samengevat:**
- 3–4 tinten per kleurgroep plus 1–2 donkere omlijningstinten.
- Zwart vooral aan de schaduwkant; aan de lichtkant een donkere tint van de kleur zelf (selout).
- Licht linksboven; de schaduw zit op de buik, aan de verre kant en onder de kop.
- Vacht wordt met een paar kartels en plukjes gesuggereerd.
- Een klein oog bestaat uit een zwart bovenlid, een witte glans en een lichtere iris aan de andere kant.
- Een masker is donkergrijs met een donkerder rand, niet egaal zwart.

## Palet (16, index 0 transparant)
| # | kleur | gebruik |
|---|---|---|
| 0 | 98d0a0 | transparant (zoals Game Freak) |
| 1 | 1c120e | omlijning (zwartbruin), schaduwkant |
| 2 | 3e261a | lijf donker: schaduw, selout van het lijf, verre poten |
| 3 | 603e28 | lijf basis (donkerbruin) |
| 4 | 805638 | lijf licht |
| 5 | 8a5c38 | warme kruin achter op de kop |
| 6 | 76685a | kop basis (grijsbruin) |
| 7 | 968878 | kop licht, binnenkant oor |
| 8 | 54483e | kop schaduw, snoet, selout van de kop |
| 9 | 322c2c | masker |
| 10 | 6e221a | oog donker roodbruin |
| 11 | a84630 | iris licht (onderkant) |
| 12 | f0eadc | klauwen licht, glans |
| 13 | a89e8c | klauwen schaduw |
| 14 | c48480 | oudroze: neus, voeten |
| 15 | 8c5252 | roze donker: schaduw van neus en voeten, verre voeten |

Het aandeel zwart (index 1) is 196 van 1174 px (±0,17): binnen de Gen 3-band, en passend bij een donker dier.

## Per Dragonfly Cave-regel (SPRITING.md §0–§8)
**§0, checklist:**
1. **Diagonaal:** het lijf staat 3/4 (B2, bevroren silhouet) en de kop meer naar de kijker. ok
2. **Ledematen:**
   - nabije voorpoot met 2 klauwen;
   - verre voorpoot als een donkere strook achter de nabije (x 27–30), met een donker roze pootje;
   - verre achterpoot in de schaduwtint met een donkerroze voet;
   - nabije achterpoot: dij als bol met licht linksboven, met een roze voet.
   - Alles is verbonden. ok
3. **Geen rechte lijnen:** het silhouet is bevroren. ok
4. **Oog:** één oog in beeld. Zwart bovenlid, witte glans linksboven, donker roodbruin en een lichtere roodbruine iris rechtsonder, in het masker. Niet feller gemaakt (SPEC). ok
5. **Leest op 1×** naast Linoone en Zigzagoon: zie het vel. ok, met de kanttekeningen onderaan.
6. **Formaat:** bevroren (1174 px). ok
7. **Pose:** bevroren. ok

**§1–2, met de hand:** elke pixel is getypt in `raster.txt`, per onderdeel (staart, oren, kop, lijf, poten, klauwen). Er zijn geen ellipsen, verlopen of automatische shading gebruikt. `bouw.py` vertaalt alleen letters naar kleuren.

**§3, curven:** de omtrek is bevroren. Binnenin volgen de grenzen tussen de tinten de vorm: de dijbol, de kopbol en de staartboog.

**§4, palet:**
- 3 tinten per hoofdgroep: lijf d/b/l, kop s/g/h, klauw n/w, roze q/p;
- daarbij de zwartbruine omlijning;
- kruin en masker elk één eigen tint.

**§5, licht en schaduw:**
- Licht van linksboven:
  - de rug en de linkerkant van de staart zijn licht;
  - het voorhoofd heeft een hooglichtvlek, niet als band langs de rand;
  - de dij is een bol met hooglicht linksboven en een donkere contourboog.
- De slagschaduw van de kop valt als een rij donker op borst en nek.
- De buik en de achterkant van de dij zijn donker, net als de verre poten.

**§6, oog en glans:** kraaloog met glans plus een lichtere iris tegenover de glans; de les over het mini-oog is toegepast.

**§7, textuur:** een paar plukjes in de schaduwtint op het achterlijf (x 39–46, y 31–34), en een gekartelde grens tussen kruin en grijze kop. Niet meer dan dat (Game Freak houdt het bij een paar).

**§8, omlijning:**
- **Zwart (1)** onder en rechts: kin, onderkant van de staart en de poten, achterkant van de dij.
- **Selout aan de lichtkant:**
  - kop: kopschaduw 8;
  - rug, staart en kruin: lijf donker 2.
- **Anti-aliasing:** nergens aan de buitenkant.
- **Klauwen:** zwart omlijnd met een zwarte scheidingslijn ertussen; de klauwen zelf zijn wit met grijs (zoals bij Linoone).

## Toets op 1× naast Linoone en Zigzagoon
De sprite leest als een donkerbruin klimdiertje met:
- een grijze kop met masker en een rood oog;
- een rond oor;
- een staart in een boog;
- lichte klauwen en roze voeten.

De kleuropbouw is nu die van Game Freak: 3 tinten per groep, selout in plaats van overal zwart, licht linksboven. Op donker blijft de omtrek leesbaar door de zwartbruine rand onderaan, en de bovenkant door de selout.

## Eerlijk: wat nog niet klopt
- **De kop leest nog wat als een helm:** het grijze vlak heeft een vrij strakke diagonale grens met de warme kruin. Op de onderlaag is dat ook zo, maar in pixels wordt het hard. Een zachtere, gekartelde overgang (meer pixels wisselen) kan dit beter maken.
- **Het lijf is overwegend donker:** het lichte vlak is een smalle strook op de rug. Game Freak-sprites (Sentret, Linoone) gebruiken veel meer hooglicht (§5, R/S-stijl). Vergeleken daarmee oogt de olinguito donker. Dat past bij Dark, maar de bolle borst leest nog weinig.
- **De verre voorpoot** is maar een strook van 1–2 px. Op 1× valt hij weg; je ziet vooral drie poten plus klauwen. Het silhouet laat niet meer ruimte.
- **Ruw tegenover Game Freak:** de wangen en de snoet onder het masker zijn grote, vrij egale vlakken in de kopschaduw.
- **Referenties op donker:** hun index 0 is niet als transparant gemarkeerd, dus op het vel staan ze op groen in plaats van op donker. Alleen de olinguito staat ook op donker.

## Lessen
- **Eerst de kleurklassen van de onderlaag op het silhouetraster afbeelden** (blokken van 4×4 meerderheid, gemarkeerd binnen en buiten het silhouet). Dat geeft per pixel waar masker, oog, neus, kruin en voeten horen, zonder te gokken.
- **Een raster als `y x pixels` laten controleren op lengte tegen het silhouet** vangt elke telfout meteen (hier 15 bij de eerste versie).
- **Een donkere zwarte onderrand onder een maskerband** leest als een vizier of spleet. Een donker randje alleen onder het oog, en de rest in de maskertint, oogt meer als Zigzagoon.
