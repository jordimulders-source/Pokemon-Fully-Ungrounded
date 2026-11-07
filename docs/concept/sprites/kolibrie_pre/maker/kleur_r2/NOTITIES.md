# Kolibrie pre-evo – kleur ronde 2 (maker, 2 nov)

Jordi, letterlijk: "fluweel als kleur" · "deze pre evo mag wel een veel mildere kleur hebben, veel minder mysterieus" · "ja beetje het idee zoals dat fletchling nog niet fire is" · "Moet echt cute zijn".
Terugkoppeling van Claude op r1:
1. te plat en te bleek;
2. kop en lijf zijn één kleur;
3. leest als mus of duif, niet als kolibrie;
4. oog mag groter en met meer glans;
5. gele mondhoeken voller.

Het silhouet blijft bevroren.

## Bestanden
- `rijen_r2.txt`: met de hand geschreven, één teken per paletindex.
- `raster.txt`, `kolibrie_pre.png` (geïndexeerd, index 0 transparant), `normal.pal` (JASC).
- `vel.png`: r2 4× op licht en donker; r2 en r1 naast Fletchling, Taillow, Natu en de eindvorm (2× en 1×, licht en donker) en foto 1.
- Scripts: `bouw.py`, `palet.py`, `controle.py`, `vel.py`.

## Wat er per punt veranderde
1. **Volume en pit.**
   - Kernschaduw 3 volgt de bolling: onder het achterhoofd, langs de flank tussen buik en vleugel, en onderin de buik.
   - Het buikhooglicht 7 zit linksboven op de borst; de kop heeft een hooglicht 4 op de kruin linksboven.
   - De omlijning aan de schaduwkant is een stap donkerder: 1 = 30,20,46 (was 44,32,62), diep violet en geen zwart. De onderrand van de buik is nu helemaal 1.
   - De lichtkant is omlijnd met 2 (74,58,108) in plaats van de lichte 3, zodat hij op licht niet meer wegvalt.
   - Aandeel zeer donkere pixels is nu 0,137 (r1: 0,109), midden in de Gen 3-band.
2. **Kap.** Een koelere, diepere lila kap (B 108,98,176, schaduw E 74,64,136, hooglicht 4) over kruin, voorhoofd en achterhoofd. De naad loopt gebogen van het voorhoofd (x15,y14) door de ooglijn naar de nek (x31,y20). Volume via licht linksboven en schaduw rechtsachter. Geen rechte grens, dus geen helm. Gezicht, wang en keel blijven licht lila/wit.
3. **Kolibrie-hint.** Een kleine glanzende blauwgroene keelvlek (gorget) direct onder de bek: een schuine sikkel van 7 px in 8 met 2 px glans 9, die de kinlijn volgt, als voorbode van de keelglans van de eindvorm. Het schouderstreepje is weg. Een eerste versie als horizontale band las als sjaal en is verworpen.
4. **Oog.** 4×5 in plaats van 4×4: bovenlid 1 met zachte hoekjes 2, een glans van 3 px (F) linksboven, iris donker boven en E (licht) onder, onderhoekjes 2. Groter en glanzender, nog steeds een Pokémon-oog met bovenlid.
5. **Mondhoeken.** Het geel is 11+2 px (r1: 6+1): aan de basis van de bovensnavel (x13–14, y14–15), in de hoek 2 px breed (x14–15, y16–17) en over de bovenrand van de ondersnavel (x11–15, y18). Op 1× leest het als een open bedelbek met geel.

## Diff tegen r1
| onderdeel | gewijzigde pixels |
|---|---|
| bek en mondhoek (x ≤ 15, y ≤ 19) | 7 |
| kop: kap, gezicht, oog, keelvlek (y9–21) | 118 |
| borst, buik, flank, vleugel (y22–40) | 138 |
| onderrand, pootjes, staart (y41+) | 7 |
| **totaal** | **270** |

## Palet r2
| index | kleur | gebruik |
|---|---|---|
| 0 | 152,208,160 | transparant |
| 1 | 30,20,46 | omlijning schaduwkant |
| 2 | 74,58,108 | omlijning lichtkant, diepe schaduw |
| 3 | 118,102,162 | kernschaduw |
| 4 | 164,150,208 | lila basis, kaphooglicht |
| 5 | 202,194,236 | lila licht, buikschaduw |
| 6 | 228,224,246 | buik |
| 7 | 252,250,255 | buikhooglicht |
| 8 | 48,140,156 | keelvlek |
| 9 | 124,210,200 | keelvlek glans |
| A | 60,52,78 | snavel, pootjes |
| B | 108,98,176 | kap, snavelhooglicht |
| C | 250,212,72 | mondhoek |
| D | 222,150,40 | mondhoek schaduw |
| E | 74,64,136 | kapschaduw, iris onder |
| F | 255,255,255 | glans |

## Checks (`controle.py`)
- **Alpha-diff tegen silhouet r2: 0.**
- **Open randen: 0.**
- **Losse pixels:** alleen bewuste accenten (ooglidhoekjes, glanspixels van de keelvlek, snavelpixel, overgangen bij kin en onderrand), geen ruis.
- 15 kleuren plus index 0 gebruikt.
- Zelf bekeken op 1× en 4×, op licht en donker, naast r1, Fletchling, Taillow, Natu, de eindvorm en foto 1:
  - Hij leest nu als een bol, zacht lila vogeltje met een eigen, diepere kap.
  - Een groot glanzend oog, een open gele bedelbek en een blauwgroen keelvlekje.
  - Op licht valt hij niet meer weg; de familie met de eindvorm is zichtbaar.
  - Mild, geen Ghost-kenmerken.

## Wat nog niet klopt
Ik zie geen open punten meer.

## Lessen
- "Mild" zit in de tinten, niet in het contrast: een lichte palet met een diep violette omlijning en een echte kernschaduw blijft zacht maar leest wel.
- Een keelvlek als horizontale band leest als sjaal. Een schuine sikkel langs de kinlijn leest als gorget.
- Een kap wordt geen helm als de naad door de ooglijn loopt en gebogen naar de nek zakt, met licht en schaduw binnen de kap.
