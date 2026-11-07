# Keuring poedelmot kleur r20 (onafhankelijk, blind geoordeeld; eerdere keuringen pas daarna gelezen)

Bron: `referenties/samengesteld.png` (mapping x 139–854 → 62 px, offset (1,17)), BOX-verkleind tot 1× (`stappen/box1x.py`) en per spritepixel gemeten (lum van het BOX-model naast de sprite; donkerfractie lum < 85 per cel).
8×: per onderdeel uitgesneden naast het model (16×) met raster. 1×: BOX-model | sprite naast elkaar.

## EIS 1: accuraat op het model
| Onderdeel | Oordeel |
|---|---|
| Ogen | **Lijkt op.** Links x 16–20, y 33–39, glans (18,34–35); rechts x 28–32, y 33–39, glans (28–29,35)/(28,36), bruine reflex rechtsonder en tan ring rechts/onder, alles op de modelplekken (±1 px). Klein: (18,35) is glans (245), model 101; de modelglans is alleen (18,34). |
| Kop/kin | **Lijkt op.** Kruin licht met tan selout, snuit c op x 21–25, y 39–41, kinlijn (21,41)→(22–26,42)→(26–29,41) zoals het model. |
| Sprieten | **Lijkt op.** Donker gestreept vlak met lichte nerf van punt tot voet, links en rechts; omtrek, punten en voeten op de modelpixels. |
| Bontkraag | **Lijkt op.** Wit, linkerrand en onderrand naar de poten op de modelplekken. |
| Linkervleugel | **Lijkt op.** Omtrek en tan streken (rij 30–34) kloppen met de meting. |
| Rechtervoorvleugel | **Wijkt af in de belijning van de linkerrand.** Het model heeft een tweede donkere lijn: de linkerrand van de voorvleugel tegen de spleet bij het lijf, van (43,29) via (42,30), (41,31), (40,32), (40,33) naar (39–40,34) (model 82–117 per cel, op 16× een zwarte lijn). In de sprite is daar crème/wit (190/245); alleen de lijn van het lijf (38–40,30)→(37,33) staat erin. Krullen en buitenrand kloppen. |
| Rechterachtervleugel | **Wijkt af in één pixel:** de lijn voorvleugel/achtervleugel loopt (41–51,35), (52–53,36), dan een gat op (54,36) (sprite 245, model 151; op 16× ligt de lijn daar op y 36,3–37,0) en verder (55,37)–(56,37). De lijn is dus onderbroken. Onderrand (45–52,46–47) en patroon kloppen. |
| Middenstuk | **Lijkt op**, op één pixel na: (35,50) is licht (209), het model is daar donker (82), de bovenrand van de middenpoot sluit daardoor niet aan op (34,50). |
| Poot 1 (links voor) + klauw | **Lijkt op.** x 16–23, y 47–55, klauw (19–21,55–56) zoals het model. |
| Poot 2 + voetbal + klauwen | **Lijkt op.** Klauwen (24–27,56–59) vallen samen met het modeldonker. |
| Verre poot (x 31–34) + klauwen | **Lijkt op.** |
| Middenpoot voor + klauwen | **Lijkt op.** Klauwen (36–39,60–61). |
| Rechterpoot + klauwen | **Lijkt op.** Klauwen (43–46,57–59). |
| Rechter achterlob | **Lijkt op.** |
| Belijning buiten | **Lijkt op.** 0 open randen, 1 px, zwart alleen aan de onderkant van de sprieten en op de ogen, geen afwisseling zwart/2 op één rand. |

## EIS 2: Gen 3 (naast Dustox en Beautifly `anim_front_gba.png`)
Voldoet: 14 kleuren, 0 losse pixels, 0 clusters < 3 px, buitenlijn 1 px, gekleurde selout aan de lichtkant (zoals Dustox), licht linksboven. Het enige netheidspunt valt samen met EIS 1: de onderbroken lijn op (54,36).

## Reparaties (alleen echte afwijkingen)
1. **Linkerrand voorvleugel:** (42,30), (41,31), (40,32), (40,33) in lijntint 4, zodat de lijn aansluit op (40,34) en boven op de sprietrand. De witte strook tussen deze lijn en de lijflijn (38–39,31–33) blijft wit.
2. **Gat dichten:** (54,36) in 4.
3. **Middenpoot:** (35,50) in 4.
4. **Klein:** glans linkeroog alleen (18,34); (18,35) in donkere oogtint (model 101).

Oordeel: FAIL
