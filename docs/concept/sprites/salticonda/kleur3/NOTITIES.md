# Salticonda – kleurronde 3: alleen een nieuwe kop (3/4)

Jordi (letterlijk):
- Over E: "teveel zijaanzicht, plus het lijkt qua hoofd niet echt op een evolutie van silicobra, zijn hoofd is bijna hetzelfde als silicobra."
- "gast elke sprite moet in driekwart gemaakt worden, kijk naar silicobra. En jij wil het volledig in zijaanzicht zetten. En wat is daar zijaanzicht aan? Het hoofd overduidelijk. Het lichaam maakt niet uit, maar we kijken volledig horizontaal op het hoofd"
- Over kleur2: "wat een misvormde hoofden [...] Lijken op alternatieve vormen van Onix maar dan een drol vorm".
- Aanvulling: "ik wil het sandaconda hoofd als motief, dus iets groter dan silicobra, de neusbult, kijken naar anaconda bronmateriaal, gewoon dat het een volgroeide slang lijkt".

## Bestanden
- `salticonda.png`: 64×64, palet-modus, transparency=0, exact het palet van E en Silicobra-Uyuni (af), 14 kleuren.
- `salticonda_raster.txt`: één teken per paletindex.
- `vel.png` toont drie dingen:
  - Silicobra-Uyuni (af), kleur1-E en kleur3 op 4× en 1×, op licht en donker.
  - Onderaan de koppen op 8×: pre-evolutie, Sandaconda en de nieuwe kop.
- Scripts in `../scripts/`:
  - `kop3.py`: de kop als handgetekend tekstraster (`KOP`), op E gezet.
  - `check_kleur3.py`: het diff-bewijs, de open randen en de losse pixels.
  - `vel_kleur3.py`: maakt het vel.

## Werkwijze
- **Skelet:** de kop van Silicobra-Uyuni (af) op 1,2× als onderlaag, met dubbele rijen en kolommen eruit. Daarna met de hand verder getekend als tekstraster.
- **Behouden van de pre-evolutie:** dezelfde opbouw en hoek:
  - snuitfront met twee neusgaten naar de kijker;
  - het gezicht als lichte "masker"-vorm onder de rand van de kuif;
  - het oog op het gezicht, met de gezichtslijn (h) en de wangstrook (f) erachter;
  - de koepel daarboven en daarachter.
- Er is geen 3D-onderlaag gebruikt en er zijn geen automatische vormen.

## Checklist
| Punt | Oordeel |
|---|---|
| 3/4, hoek van de pre-evo-kop | ok. Zelfde draaiing naar links-voor. Het snuitfront met twee neusgaten staat naar de kijker en het oog met de turquoise ring zit aan de kijkerskant op het gezicht. Geen profiel: er is geen lange platte snuit en geen oog bovenop de kop zoals in E of kleur2. |
| Groter en zwaarder | ok. Breedte 1,18×, hoogte 1,05× en oppervlak 1,21× de Silicobra-kop (583 tegen 481 px, buiten de band). Dat is twee keer de kop van E (283 px). Binnen "iets groter, ±1,2–1,3". |
| Oog = Silicobra-oog | ok. Ring r/s, bovenring t, lidlijn O die in het midden zakt (halverwege dicht), iris s/t met glans a (19,12) en pupil O. Geen spleet. |
| Zwaardere wenkbrauw | ok. Boven het lid ligt een gewelfde zoutplaat: licht a/b in het midden, naad d die aan de uiteinden zakt en een schaduwrij e/c direct op het lid. Hij zweeft niet. |
| Kroon van zoutplaten met Y-naden | ok. Drie platen en twee Y-punten, trapsgewijs en zonder kruis: (29,6) met de naad uit de kuifdip, de wenkbrauwnaad en de naad naar achter, en (35,9) waar de achternaad samenkomt en verder naar de band loopt. Een bevel-pixel a staat onder elke naad aan de lichtkant. |
| Neusbult (Sandaconda) | ok. Een ronde lichte kap bovenop het snuitfront (x 4–12, y 7–9), met een eigen h-rand en een inkeping naar het voorhoofd. |
| Bredere snuit en kaak (anaconda) | ok. Het snuitfront is 9 rijen hoog en de kaak 1 rij dieper dan bij de pre-evo, met een korte mondlijn (e) en een warme kaak (f/g). |
| Zachte gezichtslijn | ok. h tussen gezicht en kuif, met de f-wangstrook ernaast, zoals in ronde 6 van de pre-evo. |
| Turquoise halsband | ok. 5 rijen (y 20–25). Boven is hij licht (q met glans a), onder donker (s/t). Hij loopt van onder de kin tot de achterkant van de kop, en de onderrand buigt in het midden naar beneden over de bovenste winding. |
| Omlijning en licht | ok. h aan de lichtkant, K/O rechtsonder en licht van linksboven. Open randen: 0. |
| Schattig-loom, niet misvormd | ok. Op 1× en 4× naast de pre-evo leest hij als dezelfde lome slang, ouder en zwaarder. Het is geen krokodillenkop en geen spleetoog (vergeleken met kleur2 A/B). |

## Diff-bewijs (`python3 scripts/check_kleur3.py`)
- **Kopzone:** de rechthoek x 0–47, y 0–25 (kop en halsband).
- **Buiten de kopzone:** 0 pixels gewijzigd ten opzichte van `kleur1/salticonda_E.png`. Lijf, pekelringen, staart, voet en buitenlijn zijn dus bevroren.
- **Binnen de kopzone:** 743 pixels gewijzigd.
  - 76 daarvan zijn lijfpixels van E: de bovenkant van de bovenste winding in rij 21–25, onder de nieuwe, dikkere halsband.
  - Dat is de enige plek waar de kop over het lijf valt.
  - De rug van de bovenste winding rechts (x 44–49, vanaf rij 23) is ongewijzigd en sluit aan op de band.
- **Palet:** identiek aan E. Modus P, transparency 0.
- **Open randen** in de kopzone: 0.
- **Losse pixels:** 40, alleen bewuste details, zoals in kleur1:
  - de trappen en bevels van de naden;
  - de glans in het oog;
  - de f-pixels van de wangstrook;
  - de mond- en kaakschaduw.

## Eerlijk oordeel
- **Hoek:** de kop staat nu in dezelfde 3/4-hoek als de pre-evolutie, omdat hij op die kop is getekend. Zet je de twee naast elkaar, dan lees je dezelfde lijn, groter, met een plaatkroon, een wenkbrauw, een neusbult en een zwaardere kaak.
- **Plaats:** de kop raakt nu de bovenrand (rij 0). Dat was nodig om hem iets hoger te maken dan de pre-evo zonder de bovenste winding verder te bedekken.
- Ik zie geen open zwak punt.

## Lessen
- **Hoek:** een kop "in de hoek van de pre-evo" lukt pas als je de pre-evo-kop 1:1 opschaalt als onderlaag. Een vrij getekende kop schoof elke keer naar profiel: een lange snuit met het oog naar achteren.
- **Breedte en profiel:** de verhouding breedte/hoogte van de kop bepaalt mee of hij als profiel leest. Breder maken zonder hoger maken leest al snel als zijaanzicht, dus kort de snuit of de achterkant in.
- **Naden op een koepel:** laat ze gebogen meelopen met de koepel. Een rechte naad van 8–10 px leest als een streep, en c/d die elkaar afwisselen langs de rand leest als ruis.
